# help.py — Comprehensive Help & Troubleshooting for AI Literature Helper
# ~500 lines covering all common issues, disclaimers, and FAQs

import streamlit as st

# Page setup
st.set_page_config(page_title="AI Literature Helper – Help", page_icon="🆘", layout="wide")

# Sidebar navigation
st.sidebar.title("📘 Help Navigation")
section = st.sidebar.radio("Jump to section:", [
    "Overview",
    "Getting Started",
    "Recommended Workflow",
    "Boolean Queries",
    "AI Annotations & Relevance",
    "Paste Citation Mode",
    "URL / PDF Lookup",
    "Disclaimers & Limitations",
    "Text Parsing Issues",
    "PDF Parsing Issues",
    "PubMed & Semantic Scholar",
    "API Errors",
    "Zotero Integration",
    "Duplicates & Metadata",
    "Performance & Limits",
    "Institutional Access & Proxies",
    "Secrets & Configuration",
    "Tips & Best Practices",
    "FAQs",
    "Troubleshooting Checklist",
    "Ask Gemini",
    "Contact"
])
st.sidebar.markdown("---")

st.sidebar.markdown("""
<div style="text-align: center;">
    <a href="/" target="_self">
        <button style="
            background-color: #4CAF50;
            color: white;
            padding: 10px 20px;
            margin-top: 10px;
            border: none;
            border-radius: 5px;
            font-size: 16px;
            cursor: pointer;
        ">
            🔙 Go Back to Main App
        </button>
    </a>
</div>
""", unsafe_allow_html=True)


# ========== Sections ==========

if section == "Overview":
    st.title("🆘 Help & Instructions")
    st.markdown("""
    Welcome to **AI Literature Helper** — your research assistant powered by PubMed, Semantic Scholar, Crossref, and Gemini AI.

    This app helps you:
    - Search academic papers (PubMed, Semantic Scholar)
    - Extract metadata from citations, DOIs, or PDFs
    - Generate AI abstracts, tags, and relevance scores
    - Save papers directly to Zotero

    ⚠️ **Important:** This tool assists your literature review. Always double-check metadata, abstracts, and relevance scores against the original sources.
    """)

elif section == "Getting Started":
    st.header("🚀 Getting Started")
    st.markdown("""
    1. Open the app in your browser.
    2. Choose a mode:
       - **Keyword Search** (best for systematic review)
       - **Paste Citation / Text** (fallback for copied references)
       - **URL / DOI / PDF Lookup** (last resort if no metadata found)
    3. Adjust:
       - **Max Results**
       - **Minimum Relevance Score (0–3)**
    4. (Optional) Add Zotero credentials in the sidebar.
    5. Click **🚀 Go** to start.

    Results show:
    - AI Abstract (10–15 sentences)
    - Tags (`aRT`, `aTa`, `aTy`, `aMe`, `ai score-N`)
    - AI Relevance score (0–3)
    - Links to paper, DOI, and NTU proxy access
    """)

elif section == "Recommended Workflow":
    st.header("✅ Recommended Workflow")
    st.markdown("""
    For **best results**:

    1. **Always start with Keyword Search**:
       - Use **PubMed** and/or **Semantic Scholar**
       - Enable AI Boolean optimization if your query is complex
    2. If paper not found:
       - Try **Paste Citation / Text** mode
       - Paste from Google Scholar or your reference list
    3. As a **last resort**:
       - Use **URL / DOI / PDF Lookup**
       - Works best with official DOIs or open-access PDFs

    👉 PubMed & Semantic Scholar APIs are **most reliable**.  
    👉 Paste/URL/PDF modes may fail due to parsing errors or paywalls.
    """)

elif section == "Boolean Queries":
    st.header("🔤 Boolean Queries")
    st.markdown("""
    - AI can generate Boolean queries (AND, OR, NOT).
    - PubMed truncates queries after **300 characters**.
    - Always review AI-suggested queries in the editable box.
    - Example: `"CRISPR" AND "prime editing" NOT "review"`

    ⚠️ Long or nested queries may break. Simplify into key terms.
    """)

