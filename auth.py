"""Safe, optional OIDC authentication wrapper for Streamlit."""
from __future__ import annotations
import streamlit as st


def auth_configured() -> bool:
    try:
        auth = st.secrets.get("auth")
        return bool(auth and auth.get("client_id") and auth.get("client_secret") and auth.get("redirect_uri"))
    except Exception:
        return False


def is_logged_in() -> bool:
    if not auth_configured():
        return False
    return bool(getattr(st.user, "is_logged_in", False))


def user_name() -> str:
    try:
        return str(getattr(st.user, "name", None) or getattr(st.user, "email", None) or "User")
    except Exception:
        return "User"


def user_email() -> str:
    try:
        return str(getattr(st.user, "email", "") or "")
    except Exception:
        return ""


def require_login() -> bool:
    """Return True when the app may continue; fail safe into preview mode if auth is not configured."""
    if not auth_configured():
        return True
    return is_logged_in()
