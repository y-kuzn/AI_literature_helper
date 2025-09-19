import streamlit as st
import requests, json, re, os, io
import xml.etree.ElementTree as ET
from pyzotero import zotero
import fitz  # PyMuPDF
from time import sleep
from requests import RequestException
from datetime import datetime

# ----------------------------
# GEMINI (google-genai)
# ----------------------------
# pip install google-genai
from google import genai

# ============================
# CONFIG
# ============================
st.set_page_config(page_title="📚 AI Literature Helper", page_icon="🤖")

SEMANTIC_SCHOLAR_API_KEY = st.secrets["SEMANTIC_SCHOLAR_API_KEY"]
GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
NCBI_EMAIL = st.secrets["NCBI_EMAIL"]
NCBI_API_KEY = st.secrets["NCBI_API_KEY"]
client = genai.Client(api_key=GEMINI_API_KEY)

SLEEP = 0.08  # pacing for retries/backoff
PREFS_FILE = "prefs.json"

# ============================
# PREFERENCES (saved locally)
# ============================
def load_prefs():
    if not os.path.exists(PREFS_FILE):
        return {"topics": [], "authors": []}
    try:
        return json.load(open(PREFS_FILE))
    except Exception:
        return {"topics": [], "authors": []}

def save_prefs(topics, authors):
    with open(PREFS_FILE, "w") as f:
        json.dump({"topics": topics, "authors": authors}, f)

prefs = load_prefs()

# ============================
# UI
# ============================
st.title("📚 AI Literature Helper")

search_mode = st.radio(
    "🔍 What would you like to do?",
    [
        "Keyword Search",
        "Paste citation / page text",
        "Lookup by URL / PDF ",
    ],
    horizontal=False,
)

# Source selector ONLY for Keyword Search (removed for Paste mode per request)
search_source = st.selectbox(
    "📡 Choose search source",
    ["Semantic Scholar", "PubMed", "Both"]
) if search_mode == "Keyword Search" else None

max_results = st.slider("📄 Max articles to fetch:", 5, 100, 20, 1)

# Unified relevance is score3 (0..3)
min_score3 = st.slider("⭐ Minimum AI relevance score3 to save to Zotero (0–3):", 0, 3, 2, 1)

if search_mode == "Keyword Search":
    user_prompt = st.text_input("🔍 Enter your research topic or keywords:")
    use_boolean = st.checkbox("🔤 Convert to Boolean query (AI-optimized)")
elif search_mode == "Paste citation / page text":
    paste_text = st.text_area("📋 Paste citation(s) or Google Scholar results / page text:", height=220)
else:
    url_or_doi = st.text_input("🔗 Paste a URL (landing page or PDF):")

with st.sidebar:
    st.header("🔖 Preferences")
    topics_txt = st.text_input("Priority Topics (comma-separated)", ", ".join(prefs.get("topics", [])))
    authors_txt = st.text_input("Priority Authors (comma-separated)", ", ".join(prefs.get("authors", [])))
    if st.button("💾 Save Preferences"):
        save_prefs([t.strip() for t in topics_txt.split(",") if t.strip()],
                   [a.strip() for a in authors_txt.split(",") if a.strip()])
        st.sidebar.success("Saved preferences.")

add_to_zotero = st.checkbox("📥 Add articles to Zotero")
user_zotero_key = user_zotero_id = user_zotero_collection = ""
allow_duplicates = False
if add_to_zotero:
    st.markdown("### 🔐 Zotero Credentials")
    user_zotero_key = st.text_input("Zotero API Key")
    user_zotero_id = st.text_input("Zotero User ID")
    user_zotero_collection = st.text_input("Zotero Collection ID")
    allow_duplicates = st.checkbox("⚠️ Allow Zotero duplicates", value=False)

# ============================
# HELPERS
# ============================
OPERATORS = {"and": "AND", "or": "OR", "not": "NOT"}

