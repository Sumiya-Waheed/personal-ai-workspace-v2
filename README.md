# Personal AI Workspace

An evidence-grounded Streamlit workspace for **career, learning, and research**.

The original Personal AI Application Assistant has been expanded into a modular V2 with:

- Career intelligence: profile, opportunity analysis, matching, application assistant, tailored resume
- Study Assistant: document Q&A, flashcards, MCQs, important questions, smart notes, summaries, study plans
- Research Assistant: paper analysis, literature review, paper comparison, research gaps, methodology analysis, research questions, key findings
- Universal document extraction for PDF, DOCX, TXT
- Scanned/image-based PDF detection with optional RapidOCR fallback
- Modern responsive visual design
- Optional Google login through Streamlit's native OIDC authentication
- Groq-powered generation with evidence-grounding and anti-hallucination rules
- FAISS + Sentence Transformers retrieval

## Core principle

> Upload your information once → retrieve relevant evidence → generate grounded assistance.

The application must never invent personal achievements, education, jobs, projects, certifications, metrics, or other personal claims.

## Project structure

```text
app.py
config.py
auth.py
requirements.txt
README.md
.env.example
.gitignore
.streamlit/config.toml

candidate_profile/
  __init__.py
  profile_manager.py

features/
  application_assistant.py
  evidence.py
  readiness_score.py
  resume_generator.py

llm/
  generator.py
  groq_client.py
  prompts.py

opportunity/
  analyzer.py
  matcher.py

rag/
  embeddings.py
  retriever.py
  vector_store.py

study/
  assistant.py

research/
  assistant.py

ui/
  theme.py
  dashboard.py
  profile_page.py
  opportunity_page.py
  match_page.py
  assistant_page.py
  resume_page.py
  study_page.py
  research_page.py

utils/
  file_parser.py
  text_processor.py
  validators.py

tests/
  ...
```

## Local setup on Windows

Open PowerShell in the project root.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

If PowerShell blocks activation, run the project with the Python executable directly:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m streamlit run app.py
```

Create a local `.env` from `.env.example` and add your Groq key. Never commit `.env`.

## Groq configuration

### Local

```text
GROQ_API_KEY=your_real_key
```

### Streamlit Cloud

Add the same key under the app's **Secrets** settings. Do not put the real key in GitHub.

## Google login

The application uses Streamlit's native OpenID Connect authentication. It is deliberately implemented as a fail-safe feature: if OIDC secrets are absent, the app can run in preview mode; once the `[auth]` secrets are configured, login is required.

### 1. Create a Google OAuth web client

In Google Cloud Console, create/select a project and configure Google Auth Platform. Create a **Web application** client.

For local development, add this authorized redirect URI:

```text
http://localhost:8501/oauth2callback
```

For Streamlit Cloud, use your actual deployed app URL:

```text
https://YOUR-APP-NAME.streamlit.app/oauth2callback
```

### 2. Streamlit secrets

Do NOT create or commit `.streamlit/secrets.toml` with real credentials.

Use this structure in Streamlit Cloud Secrets:

```toml
GROQ_API_KEY = "your_real_groq_key"

[auth]
redirect_uri = "https://YOUR-APP-NAME.streamlit.app/oauth2callback"
cookie_secret = "generate-a-long-random-secret"
client_id = "your-google-client-id"
client_secret = "your-google-client-secret"
server_metadata_url = "https://accounts.google.com/.well-known/openid-configuration"
```

For local development, use the same `[auth]` block but change `redirect_uri` to:

```text
http://localhost:8501/oauth2callback
```

### 3. Test login

Start locally:

```powershell
streamlit run app.py
```

Click **Continue with Google**, complete authentication, and confirm the sidebar shows the signed-in user.

### 4. Important security rule

Never commit:

- `client_secret`
- `cookie_secret`
- `GROQ_API_KEY`
- `.streamlit/secrets.toml`
- `.env`
- personal documents
- private vector databases

## Document intelligence

The parser now uses a two-stage strategy for PDFs:

1. Extract normal PDF text with PyMuPDF.
2. Detect pages with very little text but image content.
3. Run RapidOCR only when OCR is needed.
4. Preserve page markers such as `[Page 7]` in the extracted text.

DOCX extraction also preserves table content. TXT files are decoded as UTF-8 with replacement for malformed bytes.

The OCR runtime is intentionally imported lazily so a normal text PDF does not initialize OCR unnecessarily.

## RAG architecture

```text
Documents
   ↓
