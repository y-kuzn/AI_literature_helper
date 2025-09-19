# help.py — Hierarchical Help Page for AI Literature Helper
# Category-based navigation + detailed sections with Ask Gemini link

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

# --------------------------
# Back button to main app
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
        **AI Literature Helper** is a Streamlit app that combines PubMed, Semantic Scholar, Crossref, and Gemini AI to assist your literature review.

        Key Features:
        - Keyword Search (PubMed & Semantic Scholar)
        - Paste citation / text parsing
        - DOI, URL, PDF metadata lookup
        - AI abstracts, tags, relevance scoring
        - Zotero export
        """)
    elif point == "Recommended Workflow":
        st.header("✅ Recommended Workflow")
        st.markdown("""
        For **best reliability**:
        1. Start with **Keyword Search** (PubMed / Semantic Scholar).
        2. If paper not found → try **Paste Citation**.
        3. As a **last resort** → use **URL / DOI / PDF Lookup**.

        👉 PubMed & Semantic Scholar are **preferred**.
        👉 Parsing text and PDFs is less reliable and may fail.
        """)
    elif point == "Disclaimers & Limitations":
        st.header("⚠️ Disclaimers & Limitations")
        st.markdown("""
        - AI abstracts may contain inaccuracies — always check the paper.
        - PDF parsing often fails for scanned documents.
        - Google fallback search may give irrelevant results.
        - Zotero rejects incomplete metadata.
        - APIs enforce rate limits (Semantic Scholar = 1 request/sec).
        """)
    elif point == "FAQs":
        st.header("❓ FAQs")
        st.markdown("""
        **Q: Can I trust AI summaries?**  
        A: They are approximate. Always validate.

        **Q: Why are scores inconsistent?**  
        A: Relevance is heuristic. Use it as guidance only.

        **Q: Can I export BibTeX?**  
        A: Yes, via Zotero after import.

        **Q: Does it cover all disciplines?**  
        A: Strongest for biomedical, CS, natural sciences.
        """)

if point == "Overview":
    st.title("🆘 Overview")
    st.markdown("""
    **AI Literature Helper** combines PubMed, Semantic Scholar, Crossref, and Gemini AI
    to help you with literature search, annotation, and Zotero export.
    """)
    ask_gemini_button()   # <--- button shows here

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
        1. Pick a mode:
           - Keyword Search
           - Paste Citation / Text
           - URL / DOI / PDF
        2. Adjust **Max Results** & **Relevance Threshold**.
        3. (Optional) Add Zotero credentials.
        4. Click **🚀 Go**.
        """)
    elif point == "Boolean Queries":
        st.header("🔤 Boolean Queries")
        st.markdown("""
        - Use AND / OR / NOT for precision.
        - PubMed truncates queries >300 characters.
        - Example: `"CRISPR" AND "prime editing" NOT "review"`
        """)
    elif point == "Paste Citation Mode":
        st.header("📋 Paste Citation Mode")
        st.markdown("""
        Paste references or Google Scholar text. Extracts:
        - Title
        - Authors
        - Year
        - DOI (if present)

        ⚠️ Issues:
        - Wrong authors (affiliations misparsed)
        - Missing years
        - Multiple citations merged
        """)
    elif point == "URL / PDF Lookup":
        st.header("🔗 URL / PDF Lookup")
        st.markdown("""
        ✅ Works best with:
        - DOI links
        - Open-access PDFs

        ⚠️ Issues:
        - “Not a PDF” → mislabelled file
        - Empty text → scanned PDF
        - Redirects → paywalls/institutional login
        """)

if point == "Overview":
    st.title("🆘 Overview")
    st.markdown("""
    **AI Literature Helper** combines PubMed, Semantic Scholar, Crossref, and Gemini AI
    to help you with literature search, annotation, and Zotero export.
    """)
    ask_gemini_button()   # <--- button shows here

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
        - Best for biomedical/life sciences.
        - Limits: 300-char queries, missing abstracts.
        """)
    elif point == "Semantic Scholar":
        st.header("📡 Semantic Scholar")
        st.markdown("""
        - Covers CS, natural sciences.
        - Rate limit: 1 request/sec.
        - Some metadata missing.
        """)
    elif point == "Crossref":
        st.header("🔎 Crossref")
        st.markdown("""
        - Enriches metadata from DOIs.
        - Not all publishers register DOIs.
        """)
    elif point == "Google Fallback":
        st.header("🌐 Google Fallback")
        st.markdown("""
        - Last-resort title lookup.
        - Can return irrelevant matches.
        """)

if point == "Overview":
    st.title("🆘 Overview")
    st.markdown("""
    **AI Literature Helper** combines PubMed, Semantic Scholar, Crossref, and Gemini AI
    to help you with literature search, annotation, and Zotero export.
    """)
    ask_gemini_button()   # <--- button shows here

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
        AI generates 10–15 sentence abstracts per paper.  
        ⚠️ Treat as summaries, not substitutes.
        """)
    elif point == "Relevance Scores":
        st.header("⭐ Relevance Scores")
        st.markdown("""
        Scores (0–3):  
        - 0 = marginal  
        - 1 = low  
        - 2 = moderate  
        - 3 = highly relevant
        """)
    elif point == "Tags":
        st.header("🏷️ Tags")
        st.markdown("""
        - `aRT` → broad topic  
        - `aTa` → subtopics  
        - `aTy` → paper type  
        - `aMe` → methods  
        - `ai score-N` → relevance
        """)