DOI_RE = re.compile(r"10\.\d{4,9}/[-._;()/:A-Za-z0-9]+", re.I)
HTML_TAG_RE = re.compile(r"<[^>]+>")
ARXIV_RE = re.compile(r"arXiv:\s*(\d{4}\.\d{4,5})(?:v\d+)?", re.I)

def build_boolean_query_simple(text: str) -> str:
    """Quick AND-join of comma/;/slash separated tokens; phrases quoted and logicals normalized."""
    q = text.strip()
    tokens = [t.strip() for t in re.split(r",|;|/", q) if t.strip()]
    if len(tokens) >= 2:
        q = " AND ".join([f'"{t}"' if " " in t else t for t in tokens])
    q = re.sub(r"\b(and|or|not)\b", lambda m: OPERATORS[m.group(1).lower()], q, flags=re.I)
    return q

def with_ntu_proxy(url: str | None, style: int = 2) -> str | None:
    if not url:
        return None
    if style == 1:
        return f"https://remotexs.ntu.edu.sg/user/login?dest={url}"
    return f"https://remotexs.ntu.edu.sg/login?url={url}"

def extract_pdf_text(url: str) -> str:
    """Download a PDF and return the first ~5000 chars of text, or empty string if fails."""
    if not url:
        return ""
    try:
        r = requests.get(url, timeout=45)
        r.raise_for_status()
        with fitz.open(stream=io.BytesIO(r.content), filetype="pdf") as doc:
            text = []
            for page in doc:
                text.append(page.get_text())
            return ("\n".join(text))[:5000]
    except Exception:
        return ""

def parse_authors(authors_info: str):
    authors = [a.strip() for a in authors_info.split(",") if a.strip()]
    out = []
    for nm in authors:
        parts = nm.split(" ")
        if len(parts) >= 2:
            out.append({"creatorType": "author", "firstName": " ".join(parts[:-1]), "lastName": parts[-1]})
        else:
            out.append({"creatorType": "author", "name": nm})
    return out

def dedupe_results(results):
    seen, out = set(), []
    for r in results:
        doi = (r.get("doi") or "").lower().replace("https://doi.org/", "")
        key = doi or (r.get("url") or r.get("title", "")).lower()
        if key in seen:
            continue
        seen.add(key); out.append(r)
    return out

def _request_json_with_retries(url, *, method="GET", headers=None, params=None, data=None, tries=4, timeout=40):
    delay = SLEEP
    for attempt in range(1, tries + 1):
        try:
            resp = (requests.post(url, headers=headers, params=params, data=data, timeout=timeout)
                    if method == "POST" else
                    requests.get(url, headers=headers, params=params, timeout=timeout))
            if 200 <= resp.status_code < 300:
                return resp.json()
            if 500 <= resp.status_code < 600:
                raise RequestException(f"Server {resp.status_code}")
            resp.raise_for_status()
        except Exception:
            if attempt == tries:
                raise
            sleep(delay)
            delay = min(delay * 2, 3.0)
    return {}

def _chunks(seq, n):
    for i in range(0, len(seq), n):
        yield seq[i:i+n]

def _take(results, k):
    return results[:k] if len(results) > k else results

def clean_snippet(text: str) -> str:
    if not text:
        return ""
    text = HTML_TAG_RE.sub(" ", text)
    text = re.sub(r"\s+", " ", text).strip()
    if DOI_RE.fullmatch(text.replace("doi:", "").strip().lower()):
        return ""
    text = re.sub(r"^doi:\s*10\.\d{4,9}/\S+\s*", "", text, flags=re.I)
    return text

# ============================
# GEMINI (Boolean, extraction, annotation)
# ============================
def gemini_json(prompt: str, model: str = "gemini-2.5-flash") -> dict | list:
    if not GEMINI_API_KEY:
        return {}
    try:
        resp = client.models.generate_content(
            model=model,
            contents=prompt,
            config={"response_mime_type": "application/json"},
        )
        txt = resp.text or ""
        try:
            return json.loads(txt)
        except Exception:
            m = re.search(r"\{[\s\S]*\}|\[[\s\S]*\]", txt)
            return json.loads(m.group(0)) if m else {}
    except Exception:
        return {}

