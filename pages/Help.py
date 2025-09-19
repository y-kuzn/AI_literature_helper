# help.py — Comprehensive Help & FAQ for AI Literature Helper

import streamlit as st

st.set_page_config(page_title="ℹ️ Help — AI Literature Helper", page_icon="ℹ️")

st.title("ℹ️ Help & FAQ — AI Literature Helper")

st.markdown("""
Welcome to **AI Literature Helper** 👋  
This page provides detailed instructions, FAQs, and troubleshooting tips.

---

## 🔍 Modes of Use

### 1. Keyword Search
- Enter keywords or research questions.
- AI can generate Boolean queries (editable).
- Sources: **Semantic Scholar**, **PubMed**, or **Both**.

### 2. Paste Citation / Page Text
- Paste references or text from Google Scholar.
- AI extracts Title, Authors, Year, DOI.
- Automatic enrichment: **DOI → Semantic Scholar → PubMed → Google fallback**.

### 3. Lookup by URL / PDF / DOI
- Paste a DOI, article URL, or PDF link.
- Tool detects PDFs (header, extension, or magic number `%PDF`).
- Extracts metadata and text for annotation.

---

## 🧪 What AI Provides
- **Abstract (AI)**: 10–15 sentence summary.
- **Tags**:
  - `aRT` — broad research topic  
  - `aTa` — specific subtopics  
  - `aTy` — paper type  
  - `aMe` — methods  
  - `ai score-N` — relevance score (0–3)  
- **Relevance Score (0–3)**: heuristic filter.

---

## 📥 Zotero Integration
- Enter API Key, User ID, Collection ID in the sidebar.
- Papers above chosen relevance threshold are added.
- Duplicate detection via Title + DOI.
- Can allow duplicates if needed.

---

## ⚠️ Common Issues & Fixes

**General**
- Nothing found → Shorten your query, check spelling, try another source.
- Progress bar stuck → Refresh app, retry with fewer results.
- Timeouts → Reduce “Max results” or wait (API rate limits).

**Semantic Scholar**
- “Semantic Scholar failed” → API rate limit (1 request/second). Retry.
- Incomplete metadata → Some papers lack abstracts/DOIs.

**PubMed**
- “ESearch/ESummary failed” → Timeout. Retry with shorter query.
- Abstract missing → Some PubMed entries don’t include abstracts.
- Query too long → PubMed truncates after 300 characters.

**Paste Citation**
- “😅 Nothing extracted” → Paste one citation per line or cleaner references.
- Wrong author parsing → AI sometimes confuses editors/affiliations.

**PDF / URL Lookup**
- “Not a PDF” → Server didn’t send proper headers. If it starts with `%PDF`, it should still parse.
- Incomplete extraction → Scanned/image PDFs may not yield text.
- Broken URL → Ensure the link is publicly accessible.

**Zotero**
- “Zotero initialization error” → Check API key and User ID.
- Duplicate detection failed → Best-effort only; clean up manually if needed.
- Export skipped → Score below threshold or duplicate detected.

---

## 🤔 FAQs

**Q: Can I trust AI abstracts?**  
A: They are summaries. Always check the original paper.

**Q: Why does the AI relevance score seem off?**  
A: It’s heuristic, not absolute. Use as a filter.

**Q: Does it cover all fields?**  
A: PubMed (biomedical) + Semantic Scholar (broad science). Some domains may have weaker coverage.

**Q: Can I prioritize my own topics/authors?**  
A: Yes, add them in sidebar preferences. They influence AI scoring.

**Q: Can I export to formats other than Zotero?**  
A: Not directly. Export to Zotero, then use its export functions.

---

## 💡 Tips
- Keep queries short and focused.
- Edit Boolean queries before PubMed search.
- Paste clean citations (one per line).
- Start with small result sets, then increase.

---

## 🤖 Ask Gemini
Still stuck? You can chat directly with Google’s Gemini here:  
👉 [**Ask Gemini**](https://gemini.google.com/)

---
""")