if point == "Overview":
    st.title("🆘 Overview")
    st.markdown("""
    **AI Literature Helper** combines PubMed, Semantic Scholar, Crossref, and Gemini AI
    to help you with literature search, annotation, and Zotero export.
    """)
    ask_gemini_button()   # <--- button shows here

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
        - Semantic Scholar → 429 Too Many Requests
        - PubMed → query too long, missing abstracts
        """)
    elif point == "Text Parsing Issues":
        st.header("🔎 Text Parsing Issues")
        st.markdown("""
        - Wrong authors
        - Year misread
        - DOI hidden
        """)
    elif point == "PDF Parsing Issues":
        st.header("📄 PDF Parsing Issues")
        st.markdown("""
        - Only first 5000–8000 chars extracted
        - Scanned PDFs → empty
        """)
    elif point == "Performance & Limits":
        st.header("⚡ Performance & Limits")
        st.markdown("""
        - Rate limits: S2 = 1/sec, PubMed strict
        - Large PDFs trimmed
        """)

if point == "Overview":
    st.title("🆘 Overview")
    st.markdown("""
    **AI Literature Helper** combines PubMed, Semantic Scholar, Crossref, and Gemini AI
    to help you with literature search, annotation, and Zotero export.
    """)
    ask_gemini_button()   # <--- button shows here

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
        - Needs API key, User ID, Collection ID
        - Exports only relevant papers
        - Duplicate check by Title + DOI
        """)
    elif point == "Duplicates & Metadata":
        st.header("📑 Duplicates & Metadata")
        st.markdown("""
        - Zotero rejects incomplete metadata
        - Crossref enrichment helps
        """)
    elif point == "Institutional Access":
        st.header("🏫 Institutional Access & Proxies")
        st.markdown("""
        - NTU proxy links generated automatically
        - Requires NTU login
        """)

if point == "Overview":
    st.title("🆘 Overview")
    st.markdown("""
    **AI Literature Helper** combines PubMed, Semantic Scholar, Crossref, and Gemini AI
    to help you with literature search, annotation, and Zotero export.
    """)
    ask_gemini_button()   # <--- button shows here

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
        `.streamlit/secrets.toml` example:

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
    elif point == "Requirements.txt":
        st.header("📦 requirements.txt")
        st.markdown("""
        Must include:
        - streamlit
        - requests
        - pyzotero
        - pymupdf
        - google-genai
        """)
    elif point == "Deployment":
        st.header("🚀 Deployment")
        st.markdown("""
        - Works on Streamlit Cloud
        - Check secrets syntax
        - Ensure dependencies pinned
        """)

if point == "Overview":
    st.title("🆘 Overview")
    st.markdown("""
    **AI Literature Helper** combines PubMed, Semantic Scholar, Crossref, and Gemini AI
    to help you with literature search, annotation, and Zotero export.
    """)
    ask_gemini_button()   # <--- button shows here

# ===========================
# Tips & Best Practices
# ===========================
elif category == "Tips & Best Practices":
    st.header("💡 Tips & Best Practices")
    st.markdown("""
    - Always start with PubMed/Semantic Scholar
    - Keep queries short
    - Use Boolean operators
    - Paste one citation per line
    - Validate AI abstracts with originals
    - Cross-check metadata before Zotero save
    """)
if point == "Overview":
    st.title("🆘 Overview")
    st.markdown("""
    **AI Literature Helper** combines PubMed, Semantic Scholar, Crossref, and Gemini AI
    to help you with literature search, annotation, and Zotero export.
    """)
    ask_gemini_button()   # <--- button shows here

# ===========================
# Contact
# ===========================
elif category == "Contact":
    st.header("📬 Contact & Feedback")
    st.markdown("""
    - Open issue: [GitHub](https://github.com/y-kuzn/ai_lit_agent/issues)  
    - Email: `kuzn0001@e.ntu.edu.sg`
    """)
    st.markdown("---")
    st.markdown("Made with ❤️ using Streamlit + Gemini")
if point == "Overview":
    st.title("🆘 Overview")
    st.markdown("""
    **AI Literature Helper** combines PubMed, Semantic Scholar, Crossref, and Gemini AI
    to help you with literature search, annotation, and Zotero export.
    """)
    ask_gemini_button()   # <--- button shows here
