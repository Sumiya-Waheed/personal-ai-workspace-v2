"""Shared visual system and reusable UI helpers."""
from __future__ import annotations
import streamlit as st

CSS = r"""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap');
:root { --ink:#182230; --muted:#667085; --line:#e7eaf0; --accent:#5b5bd6; --accent2:#7c5cff; --surface:#ffffff; --soft:#f6f7fb; --success:#16855b; --warning:#b7791f; }
html, body, [class*="css"] { font-family:'DM Sans', sans-serif; }
.block-container { max-width:1280px; padding-top:1.4rem; padding-bottom:3rem; }
h1,h2,h3 { font-family:'Space Grotesk', sans-serif; letter-spacing:-.025em; color:var(--ink); }
[data-testid="stSidebar"] { border-right:1px solid var(--line); }
[data-testid="stSidebar"] > div:first-child { padding-top:1.25rem; }
.hero { border:1px solid rgba(91,91,214,.16); border-radius:24px; padding:1.8rem 2rem; background:linear-gradient(135deg,#f4f3ff 0%,#ffffff 58%,#f3f8ff 100%); margin-bottom:1.2rem; }
.hero-kicker { color:var(--accent); font-weight:700; font-size:.78rem; text-transform:uppercase; letter-spacing:.12em; }
.hero h1 { font-size:2.25rem; margin:.35rem 0 .35rem; }
.hero p { color:var(--muted); margin:0; max-width:760px; font-size:1.02rem; }
.card { background:var(--surface); border:1px solid var(--line); border-radius:18px; padding:1.1rem 1.15rem; box-shadow:0 8px 30px rgba(16,24,40,.045); height:100%; }
.card h3 { margin:.2rem 0 .35rem; font-size:1.05rem; }
.card p { color:var(--muted); margin:0; font-size:.92rem; }
.metric-card { background:#fff; border:1px solid var(--line); border-radius:18px; padding:1rem 1.1rem; }
.metric-value { font-family:'Space Grotesk'; font-size:1.8rem; font-weight:700; color:var(--ink); }
.metric-label { color:var(--muted); font-size:.82rem; }
.pill { display:inline-block; border-radius:999px; padding:.28rem .62rem; font-size:.76rem; font-weight:700; background:#eef0ff; color:#4b4bb8; margin:.1rem .2rem .1rem 0; }
.section-label { font-size:.76rem; text-transform:uppercase; letter-spacing:.12em; font-weight:700; color:#7b8494; margin:1.35rem 0 .55rem; }
.feature-card { min-height:150px; }
.feature-icon { font-size:1.55rem; }
.evidence { border-left:3px solid var(--accent); padding:.7rem .85rem; background:#fafaff; border-radius:0 12px 12px 0; margin:.45rem 0; }
.login-wrap { max-width:760px; margin:5vh auto 0; }
.login-panel { border:1px solid var(--line); border-radius:28px; padding:2.4rem; background:linear-gradient(145deg,#ffffff,#f7f7ff); box-shadow:0 20px 60px rgba(31,35,70,.08); text-align:center; }
.small-muted { color:var(--muted); font-size:.88rem; }
.status-ok { color:var(--success); font-weight:700; }
</style>
"""


def inject():
    st.markdown(CSS, unsafe_allow_html=True)


def hero(kicker: str, title: str, description: str):
    st.markdown(f'''<div class="hero"><div class="hero-kicker">{kicker}</div><h1>{title}</h1><p>{description}</p></div>''', unsafe_allow_html=True)


def card(icon: str, title: str, description: str):
    st.markdown(f'''<div class="card feature-card"><div class="feature-icon">{icon}</div><h3>{title}</h3><p>{description}</p></div>''', unsafe_allow_html=True)


def metric(label: str, value: str):
    st.markdown(f'''<div class="metric-card"><div class="metric-value">{value}</div><div class="metric-label">{label}</div></div>''', unsafe_allow_html=True)
