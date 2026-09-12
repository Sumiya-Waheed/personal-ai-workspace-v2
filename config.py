
"""Application configuration and secrets."""
from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv

# Load local .env when running locally.
# On Streamlit Cloud, secrets are still read separately through st.secrets.
load_dotenv()


APP_NAME = "Personal AI Application Assistant"

MODEL_NAME = os.getenv("GROQ_MODEL", "openai/gpt-oss-120b")
EMBEDDING_MODEL = os.getenv(
    "EMBEDDING_MODEL",
    "sentence-transformers/all-MiniLM-L6-v2",
)

CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "900"))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "120"))
TOP_K = int(os.getenv("TOP_K", "6"))
MAX_UPLOAD_MB = int(os.getenv("MAX_UPLOAD_MB", "15"))

ROOT_DIR = Path(__file__).resolve().parent


def get_groq_api_key() -> str | None:
    """Read the API key from Streamlit secrets first, then the environment."""

    # Streamlit Cloud / Streamlit secrets
    try:
        import streamlit as st

        value = st.secrets.get("GROQ_API_KEY")
        if value:
            return str(value)
    except Exception:
        pass

    # Local .env / environment variable
    return os.getenv("GROQ_API_KEY")


def require_groq_api_key() -> str:
    """Return the Groq API key or raise a helpful configuration error."""

    key = get_groq_api_key()

    if not key:
        raise RuntimeError(
            "GROQ_API_KEY is not configured. Add it to .env locally or "
            "Streamlit Cloud → App Settings → Secrets."
        )

    return key