def gemini_boolean_query(user_query: str) -> dict:
    data = gemini_json(f"""
Create a compact Boolean query (use AND/OR/NOT and quotes for phrases) suitable for academic APIs.
Return JSON {{"boolean_query": "...", "keywords": [], "year_from": null, "year_to": null}}
Topic: {user_query}
Priority topics: {prefs.get('topics')}
""")
    out = {"boolean_query": "", "keywords": [], "year_from": None, "year_to": None}
    if isinstance(data, dict):
        out["boolean_query"] = data.get("boolean_query") or ""
        out["keywords"] = data.get("keywords") or []
        out["year_from"] = data.get("year_from")
        out["year_to"] = data.get("year_to")
    return out

def gemini_extract_from_text(raw_text: str):
    """
    Extract refs from pasted text (e.g., Google Scholar page).
    Returns list of {title, authors:[...], year, doi?}
    """
    data = gemini_json(f"""
You are an academic reference extractor.
From the text below, extract a list of references as JSON array. Each object must have:
- "title" (string)
- "authors" (list of names)
- "year" (int if available else null)
- "doi" (string DOI without https://doi.org/ if present else null)

Text:
{raw_text}

Return strictly a JSON array.
""")
    out = []
    if isinstance(data, list):
        for it in data:
            if not isinstance(it, dict):
                continue
            title = (it.get("title") or "").strip()
            if not title:
                continue
            authors = it.get("authors") or []
            if isinstance(authors, str):
                authors = [a.strip() for a in authors.split(",") if a.strip()]
            year = it.get("year")
            doi  = it.get("doi")
            if isinstance(doi, str):
                m = DOI_RE.search(doi)
                doi = m.group(0) if m else doi.strip()
            out.append({"title": title, "authors": authors, "year": year, "doi": doi})
    return out

def gemini_annotate_paper(title, authors, snippet, pdf_text, url, user_query):
    """
    Return: abstract (10–15 sentences), tags [aRT..., aTa..., aTy..., aMe..., ai score-n], score3 (0..3)
    """
    prompt = f"""
You are an academic assistant. Analyze this paper and return JSON with keys:
- "abstract": a 10–15 sentence abstract (self-contained; no refs; no hallucinations)
- "tags": list of strings with REQUIRED prefixes:
  * aRT – research topic (1–2 concise tags)
  * aTa – very specific topical tags (3–6 concise tags)
  * aTy – paper type (e.g., review, experimental, meta-analysis)
  * aMe – key method(s)
  * Plus exactly one tag "ai score-N" where N is 0..3
- "score3": integer 0..3 relevance to the query (0=marginal, 3=high)

Paper info:
Title: {title}
Authors: {authors}
Context: {snippet}
PDF: {pdf_text}
URL: {url}

User query: {user_query}
Priority topics: {prefs.get('topics')}
Priority authors: {prefs.get('authors')}

Output JSON only.
"""
    data = gemini_json(prompt)
    abstract, tags, score3 = "", [], 0
    if isinstance(data, dict):
        abstract = data.get("abstract", "") or ""
        raw_tags = data.get("tags", []) or []
        score3 = data.get("score3", 0) or 0
        try:
            score3 = int(score3)
        except Exception:
            score3 = 0
        tags = [t for t in raw_tags if isinstance(t, str)]
    # ensure ai score-n tag exists and matches score3
    score_tag = f"ai score-{max(0, min(3, score3))}"
    if score_tag not in tags:
        tags.append(score_tag)
    return abstract.strip(), tags, max(0, min(3, score3))

