# help.py — Hierarchical Help Page for AI Literature Helper
import streamlit as st

# Page setup
st.set_page_config(page_title="AI Literature Helper – Help", page_icon="🆘", layout="wide")

# ---------- Reusable Gemini button ----------
def ask_gemini_button():
    st.markdown("""
    <div style="text-align: center; margin-top: 20px; margin-bottom: 20px;">
        <a href="https://gemini.google.com/" target="_blank">
            <button style="
                background-color: #4CAF50;
                color: white;
                padding: 12px 24px;
                border: none;
                border-radius: 8px;
                font-size: 16px;
                cursor: pointer;
                box-shadow: 0px 4px 6px rgba(0,0,0,0.2);
            ">
                🤖 Ask Gemini for More Help
            </button>
        </a>
    </div>
    """, unsafe_allow_html=True)

# Sidebar navigation — categories first
st.sidebar.title("📘 Help Categories")
category = st.sidebar.selectbox("Choose a category:", [
    "General",
    "Using the App",
    "Data Sources",
    "AI Features",
    "Errors & Troubleshooting",
    "Integration",
    "Technical Setup",
    "Tips & Best Practices",
    "Contact"
])

# ===========================
# General
# ===========================
if category == "General":
    point = st.selectbox("Select a help point:", [
        "Overview",
        "Recommended Workflow",
        "Disclaimers & Limitations",
        "FAQs"
    ])

    if point == "Overview":
        st.title("🆘 Overview")
        st.markdown("""
        **AI Literature Helper** is a Streamlit app that combines PubMed, Semantic Scholar, Crossref, 
        and Gemini AI to assist with your literature review and reference management.
        """)
        ask_gemini_button()

    elif point == "Recommended Workflow":
        st.header("✅ Recommended Workflow")
        st.markdown("""
        1. Start with **Keyword Search** (PubMed/Semantic Scholar).  
        2. If not found, try **Paste Citation** mode.  
        3. As a **last resort**, use **URL/DOI/PDF lookup**.  

        👉 PubMed & Semantic Scholar are the most reliable.  
        👉 Parsing text/PDFs is less reliable.
        """)
        ask_gemini_button()

    elif point == "Disclaimers & Limitations":
        st.header("⚠️ Disclaimers & Limitations")
        st.markdown("""
        - AI abstracts may be inaccurate.  
        - PDF parsing often fails for scanned files.  
        - Zotero requires complete metadata.  
        - APIs enforce rate limits (Semantic Scholar = 1 request/sec).  
        """)
        ask_gemini_button()

    elif point == "FAQs":
        st.header("❓ Frequently Asked Questions")
        st.markdown("""
        **Q: Can I trust AI summaries?** → Validate with the original paper.  
        **Q: Why are scores inconsistent?** → They’re heuristic, not absolute.  
        **Q: Can I export to BibTeX?** → Yes, via Zotero.  
        **Q: Does it cover all fields?** → Strongest in biomedical, CS, natural sciences.  
        """)
        ask_gemini_button()

# ===========================
# Using the App
# ===========================
elif category == "Using the App":
    point = st.selectbox("Select a help point:", [
        "How to Use",
        "Boolean Queries",
        "Paste Citation Mode",
        "URL / PDF Lookup"
    ])

    if point == "How to Use":
        st.header("🚀 How to Use")
        st.markdown("""
        1. Choose a mode (Keyword, Paste Citation, or URL/DOI/PDF).  
        2. Adjust **Max Results** & **Relevance Threshold**.  
        3. (Optional) Add Zotero credentials.  
        4. Click **🚀 Go** to start.  
        """)
        ask_gemini_button()

    elif point == "Boolean Queries":
        st.header("🔤 Boolean Queries")
        st.markdown("""
        - Use **AND / OR / NOT** for precision.  
        - PubMed truncates queries >300 chars.  
        - Example: `"CRISPR" AND "prime editing" NOT "review"`.  
        """)
        ask_gemini_button()

    elif point == "Paste Citation Mode":
        st.header("📋 Paste Citation Mode")
        st.markdown("""
        - Paste references or Google Scholar text.  
        - Extracts Title, Authors, Year, DOI.  

        ⚠️ Issues:  
        - Wrong authors (affiliations misparsed).  
        - Missing year.  
        - Multiple citations merged.  
        """)
        ask_gemini_button()

    elif point == "URL / PDF Lookup":
        st.header("🔗 URL / PDF Lookup")
        st.markdown("""
        ✅ Works with DOIs, landing pages, open PDFs.  

        ⚠️ Issues:  
        - “Not a PDF” → mislabelled file.  
        - Empty text → scanned PDF.  
        - Redirects → login/paywall needed.  
        """)
        ask_gemini_button()

# ===========================
# Data Sources
# ===========================
elif category == "Data Sources":
    point = st.selectbox("Select a help point:", [
        "PubMed",
        "Semantic Scholar",
        "Crossref",
        "Google Fallback"
    ])

    if point == "PubMed":
        st.header("🧬 PubMed")
        st.markdown("""
        - Best for biomedical sciences.  
        - Limits: 300-char queries, missing abstracts.  
        """)
        ask_gemini_button()

    elif point == "Semantic Scholar":
        st.header("📡 Semantic Scholar")
        st.markdown("""
        - Covers many fields (esp. CS).  
        - Rate limit: 1 request/sec.  
        - Metadata sometimes incomplete.  
        """)
        ask_gemini_button()

    elif point == "Crossref":
        st.header("🔎 Crossref")
        st.markdown("""
        - Enriches metadata using DOIs.  
        - Not all publishers register DOIs.  
        """)
        ask_gemini_button()

    elif point == "Google Fallback":
        st.header("🌐 Google Fallback")
        st.markdown("""
        - Used if PubMed/S2 fail.  
        - May return irrelevant matches.  
        """)
        ask_gemini_button()

