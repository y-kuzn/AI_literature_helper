# help.py — Comprehensive Help Page for AI Literature Helper
import streamlit as st
import smtplib
from email.mime.text import MIMEText

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

# ---------- Sidebar navigation ----------
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
    "Feedback",
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
        **AI Literature Helper** combines PubMed, Semantic Scholar, Crossref, and Gemini AI  
        to streamline literature search, annotation, and reference management.
        """)
        ask_gemini_button()

    elif point == "Recommended Workflow":
        st.header("✅ Recommended Workflow")
        st.markdown("""
        - Start with **Keyword Search** (PubMed/Semantic Scholar).  
        - If not found → try **Paste Citation Mode**.  
        - As a **last resort** → use **URL / DOI / PDF Lookup**.  

        👉 PubMed & Semantic Scholar are most reliable.  
        👉 Parsing text/PDFs is less reliable.  
        """)
        ask_gemini_button()

    elif point == "Disclaimers & Limitations":
        st.header("⚠️ Disclaimers & Limitations")
        st.markdown("""
        - AI abstracts may contain inaccuracies.  
        - PDF parsing often fails for scanned files.  
        - Zotero requires complete metadata.  
        - APIs enforce rate limits (S2 = 1 request/sec).  
        """)
        ask_gemini_button()

    elif point == "FAQs":
        st.header("❓ FAQs")
        st.markdown("""
        **Q: Can I trust AI summaries?** → Verify with the original paper.  
        **Q: Why are scores inconsistent?** → They’re heuristic, not absolute.  
        **Q: Can I export to BibTeX?** → Yes, via Zotero.  
        **Q: Which fields are covered?** → Strongest in biomedical, CS, natural sciences.  
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
        - PubMed truncates queries >300 characters.  
        - Example: `"CRISPR" AND "prime editing" NOT "review"`.  
        """)
        ask_gemini_button()

    elif point == "Paste Citation Mode":
        st.header("📋 Paste Citation Mode")
        st.markdown("""
        Paste citations or Google Scholar text → extracts:  
        - Title  
        - Authors  
        - Year  
        - DOI (if present)  

        ⚠️ Known issues:  
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
        - “Not a PDF” → server mislabeled file.  
        - Empty text → scanned PDFs not supported.  
        - Redirects → login/paywall required.  
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
        - Best for biomedical/life sciences.  
        - Limitations: 300-char queries, missing abstracts.  
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
        - Enriches metadata from DOIs.  
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
        AI generates **10–15 sentence abstracts**.  
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
        - PubMed → query too long, missing abstracts.  
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
        - Scanned PDFs → empty output.  
        """)
        ask_gemini_button()

    elif point == "Performance & Limits":
        st.header("⚡ Performance & Limits")
        st.markdown("""
        - Semantic Scholar: 1 req/sec.  
        - PubMed: ~3 req/sec safe.  
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
        - Saves only papers above relevance threshold.  
        - Duplicate check: Title + DOI.  
        """)
        ask_gemini_button()

    elif point == "Duplicates & Metadata":
        st.header("📑 Duplicates & Metadata")
        st.markdown("""
        - Zotero rejects incomplete metadata.  
        - Crossref enrichment helps fill gaps.  
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
        `.streamlit/secrets.toml` example:

        ```toml
        SMTP_SERVER = "smtp.gmail.com"
        SMTP_PORT = 465
        SMTP_USER = "your_gmail@gmail.com"
        SMTP_PASSWORD = "your_app_password"

        SEMANTIC_SCHOLAR_API_KEY = "your_key"
        GEMINI_API_KEY = "your_key"
        NCBI_EMAIL = "your@email"
        NCBI_API_KEY = "your_key"
        ZOTERO_API_KEY = "your_key"
        ZOTERO_USER_ID = "your_id"
        ZOTERO_COLLECTION_ID = "your_collection_id"
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
        - Pin dependency versions.  
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
    - Always verify AI abstracts.  
    - Cross-check metadata before Zotero save.  
    """)
    ask_gemini_button()

# ===========================
# Feedback Form
# ===========================
elif category == "Feedback":
    st.header("📬 Feedback Form")
    st.markdown("Have suggestions, bug reports, or ideas? Fill the form below:")

    with st.form("feedback_form"):
        name = st.text_input("Your Name (optional)")
        email = st.text_input("Your Email (so we can reply)")
        message = st.text_area("Your Feedback", height=200)
        submitted = st.form_submit_button("Send Feedback")

    if submitted:
        if not email.strip() or "@" not in email:
            st.error("⚠️ Please provide a valid email so we can reply to you.")
        elif not message.strip():
            st.error("⚠️ Please enter a message before submitting.")
        else:
            try:
                # Load SMTP secrets
                smtp_server = st.secrets["SMTP_SERVER"]
                smtp_port = st.secrets["SMTP_PORT"]
                smtp_user = st.secrets["SMTP_USER"]
                smtp_password = st.secrets["SMTP_PASSWORD"]

                # Build email
                body = f"""
Feedback from AI Literature Helper

Name: {name or "Anonymous"}
Email: {email}

Message:
{message}
                """
                msg = MIMEText(body)
                msg["Subject"] = "AI Literature Helper – New Feedback"
                msg["From"] = smtp_user
                msg["To"] = "kuzn0001@e.ntu.edu.sg"
                msg["Reply-To"] = email  # lets you click Reply in inbox

                # Send email
                with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
                    server.login(smtp_user, smtp_password)
                    server.sendmail(smtp_user, ["kuzn0001@e.ntu.edu.sg"], msg.as_string())

                st.success("✅ Thank you! Your feedback has been sent.")
            except Exception as e:
                st.error(f"❌ Failed to send feedback: {e}")

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