# ============================
# SEARCH PROVIDERS (S2 + PubMed) + Crossref + Google fallback
# ============================
def search_semantic_scholar(query, limit=10):
    """Stable Semantic Scholar search."""
    url = "https://api.semanticscholar.org/graph/v1/paper/search"
    headers = {"x-api-key": SEMANTIC_SCHOLAR_API_KEY} if SEMANTIC_SCHOLAR_API_KEY else {}
    params = {
        "query": query,
        "limit": limit,
        "fields": "title,authors,url,abstract,openAccessPdf,externalIds,venue,year,citationCount,publicationDate,publicationTypes"
    }
    try:
        response = requests.get(url, headers=headers, params=params, timeout=30)
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        st.error(f"Semantic Scholar error: {e}")
        return []

    results = []
    for paper in (data or {}).get("data", []) or []:
        doi = None
        if isinstance(paper.get("externalIds"), dict):
            doi = paper["externalIds"].get("DOI")
        results.append({
            "title": paper.get("title", ""),
            "url": paper.get("url", "") or (f"https://doi.org/{doi}" if doi else ""),
            "authors_info": ", ".join([a.get("name", "") for a in paper.get("authors", [])]),
            "snippet": clean_snippet(paper.get("abstract", "") or ""),
            "pdf_url": (paper.get("openAccessPdf") or {}).get("url", ""),
            "doi": doi,
            "venue": paper.get("venue"),
            "year": paper.get("year"),
            "citationCount": paper.get("citationCount"),
            "publicationDate": paper.get("publicationDate"),
            "publicationTypes": paper.get("publicationTypes"),
        })
    return results

def semantic_scholar_by_doi(doi: str):
    if not doi:
        return None
    url = f"https://api.semanticscholar.org/graph/v1/paper/DOI:{doi}"
    headers = {"x-api-key": SEMANTIC_SCHOLAR_API_KEY} if SEMANTIC_SCHOLAR_API_KEY else {}
    params = {"fields": "title,authors,url,abstract,openAccessPdf,externalIds,venue,year,citationCount,publicationDate,publicationTypes"}
    try:
        r = requests.get(url, headers=headers, params=params, timeout=20)
        r.raise_for_status()
        p = r.json()
        return {
            "title": p.get("title", ""),
            "url": p.get("url", "") or (f"https://doi.org/{doi}"),
            "authors_info": ", ".join([a.get("name", "") for a in p.get("authors", [])]),
            "snippet": clean_snippet(p.get("abstract", "") or ""),
            "pdf_url": (p.get("openAccessPdf") or {}).get("url", ""),
            "doi": (p.get("externalIds") or {}).get("DOI") or doi,
            "venue": p.get("venue"),
            "year": p.get("year"),
            "citationCount": p.get("citationCount"),
            "publicationDate": p.get("publicationDate"),
            "publicationTypes": p.get("publicationTypes"),
        }
    except Exception:
        return None

def search_pubmed(query, limit=10):
    """
    Simple, robust PubMed: GET ESearch + ESummary + (best-effort) EFetch abstracts; term capped to 300 chars.
    """
    base = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
    term = (query or "")[:300]  # PubMed truncation
    es_params = {"db": "pubmed", "term": term, "retmode": "json", "retmax": limit, "email": NCBI_EMAIL}
    if NCBI_API_KEY:
        es_params["api_key"] = NCBI_API_KEY
    try:
        es = requests.get(f"{base}/esearch.fcgi", params=es_params, timeout=30).json()
    except Exception as e:
        st.error(f"PubMed ESearch error: {e}")
        return []

    ids = (es.get("esearchresult", {}) or {}).get("idlist", []) or []
    if not ids:
        return []

    # ESummary (basic metadata)
    sum_params = {"db": "pubmed", "id": ",".join(ids), "retmode": "json", "email": NCBI_EMAIL}
    if NCBI_API_KEY:
        sum_params["api_key"] = NCBI_API_KEY
    try:
        sm = requests.get(f"{base}/esummary.fcgi", params=sum_params, timeout=30).json()
    except Exception as e:
        st.error(f"PubMed ESummary error: {e}")
        return []

    # EFetch to get abstracts (XML) — best effort
    abstracts = {}
    try:
        ef_params = {"db": "pubmed", "retmode": "xml", "email": NCBI_EMAIL}
        if NCBI_API_KEY:
            ef_params["api_key"] = NCBI_API_KEY
        ef = requests.post(f"{base}/efetch.fcgi", params=ef_params, data={"id": ",".join(ids)}, timeout=40)
        ef.raise_for_status()
        root = ET.fromstring(ef.text)
        for art in root.findall(".//PubmedArticle"):
            pmid = art.findtext(".//PMID")
            abst_nodes = art.findall(".//Abstract/AbstractText")
            abs_text = " ".join((n.text or "") for n in abst_nodes).strip()
            abstracts[pmid] = clean_snippet(abs_text)
    except Exception:
        pass

    out, block = [], sm.get("result", {}) or {}
    for pmid in ids[:limit]:
        r = block.get(pmid, {}) or {}
        jrnl = r.get("fulljournalname") or r.get("source")
        # year parsing
        year = None
        try:
            dp = r.get("pubdate") or ""
            m = re.search(r"\b(19|20)\d{2}\b", dp)
            if m:
                year = int(m.group(0))
        except Exception:
            pass

        out.append({
            "title": r.get("title", ""),
            "url": f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/",
            "authors_info": ", ".join([a.get("name","") for a in (r.get("authors") or [])]) if isinstance(r.get("authors", []), list) else "",
            "snippet": abstracts.get(pmid) or clean_snippet(r.get("source", "") or ""),
            "pdf_url": "",
            "doi": None,
            "venue": jrnl,
            "year": year,
            "citationCount": None,
            "publicationDate": r.get("pubdate"),
            "publicationTypes": r.get("pubtype"),
        })
    return out