elif section == "AI Annotations & Relevance":
    st.header("🤖 AI Annotations & Relevance")
    st.markdown("""
    Each paper is analyzed by Gemini AI:

    - **AI Abstract**: 10–15 self-contained sentences
    - **Tags**:
      - `aRT` → broad research topic
      - `aTa` → subtopics
      - `aTy` → paper type (review, experimental, etc.)
      - `aMe` → methods
      - `ai score-N` → relevance score (0–3)
    - **Relevance Score (0–3)**:
      - 0 = marginal relevance
      - 1 = low relevance
      - 2 = moderate relevance
      - 3 = highly relevant

    ⚠️ Relevance is heuristic. Always validate manually.
    """)

elif section == "Paste Citation Mode":
    st.header("📋 Paste Citation Mode")
    st.markdown("""
    Paste citations or Google Scholar text. Gemini extracts:
    - Title
    - Authors
    - Year
    - DOI (if present)

    ⚠️ Known issues:
    - **Nothing extracted** → Try one citation per line
    - **Wrong authors** → Affiliations mistaken for names
    - **Year missing** → Citation may omit year
    - **Merged citations** → Ensure clean copy-paste
    """)

elif section == "URL / PDF Lookup":
    st.header("🔗 URL / PDF Lookup")
    st.markdown("""
    Use this when you only have a link or PDF.

    ✅ Works best with:
    - DOI links
    - Publisher landing pages
    - Open-access PDFs

    ⚠️ Common problems:
    - **“Not a PDF”** → Server mislabels file
    - **No text extracted** → PDF is scanned/image-only
    - **Redirects** → Publisher requires login
    - **Paywalls** → Metadata unavailable
    """)

elif section == "Disclaimers & Limitations":
    st.header("⚠️ Disclaimers & Limitations")
    st.markdown("""
    - AI abstracts may contain inaccuracies.
    - Relevance scoring is **advisory only**.
    - PDF parsing often fails for scanned documents.
    - Google fallback search is heuristic and noisy.
    - Not all papers have DOIs, metadata, or abstracts.
    - Zotero rejects incomplete metadata.
    - Some APIs enforce strict **rate limits** (1 request/sec).
    """)

elif section == "Text Parsing Issues":
    st.header("🔎 Text Parsing Issues")
    st.markdown("""
    Parsing citations is error-prone.

    **Possible issues:**
    - Authors list truncated or misformatted
    - Journal names mistaken for authors
    - Year misread from volume/issue numbers
    - DOIs hidden inside text

    **Fixes:**
    - Clean citation manually before pasting
    - Try using Keyword Search first
    - If DOI available, use DOI Lookup
    """)

elif section == "PDF Parsing Issues":
    st.header("📄 PDF Parsing Issues")
    st.markdown("""
    **PDF text extraction** is limited:
    - Only first ~5000–8000 characters used
    - Scanned PDFs return empty text
    - Equations and tables often lost
    - Metadata (title/authors) guessed heuristically

    **Best practice:**
    - Use DOI whenever possible
    - Treat PDF parsing as **last resort**
    """)

elif section == "PubMed & Semantic Scholar":
    st.header("📡 PubMed & Semantic Scholar")
    st.markdown("""
    - **PubMed** → best for biomedical and life sciences
    - **Semantic Scholar** → broader, especially computer science

    **Limitations:**
    - PubMed truncates long queries
    - Semantic Scholar enforces **1 request/sec**
    - Some papers missing abstracts or DOIs
    - Metadata may differ between APIs

    👉 Always cross-check with publisher pages.
    """)

elif section == "API Errors":
    st.header("⚠️ API Errors")
    st.markdown("""
    **Semantic Scholar**
    - “429 Too Many Requests” → Exceeded 1 request/sec
    - Fix: add delay or retry later

    **PubMed**
    - “ESearch failed” → Timeout
    - “Query too long” → Truncated at 300 chars
    - Missing abstracts → Not all entries provide them

    **Crossref**
    - DOI not found → Some publishers don’t register metadata
    """)

