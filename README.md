# AI literature helper

**AI Literature Helper** is a Streamlit-based research assistant that integrates **Semantic Scholar**, **PubMed**, **Crossref**, and a **Google fallback** with **Gemini AI** to streamline literature discovery, annotation, and organization.  

It generates AI-powered **abstracts**, structured **tags**, and **relevance scores**, and supports seamless **Zotero export** with duplicate detection.

---

## ✨ Features

- 🔍 **Keyword Search**  
  Search PubMed, Semantic Scholar, or both, with optional AI-optimized Boolean queries (editable before search).  

- 📋 **Paste citations / text**  
  Paste citations or Google Scholar result text → AI extracts Title, Authors, Year, DOI.  
  Enrichment follows: DOI → Semantic Scholar → PubMed → Google fallback.  

- 🔗 **URL / PDF Lookup**  
  Paste a DOI, article URL, or PDF link. Crossref metadata and PDF text are extracted for annotation.  

- 🤖 **AI annotations**  
  - AI-generated abstract (10–15 sentences)  
  - Tags:  
    - `aRT` – broad research topic  
    - `aTa` – specific topical tags  
    - `aTy` – paper type  
    - `aMe` – methods  
    - `ai score-N` – relevance score (0–3)  
  - Unified across all modes  

- 📥 **Zotero integration**  
  - Add articles above your chosen relevance threshold  
  - Duplicate detection by title/DOI  
  - Proxy link support for institutional access  

- 📊 **Usability**  
  - Progress bar + live status updates  
  - Comprehensive in-app **Help page** (usage, errors, FAQs, troubleshooting)  

---

## 🚀 Getting Started

### Prerequisites
- Python 3.9+
- API keys:
  - [Semantic Scholar](https://api.semanticscholar.org/)
  - [Google Gemini](https://ai.google.dev/)
  - (Optional) [NCBI PubMed](https://www.ncbi.nlm.nih.gov/books/NBK25497/)
- (Optional) [Zotero API key](https://www.zotero.org/settings/keys)

### Installation

```bash
git clone https://github.com/your-username/ai-literature-helper.git
cd ai-literature-helper
pip install -r requirements.txt