# ===========================
# AI Features
# ===========================
elif category == "AI Features":
    point = st.selectbox("Select a help point:", [
        "AI Annotations",
        "Relevance Scores",
        "Tags"
    ])

    if point == "AI Annotations":
        st.header("📝 AI Annotations")
        st.markdown("""
        AI generates 10–15 sentence abstracts.  
        ⚠️ Treat them as summaries, not substitutes.  
        """)
        ask_gemini_button()

    elif point == "Relevance Scores":
        st.header("⭐ Relevance Scores")
        st.markdown("""
        Scores (0–3):  
        - 0 = marginal  
        - 1 = low  
        - 2 = moderate  
        - 3 = highly relevant  
        """)
        ask_gemini_button()

    elif point == "Tags":
        st.header("🏷️ Tags")
        st.markdown("""
        - `aRT` → broad topic  
        - `aTa` → subtopics  
        - `aTy` → paper type  
        - `aMe` → methods  
        - `ai score-N` → relevance  
        """)
        ask_gemini_button()

# ===========================
# Errors & Troubleshooting
# ===========================
elif category == "Errors & Troubleshooting":
    point = st.selectbox("Select a help point:", [
        "API Errors",
        "Text Parsing Issues",
        "PDF Parsing Issues",
        "Performance & Limits"
    ])

    if point == "API Errors":
        st.header("⚠️ API Errors")
        st.markdown("""
        - Semantic Scholar → 429 Too Many Requests.  
        - PubMed → query too long / missing abstracts.  
        """)
        ask_gemini_button()

    elif point == "Text Parsing Issues":
        st.header("🔎 Text Parsing Issues")
        st.markdown("""
        - Wrong authors parsed.  
        - Year misread.  
        - DOI hidden in text.  
        """)
        ask_gemini_button()

    elif point == "PDF Parsing Issues":
        st.header("📄 PDF Parsing Issues")
        st.markdown("""
        - Only first 5000–8000 chars extracted.  
        - Scanned PDFs return empty.  
        """)
        ask_gemini_button()

    elif point == "Performance & Limits":
        st.header("⚡ Performance & Limits")
        st.markdown("""
        - Semantic Scholar: 1 req/sec.  
        - PubMed: ~3 req/sec.  
        - Large PDFs trimmed.  
        """)
        ask_gemini_button()

# ===========================
# Integration
# ===========================
elif category == "Integration":
    point = st.selectbox("Select a help point:", [
        "Zotero",
        "Duplicates & Metadata",
        "Institutional Access"
    ])

    if point == "Zotero":
        st.header("📥 Zotero Integration")
        st.markdown("""
        - Needs API key, User ID, Collection ID.  
        - Saves only relevant papers.  
        - Duplicate check: Title + DOI.  
        """)
        ask_gemini_button()

    elif point == "Duplicates & Metadata":
        st.header("📑 Duplicates & Metadata")
        st.markdown("""
        - Zotero rejects incomplete metadata.  
        - Crossref enrichment improves accuracy.  
        """)
        ask_gemini_button()

    elif point == "Institutional Access":
        st.header("🏫 Institutional Access")
        st.markdown("""
        - NTU proxy links auto-generated.  
        - Requires NTU login.  
        """)
        ask_gemini_button()

# ===========================
# Technical Setup
# ===========================
elif category == "Technical Setup":
    point = st.selectbox("Select a help point:", [
        "Secrets & Configuration",
        "Requirements.txt",
        "Deployment"
    ])

    if point == "Secrets & Configuration":
        st.header("🔑 Secrets & Configuration")
        st.markdown("""
        `.streamlit/secrets.toml`:

        ```toml
        SEMANTIC_SCHOLAR_API_KEY = "key"
        GEMINI_API_KEY = "key"
        NCBI_EMAIL = "you@email.com"
        NCBI_API_KEY = "key"
        ZOTERO_API_KEY = "key"
        ZOTERO_USER_ID = "id"
        ZOTERO_COLLECTION_ID = "id"
        ```
        """)
        ask_gemini_button()

    elif point == "Requirements.txt":
        st.header("📦 requirements.txt")
        st.markdown("""
        Required packages:
        - streamlit
        - requests
        - pyzotero
        - pymupdf
        - google-genai
        """)
        ask_gemini_button()

    elif point == "Deployment":
        st.header("🚀 Deployment")
        st.markdown("""
        - Works on Streamlit Cloud.  
        - Ensure secrets are valid TOML.  
        - Pin dependency versions in requirements.txt.  
        """)
        ask_gemini_button()

# ===========================
# Tips & Best Practices
# ===========================
elif category == "Tips & Best Practices":
    st.header("💡 Tips & Best Practices")
    st.markdown("""
    - Start with PubMed/Semantic Scholar.  
    - Keep queries short.  
    - Use Boolean operators.  
    - Paste one citation per line.  
    - Always validate AI abstracts.  
    """)
    ask_gemini_button()

# ===========================
# Contact
# ===========================
elif category == "Contact":
    st.header("📬 Contact & Feedback")
    st.markdown("""
    - GitHub Issues: [ai_lit_agent](https://github.com/y-kuzn/ai_lit_agent/issues)  
    - Email: `kuzn0001@e.ntu.edu.sg`  

    Made with ❤️ using Streamlit + Gemini
    """)
    ask_gemini_button()