# ---------- Crossref enrichment (if DOI is known) ----------
def crossref_enrich(doi: str) -> dict:
    if not doi:
        return {}
    url = f"https://api.crossref.org/works/{doi}"
    try:
        data = _request_json_with_retries(url, timeout=30)
        msg = (data or {}).get("message", {})
        if not msg:
            return {}
        title = (msg.get("title") or [""])[0]
        journal = (msg.get("container-title") or [""])[0]
        date_parts = (msg.get("issued") or {}).get("date-parts", [[]])
        year = date_parts[0][0] if date_parts and date_parts[0] else None
        volume = msg.get("volume")
        issue = msg.get("issue")
        page = msg.get("page")
        url = msg.get("URL")
        authors = []
        for a in msg.get("author", []) or []:
            nm = f"{a.get('given','')} {a.get('family','')}".strip()
            if nm: authors.append(nm)
        return {
            "title": title,
            "venue": journal,
            "year": year,
            "volume": volume,
            "issue": issue,
            "pages": page,
            "url": url,
            "authors_info": ", ".join(authors),
        }
    except Exception:
        return {}

# ---------- URL / PDF handling ----------
def fetch_url_and_guess_pdf(url: str) -> tuple[bool, str]:
    """Return (is_pdf, text). Detect PDF by header, extension, or magic bytes.
       If PDF, extract up to 8000 chars; else return (False, "")."""
    try:
        r = requests.get(url, timeout=45, allow_redirects=True)
        r.raise_for_status()
        ctype = r.headers.get("content-type", "").lower()
        content = r.content

        # PDF detection: by header, extension, or magic number
        is_pdf = (
            "pdf" in ctype
            or url.lower().endswith(".pdf")
            or content.startswith(b"%PDF")
        )

        if is_pdf:
            with fitz.open(stream=io.BytesIO(content), filetype="pdf") as doc:
                text = []
                for page in doc:
                    text.append(page.get_text())
                return True, ("\n".join(text))[:8000]

        return False, ""
    except Exception:
        return False, ""

def extract_metadata_from_pdf_text(pdf_text: str) -> dict:
    """Find DOI, a plausible title, author line."""
    if not pdf_text:
        return {}
    md = {}
    doi_m = DOI_RE.search(pdf_text)
    if doi_m:
        md["doi"] = doi_m.group(0)
    # crude title guess: first reasonable line before 'Abstract'
    lines = [ln.strip() for ln in pdf_text.splitlines() if ln.strip()]
    title = None
    for ln in lines[:60]:
        if re.match(r"^abstract\b", ln, re.I):
            break
        if 8 <= len(ln) <= 240 and not re.search(r"(doi:|arxiv:)", ln, re.I):
            title = ln
            break
    if title:
        md["title"] = title
    # weak authors pattern
    for j in range(1, 8):
        if j < len(lines):
            cand = lines[j]
            if re.search(r"[A-Z][a-z]+\s+[A-Z][a-z]+", cand):
                md["authors_info"] = cand
                break
    return md