Universal extraction / OCR
   ↓
Cleaning
   ↓
Chunking
   ↓
Sentence Transformers
   ↓
FAISS
   ↓
Retriever
   ↓
Relevant evidence
   ↓
Grounded prompt
   ↓
Groq
   ↓
Answer + evidence
```

The profile vector store contains only the user's profile documents during the current session. Opportunity content is kept separate.

## Study Assistant

Modes included:

- Document Q&A
- Flashcards
- MCQ Lab
- Important Questions
- Smart Notes
- Summary
- Study Plan

Each mode uses the uploaded study material as its source of truth.

## Research Assistant

Modes included:

- Paper Analyzer
- Literature Review
- Compare Papers
- Research Gaps
- Methodology Analysis
- Research Questions
- Key Findings

Claims about papers are grounded in the uploaded material. New research directions are explicitly presented as suggestions.

## Career workflow

1. Upload profile documents.
2. Build the personal knowledge base.
3. Upload an opportunity.
4. Analyze explicit opportunity requirements.
5. Run profile ↔ opportunity matching.
6. Review readiness, matches, gaps and unclear requirements.
7. Generate grounded application answers.
8. Tailor a resume without fabricating personal claims.

## Testing and verification

Compile all Python files:

```powershell
python -m compileall -q .
```

Run tests:

```powershell
pytest -q
```

The most important deployment checks are:

- all imports resolve after `pip install -r requirements.txt`
- `streamlit run app.py` starts without an import error
- Groq secret is available
- login secrets are valid if authentication is enabled
- normal PDFs work
- scanned PDFs trigger OCR instead of silently returning an empty document
- DOCX and TXT work
- profile retrieval works
- opportunity analysis works
- matching and readiness work
- Study and Research work

## Streamlit Cloud deployment

1. Push the project to GitHub.
2. Open Streamlit Community Cloud.
3. Create/open the app for your GitHub repository.
4. Select branch `main`.
5. Select `app.py` as the entrypoint.
6. Deploy.
7. Open **Settings / Secrets**.
8. Add `GROQ_API_KEY`.
9. Add the `[auth]` block if you want Google login enabled.
10. Save secrets and reboot/redeploy the app.
11. Open the deployed URL and test Google login.
12. Return to Google Cloud Console and make sure the exact deployed `/oauth2callback` URI is an authorized redirect URI.

After every code update:

```powershell
git add .
git commit -m "Upgrade Personal AI Workspace"
git push
```

Streamlit Cloud will detect the GitHub update and rebuild the app.

## Troubleshooting

### `ModuleNotFoundError` for a package

Make sure the package is in `requirements.txt`, then redeploy. Do not install packages only on your local computer and expect Streamlit Cloud to have them.

### `GROQ_API_KEY` missing

Add it to Streamlit Cloud Secrets exactly as:

```text
GROQ_API_KEY = "..."
```

### Google login redirect error

The redirect URI in Google Cloud must exactly match the Streamlit secret, including:

```text
/oauth2callback
```

### Scanned PDF cannot be read

Confirm `rapidocr-onnxruntime` installed successfully during deployment. The app will show a friendly OCR error instead of silently indexing an empty document.

### Old code appears after GitHub push

Check that the latest commit is on `main`, then use Streamlit Cloud's reboot/redeploy control.

## Privacy

This application handles personal documents. Use only documents you are comfortable processing through the configured services. Do not upload passwords, API keys, payment-card information, or credentials. The hackathon architecture intentionally keeps the current profile knowledge base in session memory instead of introducing an unnecessary persistent database.
