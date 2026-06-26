# 🔧 GrantMatch AI – Technical Guide

## Overview

This document provides technical information for developers who want to understand, maintain, or extend GrantMatch AI.

The application recommends grant opportunities for nonprofit organizations using semantic search and generates AI-powered explanations for each recommendation.

---

# Technology Stack

| Technology            | Purpose                                  |
| --------------------- | ---------------------------------------- |
| Python                | Core programming language                |
| Streamlit             | Web application framework                |
| Sentence Transformers | Generate sentence embeddings             |
| Cosine Similarity     | Rank grants based on semantic similarity |
| Google Gemini API     | Generate AI explanations                 |
| SQLite                | Store grant information and embeddings   |
| Pandas                | Data processing                          |
| NumPy                 | Numerical operations                     |
| PyPDF                 | Extract text from uploaded PDFs          |
| ReportLab             | Generate downloadable PDF reports        |

---

# System Architecture

```
User
   │
   ▼
Upload PDF / Enter Mission
   │
   ▼
PDF Text Extraction
   │
   ▼
Mission Validation
   │
   ▼
Grant Filtering
   │
   ▼
Sentence Transformer
   │
   ▼
Mission Embedding
   │
   ▼
Cosine Similarity
   │
   ▼
Rank Matching Grants
   │
   ▼
Google Gemini API
   │
   ▼
AI Explanation
   │
   ▼
Display Results
   │
   ▼
Generate PDF Report
```

---

# Project Workflow

1. User uploads a mission statement or enters it manually.
2. The application extracts text from the PDF (if uploaded).
3. The mission statement is validated.
4. Selected filters are applied.
5. The mission statement is converted into a sentence embedding.
6. Precomputed grant embeddings are loaded.
7. Cosine similarity is calculated between the mission embedding and each grant embedding.
8. Grants are ranked by similarity score.
9. Google Gemini generates an explanation for the recommended grants.
10. Results are displayed and can be exported as a PDF.

---

# AI Components

## Semantic Search

The recommendation engine uses:

* Sentence Transformers
* Dense vector embeddings
* Cosine similarity

This enables the application to recommend grants based on semantic meaning rather than exact keyword matches.

---

## Google Gemini

Gemini is **not** responsible for selecting grants.

It is used only to generate natural-language explanations describing why a recommended grant aligns with the nonprofit's mission.

---

# Updating the Grant Database

When adding new grant records:

1. Insert the grant information into the SQLite database.
2. Generate sentence embeddings for the new grants.
3. Store the embeddings.
4. Restart the application.

---

# Environment Variables

The application requires the following environment variable:

```
GOOGLE_API_KEY
```

Store the API key securely using Streamlit Secrets or environment variables.

Do not hardcode API keys in the source code.

---

# Common Issues

### No recommendations returned

* Check the selected filters.
* Verify that grant data exists.
* Ensure the mission statement contains meaningful content.

---

### AI explanation not generated

* Verify the Gemini API key.
* Check internet connectivity.
* Confirm API quota has not been exceeded.

---

### PDF text extraction fails

* Ensure the uploaded file contains selectable text.
* Scanned PDFs may require OCR before upload.

---

# Future Improvements

Possible enhancements include:

* User authentication
* Vector database integration (FAISS or ChromaDB)
* Multi-document support
* Advanced grant filtering
* Admin dashboard
* Automated grant database updates

---

# Maintenance Notes

GrantMatch AI is designed with modular components so that the user interface, semantic search pipeline, AI explanation module, and reporting functionality can be updated independently without affecting the overall workflow.