def google_search_fallback(query: str):
    """Very light fallback via Google Custom Search (requires valid key & cx)."""
    try:
        r = requests.get(
            "https://www.googleapis.com/customsearch/v1",
            params={
                "q": query,
                "key": GEMINI_API_KEY,  # reuse key; replace with your proper CSE key
                "cx": "017576662512468239146:omuauf_lfve",  # demo CX; replace with your own
            },
            timeout=20,
        )
        data = r.json()
        items = data.get("items", []) or []
        if not items:
            return []
        out = []
        for it in items:
            out.append({
                "title": it.get("title"),
                "url": it.get("link"),
                "authors_info": "",
                "snippet": it.get("snippet"),
                "pdf_url": "",
                "doi": None,
                "venue": None,
                "year": None
            })
        return out
    except Exception:
        return []

# ============================
# MAIN ACTION
# ============================
if st.button("🚀 Go"):
    progress = st.progress(0)
    status = st.empty()

    papers_meta = []
    try:
        # 1) KEYWORD SEARCH
        if search_mode == "Keyword Search":
            if not user_prompt or not user_prompt.strip():
                st.warning("Please enter a research topic.")
                st.stop()

            status.info("🧠 Preparing query…")
            if use_boolean:
                b = gemini_boolean_query(user_prompt)
                effective_query = b.get("boolean_query") or build_boolean_query_simple(user_prompt)
                if b.get("keywords"):
                    st.caption("Keywords: " + ", ".join((b.get("keywords") or [])[:12]))
                if b.get("year_from") or b.get("year_to"):
                    st.caption(f"Years: {b.get('year_from')}–{b.get('year_to')}")
            else:
                effective_query = build_boolean_query_simple(user_prompt)

            # Editable query box
            effective_query = st.text_area("✏️ Editable search query (you can tweak before searching):", effective_query)
            progress.progress(10)

            agg = []
            if search_source in ("Semantic Scholar", "Both"):
                status.info("🔎 Searching Semantic Scholar…")
                try:
                    agg.extend(search_semantic_scholar(effective_query, limit=max_results))
                except Exception as e:
                    st.warning(f"Semantic Scholar failed: {e}")
                progress.progress(30)

            if search_source in ("PubMed", "Both"):
                status.info("🧬 Searching PubMed…")
                try:
                    agg.extend(search_pubmed(effective_query, limit=max_results))
                except Exception as e:
                    st.warning(f"PubMed failed: {e}")
                progress.progress(50)

            status.info("📦 Combining results…")
            papers_meta = _take(dedupe_results(agg), max_results)
            progress.progress(60)

        # 2) PASTE CITATION / TEXT (Gemini extraction + PubMed + Google fallback; DOI→S2 if available)
        elif search_mode == "Paste citation / page text":
            if not paste_text.strip():
                st.warning("Please paste citation(s) or text.")
                st.stop()

            status.info("🧾 Extracting references with Gemini…")
            refs = gemini_extract_from_text(paste_text)
            progress.progress(30)

            if not refs:
                status.warning("")
                progress.progress(100)
                st.error("😅 We squinted at every reference style… but found nada.")
                st.caption("Try another copy/paste (e.g., select all items on the Google Scholar results page).")
                st.stop()

            status.info("🔎 Enriching references…")
            collected = []
            for r in refs[:max_results]:
                title, authors, year, doi = r.get("title"), r.get("authors"), r.get("year"), r.get("doi")
                enriched = None

                # 1. DOI → Semantic Scholar enrichment
                if doi:
                    enriched = semantic_scholar_by_doi(doi)

                # 2. PubMed by title
                if not enriched and title:
                    pm = search_pubmed(title, 1)
                    enriched = pm[0] if pm else None

                # 3. Google fallback
                if not enriched and title:
                    gg = google_search_fallback(title)
                    enriched = gg[0] if gg else None

                # 4. If still nothing → bare metadata
                if not enriched:
                    enriched = {
                        "title": title,
                        "authors_info": ", ".join(authors) if isinstance(authors, list) else (authors or ""),
                        "snippet": "",
                        "url": "",
                        "pdf_url": "",
                        "doi": doi,
                        "year": year,
                        "venue": None
                    }
                collected.append(enriched)

            papers_meta = collected
            progress.progress(60)

        # 3) LOOKUP BY URL / DOI / PDF
        else:  # search_mode == "Lookup by URL / PDF"
            if not url_or_doi or not url_or_doi.strip():
                st.warning("Please paste a URL or DOI.")
                st.stop()

            val = url_or_doi.strip()
            status.info("🧭 Resolving input…")
            progress.progress(10)

            if DOI_RE.fullmatch(val):
                # DOI path: Crossref enrich + S2 by title if possible
                doi = val
                enr = crossref_enrich(doi)
                title = enr.get("title")
                if title:
                    status.info("🔎 Searching Semantic Scholar by title…")
                    ss = search_semantic_scholar(title, limit=1)
                else:
                    ss = []
                base = {
                    "title": enr.get("title"),
                    "url": enr.get("url"),
                    "authors_info": enr.get("authors_info"),
                    "snippet": "",
                    "pdf_url": "",
                    "doi": doi,
                    "venue": enr.get("venue"),
                    "year": enr.get("year"),
                }
                papers_meta = [ss[0] | base] if ss else [base]
                progress.progress(60)
            else:
                # Assume URL
                is_pdf, pdf_text = fetch_url_and_guess_pdf(val)
                progress.progress(25)
                if is_pdf:
                    status.info("📄 PDF detected — extracting metadata…")
                    md = extract_metadata_from_pdf_text(pdf_text)
                    doi = md.get("doi")
                    if doi:
                        enr = crossref_enrich(doi)
                    else:
                        enr = {}
                    title = md.get("title") or enr.get("title")
                    status.info("🔎 Searching Semantic Scholar by title…")
                    ss = search_semantic_scholar(title, limit=1) if title else []
                    base = {
                        "title": title,
                        "url": val,
                        "authors_info": md.get("authors_info") or enr.get("authors_info"),
                        "snippet": clean_snippet(pdf_text[:1200]),
                        "pdf_url": val,
                        "doi": doi,
                        "venue": enr.get("venue"),
                        "year": enr.get("year"),
                    }
                    papers_meta = [ss[0] | base] if ss else [base]
                    progress.progress(70)
                else:
                    status.info("🌐 Not a PDF — trying title guess from URL path…")
                    guessed = re.sub(r"[-_/]+", " ", val.split("//")[-1])[:120]
                    ss = search_semantic_scholar(guessed, limit=1)
                    papers_meta = ss
                    progress.progress(70)

        # Initialize Zotero (optional)
        if add_to_zotero and user_zotero_key and user_zotero_id:
            try:
                zot = zotero.Zotero(user_zotero_id, 'user', user_zotero_key)
            except Exception as e:
                st.error(f"Zotero initialization error: {e}")
                zot = None
        else:
            zot = None

        # If nothing found — friendly message
        if not papers_meta:
            status.warning("")
            progress.progress(100)
            st.error("😅 We searched high, low, and even peered behind the paywall sofa cushions… but found nada.")
            st.caption("Try tweaking the query or switching modes. Even librarians have off days.")
            st.stop()

        # Render + Gemini analysis (UNIFIED)
        status.info("🧪 Analyzing and annotating…")
        progress.progress(75)

        # Map Zotero threshold: score3 (0..3)
        zotero_threshold_score3 = min(3, max(0, int(min_score3)))

        for i, paper in enumerate(papers_meta):
            title = paper.get("title", "")
            url = paper.get("url", "")
            authors_info = paper.get("authors_info", "")
            snippet = paper.get("snippet", "")
            pdf_url = paper.get("pdf_url", "")
            doi = paper.get("doi")
            venue = paper.get("venue")
            year = paper.get("year")

            # Pull PDF text when useful
            pdf_text = extract_pdf_text(pdf_url or url)

            with st.expander(f"📄 {title or 'Untitled'}", expanded=True):
                if authors_info:
                    st.markdown(f"**Authors:** {authors_info}")
                if venue or year:
                    st.markdown(f"**Venue / Year:** {venue or '—'} — {year or '—'}")
                if snippet:
                    st.markdown(f"**Abstract (source):** {snippet}")

                if url:
                    st.markdown(f"[🔗 View Paper]({url})")
                    doi_or_url = f"https://doi.org/{doi}" if doi else url
                    inst1 = with_ntu_proxy(doi_or_url, style=1)
                    inst2 = with_ntu_proxy(doi_or_url, style=2)
                    if inst1:
                        st.markdown(f"[🏫 NTU Access (style 1)]({inst1})")
                    if inst2:
                        st.markdown(f"[🏫 NTU Access (style 2)]({inst2})")

                # Unified Gemini annotation
                user_query = (
                    user_prompt if search_mode == 'Keyword Search' else
                    (title or paste_text if search_mode == 'Paste citation / page text' else url_or_doi)
                )

                try:
                    abstract_ai, tags, score3 = gemini_annotate_paper(
                        title, authors_info, snippet, pdf_text, url, user_query
                    ) if GEMINI_API_KEY else ("", [], 0)
                except Exception as e:
                    st.error(f"Gemini API error: {e}")
                    abstract_ai, tags, score3 = "", [], 0

                if abstract_ai:
                    st.markdown("**Abstract (AI):**")
                    st.write(abstract_ai)
                if tags:
                    st.markdown("**🏷️ Tags:** " + ", ".join(tags))
                st.markdown(f"**AI Relevance (0–3):** `{score3}`")

                # Zotero save with consistent metadata
                if add_to_zotero and zot and user_zotero_collection and (score3 >= zotero_threshold_score3):
                    doi_or_url = f"https://doi.org/{doi}" if doi else url
                    proxy_url = with_ntu_proxy(doi_or_url, style=1) or with_ntu_proxy(doi_or_url, style=2) or url

                    item = {
                        'itemType': 'journalArticle',
                        'title': title,
                        'creators': parse_authors(authors_info),
                        'abstractNote': abstract_ai or snippet,
                        'tags': [{'tag': t} for t in (tags or [])],
                        'url': proxy_url,
                        'date': str(year) if year else None,
                        'DOI': doi,
                        'collections': [user_zotero_collection]
                    }
                    item = {k: v for k, v in item.items() if v not in (None, "")}

                    duplicate_found = False
                    if not allow_duplicates and title.strip():
                        try:
                            existing_items = zot.items(q=title, itemType="journalArticle")
                            for existing in existing_items:
                                t = existing.get("data", {}).get("title", "").strip().lower()
                                if t == title.strip().lower():
                                    duplicate_found = True
                                    break
                            if doi and not duplicate_found:
                                existing2 = zot.items(q=doi, itemType="journalArticle")
                                for ex in existing2:
                                    if doi and (doi.lower() in json.dumps(ex.get("data", {})).lower()):
                                        duplicate_found = True
                                        break
                        except Exception as e:
                            st.warning(f"⚠️ Zotero duplicate check failed: {e}")

                    if duplicate_found and not allow_duplicates:
                        st.warning(f"⚠️ Skipped Zotero save: duplicate found for '{title}'")
                    else:
                        try:
                            zot.create_items([item])
                            st.success(f"✅ Added to Zotero (score3={score3})")
                        except Exception as e:
                            st.error(f"❌ Zotero error: {e}")

        status.success("Done ✅")
        progress.progress(100)

    finally:
        # Clear status after a short delay to avoid lingering messages
        sleep(0.4)
        status.empty()