elif section == "Zotero Integration":
    st.header("📥 Zotero Integration")
    st.markdown("""
    ### Setup
    - Generate [Zotero API Key](https://www.zotero.org/settings/keys)
    - Find **User ID** in Zotero account
    - Find **Collection ID** by right-clicking collection → Edit

    ### Rules
    - Only saves papers with score ≥ threshold
    - Includes title, authors, abstract, tags, URL
    - Duplicate check by Title + DOI

    ⚠️ Zotero rejects empty fields → metadata must be complete
    """)

elif section == "Duplicates & Metadata":
    st.header("📑 Duplicates & Metadata")
    st.markdown("""
    - **Duplicates** detected by Title + DOI
    - Zotero duplicate check may miss some
    - Crossref enrichment improves metadata
    - Incomplete metadata may prevent Zotero save
    """)

elif section == "Performance & Limits":
    st.header("⚡ Performance & Limits")
    st.markdown("""
    - Semantic Scholar: 1 request/sec
    - PubMed: ~3 requests/sec safe
    - Timeouts: 30–45 seconds
    - Large PDFs trimmed to first ~8000 chars
    - Progress bar may appear stuck → refresh app
    """)

elif section == "Institutional Access & Proxies":
    st.header("🏫 Institutional Access & Proxies")
    st.markdown("""
    - NTU proxy links auto-generated for DOI/URL
    - Requires NTU login to access paywalled content
    - If outside NTU → proxy links won’t work
    - Open-access PDFs bypass login
    """)

elif section == "Secrets & Configuration":
    st.header("🔑 Secrets & Configuration")
    st.markdown("""
    Store sensitive keys in `.streamlit/secrets.toml`:

    ```toml
    SEMANTIC_SCHOLAR_API_KEY = "your_key"
    GEMINI_API_KEY = "your_gemini_key"
    NCBI_EMAIL = "your_email"
    NCBI_API_KEY = "your_ncbi_key"
    ZOTERO_API_KEY = "your_zotero_key"
    ZOTERO_USER_ID = "your_user_id"
    ZOTERO_COLLECTION_ID = "your_collection_id"
    ```

    ⚠️ Ensure valid TOML syntax:
    - Keys = values with quotes
    - No stray characters after closing quote
    """)

elif section == "Tips & Best Practices":
    st.header("💡 Tips & Best Practices")
    st.markdown("""
    - Start with PubMed/Semantic Scholar
    - Keep queries short
    - Use Boolean operators for precision
    - Paste one citation per line
    - Validate AI abstracts with originals
    - Save to Zotero after verifying metadata
    """)

elif section == "FAQs":
    st.header("❓ Frequently Asked Questions")
    st.markdown("""
    **Q: Can I trust AI abstracts?**  
    A: They’re summaries only. Always verify.

    **Q: Why are scores off?**  
    A: Relevance is heuristic. Use as guide only.

    **Q: Does it cover all fields?**  
    A: Strongest in biomedical, CS, natural sciences.

    **Q: Can I export to BibTeX/EndNote?**  
    A: Yes, via Zotero exports.
    """)

elif section == "Troubleshooting Checklist":
    st.header("🛠️ Troubleshooting Checklist")
    st.markdown("""
    - ✅ Tried PubMed/Semantic Scholar first?
    - ✅ Query short and precise?
    - ✅ One citation per line?
    - ✅ DOI pasted correctly?
    - ✅ Zotero keys valid?
    - ✅ Not exceeding API limits?
    - ✅ Checked if PDF is scanned?
    """)

elif section == "Ask Gemini":
    st.header("🤖 Ask Gemini")
    st.markdown("""
    Still need help? Ask **Google Gemini** directly:  
    👉 [**Ask Gemini**](https://gemini.google.com/)
    """)

elif section == "Contact":
    st.header("📬 Contact & Feedback")
    st.markdown("""
    Have questions, suggestions, or bugs?

    - Open GitHub issue: [ai_lit_agent](https://github.com/y-kuzn/ai_lit_agent/issues)
    - Email: `kuzn0001@e.ntu.edu.sg`

    ---
    Made with ❤️ using Streamlit + Gemini
    """)
