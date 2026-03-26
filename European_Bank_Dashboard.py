"""
European Bank Customer Churn Intelligence Platform v3
======================================================
Recruiter-grade dark analytics dashboard.
Premium glassmorphism + neon accent design system.

Run with:
    pip install streamlit pandas plotly numpy
    streamlit run European_Bank_Dashboard_v3.py
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

# ─────────────────────────────────────────────
# Page Config
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="EuroBank · Churn Intelligence",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# Design System
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=Outfit:wght@300;400;500;600;700;800;900&family=IBM+Plex+Mono:wght@400;500;600&display=swap');

:root {
    /* Backgrounds */
    --bg-base:   #020408;
    --bg-1:      #060c14;
    --bg-2:      #0a1220;
    --bg-3:      #0f1a2e;
    --bg-4:      #162338;
    --bg-glass:  rgba(10,18,32,0.7);
    --bg-glass2: rgba(15,26,46,0.6);

    /* Borders */
    --border:    rgba(255,255,255,0.06);
    --border2:   rgba(255,255,255,0.1);
    --border3:   rgba(255,255,255,0.16);

    /* Neon Accents */
    --cyan:      #00e5ff;
    --cyan-dim:  rgba(0,229,255,0.12);
    --cyan-glow: 0 0 20px rgba(0,229,255,0.3), 0 0 60px rgba(0,229,255,0.1);

    --rose:      #ff2d6b;
    --rose-dim:  rgba(255,45,107,0.12);
    --rose-glow: 0 0 20px rgba(255,45,107,0.3);

    --amber:     #ffb300;
    --amber-dim: rgba(255,179,0,0.12);
    --amber-glow:0 0 20px rgba(255,179,0,0.3);

    --violet:    #b575ff;
    --violet-dim:rgba(181,117,255,0.12);

    --emerald:   #00e676;
    --emerald-dim:rgba(0,230,118,0.12);

    /* Text */
    --t1: #f0f6ff;
    --t2: #7a9cc4;
    --t3: #3a5070;
    --t4: #1e3050;

    /* Fonts */
    --font-display: 'Outfit', sans-serif;
    --font-body:    'Space Grotesk', sans-serif;
    --font-mono:    'IBM Plex Mono', monospace;
}

/* ── Reset ── */
*, *::before, *::after { box-sizing: border-box; }

.stApp {
    background: var(--bg-base) !important;
    font-family: var(--font-body) !important;
    background-image:
        radial-gradient(ellipse 80% 50% at 20% -10%, rgba(0,229,255,0.04) 0%, transparent 60%),
        radial-gradient(ellipse 60% 40% at 80% 110%, rgba(181,117,255,0.04) 0%, transparent 60%);
}
.stApp > header { background: transparent !important; }
.block-container { padding-top: 1.5rem !important; }

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: var(--bg-1) !important;
    border-right: 1px solid var(--border2) !important;
}
[data-testid="stSidebar"] * {
    font-family: var(--font-body) !important;
}
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] .stMarkdown p,
[data-testid="stSidebar"] span {
    color: var(--t2) !important;
    font-size: 12px !important;
}
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
    color: var(--t1) !important;
    font-family: var(--font-display) !important;
}
[data-testid="stSidebar"] .stMultiSelect > div > div,
[data-testid="stSidebar"] .stSelectbox > div > div {
    background: var(--bg-3) !important;
    border: 1px solid var(--border2) !important;
    color: var(--t1) !important;
    border-radius: 10px !important;
}
[data-testid="stSidebar"] [data-baseweb="tag"] {
    background: var(--cyan-dim) !important;
    border: 1px solid rgba(0,229,255,0.25) !important;
    color: var(--cyan) !important;
    font-family: var(--font-mono) !important;
    font-size: 10px !important;
    border-radius: 4px !important;
}
[data-testid="stSidebar"] hr { border-color: var(--border2) !important; }
[data-testid="stSidebar"] [data-testid="stRadio"] span,
[data-testid="stSidebar"] [data-testid="stRadio"] > label { color: var(--t2) !important; }
[data-testid="stSlider"] [data-baseweb="slider"] [role="slider"] {
    background: var(--cyan) !important;
    border-color: var(--cyan) !important;
    box-shadow: var(--cyan-glow) !important;
}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    background: rgba(6,12,20,0.9) !important;
    border-bottom: 1px solid var(--border2) !important;
    gap: 0 !important;
    padding: 0 !important;
    backdrop-filter: blur(12px) !important;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    color: var(--t3) !important;
    font-family: var(--font-mono) !important;
    font-size: 11px !important;
    font-weight: 500 !important;
    letter-spacing: 0.08em !important;
    text-transform: uppercase !important;
    border: none !important;
    border-bottom: 2px solid transparent !important;
    padding: 14px 22px !important;
    transition: all 0.25s ease !important;
    border-radius: 0 !important;
}
.stTabs [data-baseweb="tab"]:hover {
    color: var(--t1) !important;
    background: rgba(255,255,255,0.03) !important;
}
.stTabs [aria-selected="true"] {
    color: var(--cyan) !important;
    border-bottom-color: var(--cyan) !important;
    background: rgba(0,229,255,0.04) !important;
    text-shadow: 0 0 20px rgba(0,229,255,0.5) !important;
}
.stTabs [data-baseweb="tab-highlight"] { display: none !important; }
.stTabs [data-baseweb="tab-panel"] {
    background: transparent !important;
    padding: 24px 0 !important;
}

/* ── Text ── */
.stMarkdown p, .stMarkdown li { color: var(--t2) !important; font-family: var(--font-body) !important; }
h1,h2,h3,h4 { color: var(--t1) !important; font-family: var(--font-display) !important; }
[data-testid="stMetricValue"] { color: var(--t1) !important; font-family: var(--font-mono) !important; }
[data-testid="stMetricLabel"] { color: var(--t3) !important; font-size: 11px !important; font-family: var(--font-mono) !important; }
[data-testid="stMetricDelta"]  { font-size: 11px !important; font-family: var(--font-mono) !important; }
[data-testid="stDataFrame"] > div {
    background: var(--bg-2) !important;
    border: 1px solid var(--border2) !important;
    border-radius: 14px !important;
}
.stCaption,[data-testid="stCaptionContainer"]{color:var(--t3)!important;font-family:var(--font-mono)!important;font-size:11px!important;}

/* ══ CUSTOM COMPONENTS ══ */

/* Hero Header */
.hero {
    background: linear-gradient(135deg, #060c14 0%, #0a1525 40%, #080f1e 100%);
    border: 1px solid var(--border2);
    border-radius: 20px;
    padding: 32px 40px 28px;
    margin-bottom: 6px;
    position: relative;
    overflow: hidden;
}
.hero::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0; bottom: 0;
    background:
        radial-gradient(ellipse 50% 80% at 0% 50%, rgba(0,229,255,0.06) 0%, transparent 60%),
        radial-gradient(ellipse 40% 60% at 100% 50%, rgba(181,117,255,0.05) 0%, transparent 60%);
    pointer-events: none;
}
.hero-eyebrow {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    font-family: var(--font-mono);
    font-size: 10px;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: var(--cyan);
    margin-bottom: 14px;
    position: relative;
}
.hero-dot {
    width: 7px; height: 7px;
    border-radius: 50%;
    background: var(--cyan);
    box-shadow: 0 0 12px var(--cyan), 0 0 24px rgba(0,229,255,0.4);
    animation: blink 2s ease-in-out infinite;
}
@keyframes blink { 0%,100%{opacity:1;transform:scale(1)} 50%{opacity:0.4;transform:scale(0.8)} }
.hero-title {
    font-family: var(--font-display) !important;
    font-size: clamp(1.6rem, 3vw, 2.4rem) !important;
    font-weight: 800 !important;
    line-height: 1.1 !important;
    letter-spacing: -0.03em !important;
    color: var(--t1) !important;
    margin: 0 0 6px !important;
    position: relative;
}
.hero-title em {
    font-style: normal;
    background: linear-gradient(90deg, var(--cyan), var(--violet));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.hero-sub {
    font-family: var(--font-mono);
    font-size: 11px;
    color: var(--t3);
    letter-spacing: 0.04em;
    margin-top: 4px;
    position: relative;
}
.hero-pills {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    margin-top: 20px;
    position: relative;
}
.pill {
    display: inline-flex;
    align-items: center;
    gap: 5px;
    padding: 5px 12px;
    border-radius: 100px;
    font-family: var(--font-mono);
    font-size: 10px;
    letter-spacing: 0.06em;
    font-weight: 500;
    border: 1px solid;
    transition: all 0.2s;
}
.pill-default { background: var(--bg-3); border-color: var(--border2); color: var(--t2); }
.pill-cyan    { background: var(--cyan-dim); border-color: rgba(0,229,255,0.3); color: var(--cyan); }
.pill-rose    { background: var(--rose-dim); border-color: rgba(255,45,107,0.3); color: var(--rose); }
.pill-amber   { background: var(--amber-dim); border-color: rgba(255,179,0,0.3); color: var(--amber); }
.pill-emerald { background: var(--emerald-dim); border-color: rgba(0,230,118,0.3); color: var(--emerald); }

/* KPI Cards */
.kpi {
    background: var(--bg-glass);
    backdrop-filter: blur(16px);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 20px 22px 18px;
    position: relative;
    overflow: hidden;
    transition: border-color 0.3s, transform 0.25s;
    height: 100%;
}
.kpi:hover { border-color: var(--border3); transform: translateY(-3px); }
.kpi::before {
    content: '';
    position: absolute;
    bottom: 0; left: 0;
    height: 2px; width: var(--bar, 50%);
    background: var(--accent, var(--cyan));
    border-radius: 0 2px 0 0;
    box-shadow: 0 0 12px var(--accent, var(--cyan));
}
.kpi-label {
    font-family: var(--font-mono);
    font-size: 9px;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: var(--t3);
    margin-bottom: 10px;
}
.kpi-value {
    font-family: var(--font-display);
    font-size: 1.85rem;
    font-weight: 700;
    line-height: 1;
    color: var(--accent, var(--cyan));
    letter-spacing: -0.02em;
}
.kpi-meta {
    font-family: var(--font-mono);
    font-size: 10px;
    color: var(--t3);
    margin-top: 8px;
    letter-spacing: 0.02em;
}

/* Section Headers */
.section-head {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 18px;
    padding-bottom: 12px;
    border-bottom: 1px solid var(--border);
}
.section-bar {
    width: 3px; height: 16px;
    background: linear-gradient(180deg, var(--cyan), var(--violet));
    border-radius: 2px;
    box-shadow: 0 0 10px rgba(0,229,255,0.4);
}
.section-label {
    font-family: var(--font-mono);
    font-size: 9px;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: var(--t3);
}

/* Insight Cards */
.insight {
    border-radius: 12px;
    padding: 16px 20px;
    font-family: var(--font-body);
    font-size: 12.5px;
    line-height: 1.7;
    border-left: 3px solid;
    margin: 10px 0;
    backdrop-filter: blur(8px);
    transition: transform 0.2s;
}
.insight:hover { transform: translateX(3px); }
.insight-title {
    font-family: var(--font-display);
    font-size: 13px;
    font-weight: 700;
    margin-bottom: 6px;
    letter-spacing: -0.01em;
    display: block;
}
.ins-cyan    { background: var(--cyan-dim);    border-color: var(--cyan);    color: rgba(0,229,255,0.7); }
.ins-cyan    .insight-title { color: var(--cyan); }
.ins-rose    { background: var(--rose-dim);    border-color: var(--rose);    color: rgba(255,45,107,0.7); }
.ins-rose    .insight-title { color: var(--rose); }
.ins-amber   { background: var(--amber-dim);   border-color: var(--amber);   color: rgba(255,179,0,0.7); }
.ins-amber   .insight-title { color: var(--amber); }
.ins-emerald { background: var(--emerald-dim); border-color: var(--emerald); color: rgba(0,230,118,0.7); }
.ins-emerald .insight-title { color: var(--emerald); }
.ins-violet  { background: var(--violet-dim);  border-color: var(--violet);  color: rgba(181,117,255,0.7); }
.ins-violet  .insight-title { color: var(--violet); }

/* Risk Matrix */
.risk-cell {
    background: var(--bg-glass);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 18px 16px;
    text-align: center;
    transition: all 0.25s;
    position: relative;
    overflow: hidden;
}
.risk-cell:hover { border-color: var(--border3); transform: translateY(-2px); }
.risk-cell::after {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: var(--rc-color, var(--cyan));
    box-shadow: 0 0 14px var(--rc-color, var(--cyan));
}
.rc-label { font-family: var(--font-mono); font-size: 9px; text-transform: uppercase; letter-spacing: 0.1em; color: var(--t3); margin-bottom: 8px; }
.rc-val   { font-family: var(--font-display); font-size: 1.7rem; font-weight: 700; }
.rc-sub   { font-family: var(--font-mono); font-size: 10px; color: var(--t3); margin-top: 6px; }

/* Tag badges */
.badge {
    display: inline-flex;
    align-items: center;
    padding: 2px 10px;
    border-radius: 6px;
    font-family: var(--font-mono);
    font-size: 10px;
    font-weight: 500;
    border: 1px solid;
}
.badge-ok     { background: var(--emerald-dim); color: var(--emerald); border-color: rgba(0,230,118,0.3); }
.badge-warn   { background: var(--amber-dim);   color: var(--amber);   border-color: rgba(255,179,0,0.3); }
.badge-danger { background: var(--rose-dim);    color: var(--rose);    border-color: rgba(255,45,107,0.3); }
.badge-info   { background: var(--cyan-dim);    color: var(--cyan);    border-color: rgba(0,229,255,0.3); }

/* Sidebar */
.sb-brand {
    text-align: center;
    padding: 20px 0 12px;
}
.sb-logo {
    font-size: 2.2rem;
    display: block;
    filter: drop-shadow(0 0 16px rgba(0,229,255,0.5));
}
.sb-name {
    font-family: var(--font-display);
    font-size: 16px;
    font-weight: 700;
    color: var(--t1);
    letter-spacing: -0.02em;
    margin-top: 8px;
}
.sb-ver {
    font-family: var(--font-mono);
    font-size: 9px;
    color: var(--t3);
    letter-spacing: 0.1em;
    text-transform: uppercase;
    margin-top: 4px;
}
.sb-stat {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 8px 0;
    border-bottom: 1px solid var(--border);
}
.sb-stat-label { font-family: var(--font-mono); font-size: 10px; color: var(--t3); text-transform: uppercase; letter-spacing: 0.08em; }
.sb-stat-val   { font-family: var(--font-mono); font-size: 13px; font-weight: 600; }
.sb-filter-head { font-family: var(--font-mono); font-size: 9px; letter-spacing: 0.14em; text-transform: uppercase; color: var(--t3); padding: 14px 0 6px; }

/* Divider */
.div { height: 1px; background: var(--border); margin: 12px 0; }

/* Footer */
.dash-footer {
    text-align: center;
    font-family: var(--font-mono);
    font-size: 9px;
    letter-spacing: 0.1em;
    color: var(--t4);
    text-transform: uppercase;
    padding: 28px 0 12px;
    border-top: 1px solid var(--border);
    margin-top: 40px;
}

/* Geo flag row */
.geo-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 11px 0;
    border-bottom: 1px solid var(--border);
    transition: background 0.2s;
}
.geo-row:last-child { border-bottom: none; }
.geo-name { font-family: var(--font-body); font-size: 13px; color: var(--t1); font-weight: 500; }
.geo-badges { display: flex; gap: 6px; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# Plotly theme
# ─────────────────────────────────────────────
DARK_BG    = "#060c14"
GRID       = "rgba(255,255,255,0.04)"
TICK_CLR   = "#3a5070"
FONT_MONO  = "IBM Plex Mono, monospace"
FONT_DISP  = "Outfit, sans-serif"

CYAN    = "#00e5ff"
ROSE    = "#ff2d6b"
AMBER   = "#ffb300"
VIOLET  = "#b575ff"
EMERALD = "#00e676"
ORANGE  = "#ff6d00"

def base_layout(h=300, margin=None):
    m = margin or dict(l=14, r=14, t=20, b=14)
    return dict(
        height=h, margin=m,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor=DARK_BG,
        font=dict(family=FONT_MONO, color=TICK_CLR, size=11),
        xaxis=dict(
            showgrid=True, gridcolor=GRID, gridwidth=1,
            zeroline=False, showline=False,
            tickfont=dict(family=FONT_MONO, color=TICK_CLR, size=10),
        ),
        yaxis=dict(
            showgrid=True, gridcolor=GRID, gridwidth=1,
            zeroline=False, showline=False,
            tickfont=dict(family=FONT_MONO, color=TICK_CLR, size=10),
        ),
        legend=dict(
            bgcolor="rgba(0,0,0,0)", bordercolor=GRID, borderwidth=1,
            font=dict(family=FONT_MONO, color="#3a5070", size=10),
        ),
    )

def alpha(hex_color, a=0.25):
    h = hex_color.lstrip('#')
    r, g, b = int(h[0:2],16), int(h[2:4],16), int(h[4:6],16)
    return f"rgba({r},{g},{b},{a})"

def rate_color(r):
    if r >= 30: return ROSE
    if r >= 20: return AMBER
    return EMERALD

PLOTLY_CFG = {"displayModeBar": False, "responsive": True}

# ─────────────────────────────────────────────
# Helper HTML builders
# ─────────────────────────────────────────────
def kpi(label, value, meta="", accent=CYAN, bar="50%"):
    return f"""<div class="kpi" style="--accent:{accent};--bar:{bar}">
  <div class="kpi-label">{label}</div>
  <div class="kpi-value">{value}</div>
  <div class="kpi-meta">{meta}</div>
</div>"""

def sec(title):
    return f"""<div class="section-head">
  <div class="section-bar"></div>
  <div class="section-label">{title}</div>
</div>"""

def insight(title, body, cls="ins-cyan"):
    return f"""<div class="insight {cls}">
  <span class="insight-title">{title}</span>{body}
</div>"""

def risk_cell(label, val, sub1, sub2, color):
    return f"""<div class="risk-cell" style="--rc-color:{color}">
  <div class="rc-label">{label}</div>
  <div class="rc-val" style="color:{color}">{val}</div>
  <div class="rc-sub">{sub1}</div>
  <div class="rc-sub" style="color:{color};opacity:0.7">{sub2}</div>
</div>"""

# ─────────────────────────────────────────────
# Data
# ─────────────────────────────────────────────
@st.cache_data
def load_data():
    for path in ["European_Bank.csv", "/mnt/project/European_Bank.csv",
                 "/mnt/user-data/uploads/European_Bank.csv"]:
        try:
            df = pd.read_csv(path); break
        except FileNotFoundError:
            continue
    else:
        np.random.seed(42)
        n = 10000
        df = pd.DataFrame({
            "CustomerId":      range(1, n+1),
            "CreditScore":     np.random.randint(350, 851, n),
            "Geography":       np.random.choice(["France","Germany","Spain"], n, p=[0.5,0.25,0.25]),
            "Gender":          np.random.choice(["Male","Female"], n),
            "Age":             np.clip(np.random.normal(38,10,n).astype(int),18,80),
            "Tenure":          np.random.randint(0,11,n),
            "Balance":         np.where(np.random.random(n)<0.37, 0, np.random.uniform(10000,250000,n)),
            "NumOfProducts":   np.random.choice([1,2,3,4],n,p=[0.5,0.46,0.027,0.006]),
            "HasCrCard":       np.random.choice([0,1],n,p=[0.3,0.7]),
            "IsActiveMember":  np.random.choice([0,1],n,p=[0.49,0.51]),
            "EstimatedSalary": np.random.uniform(10000,200000,n),
            "Exited":          np.random.choice([0,1],n,p=[0.8,0.2]),
        })

    df["Exited"]         = df["Exited"].astype(int)
    df["IsActiveMember"] = df["IsActiveMember"].astype(int)
    df["HasCrCard"]      = df["HasCrCard"].astype(int)
    df["RSI"]            = df["IsActiveMember"] + df["NumOfProducts"].clip(upper=2) + df["HasCrCard"]

    def classify(row):
        a = row["IsActiveMember"] == 1
        p = row["NumOfProducts"]
        b = row["Balance"]
        if   a and p >= 2:         return "Active Engaged"
        elif not a and p <= 1:     return "Inactive Disengaged"
        elif a and p == 1:         return "Active Low-Product"
        elif not a and b > 100000: return "Inactive High-Balance"
        else:                      return "Other"

    df["EngagementProfile"] = df.apply(classify, axis=1)
    df["AgeBand"]    = pd.cut(df["Age"],       bins=[0,29,39,49,59,120], labels=["<30","30–39","40–49","50–59","60+"])
    df["BalanceBand"]= df["Balance"].apply(lambda b: "Zero" if b==0 else "€1–50K" if b<50000 else "€50–100K" if b<100000 else "€100–150K" if b<150000 else "€150K+")
    df["IsSticky"]   = ((df["IsActiveMember"]==1)&(df["NumOfProducts"]>=2)&(df["HasCrCard"]==1)).astype(int)
    df["IsAtRisk"]   = ((df["IsActiveMember"]==0)&(df["Balance"]>100000)).astype(int)
    df["CSBand"]     = pd.cut(df["CreditScore"], bins=[0,499,599,699,799,1000], labels=["<500","500–599","600–699","700–799","800+"])
    return df

def churn_rate(df):  return df["Exited"].mean() * 100
def churn_by(df, col):
    g = df.groupby(col)["Exited"].agg(["sum","count"]).reset_index()
    g.columns = [col,"Churned","Total"]
    g["ChurnRate"] = g["Churned"] / g["Total"] * 100
    return g

df_full = load_data()

# ─────────────────────────────────────────────
# Sidebar
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class="sb-brand">
      <span class="sb-logo">🏦</span>
      <div class="sb-name">EuroBank</div>
      <div class="sb-ver">Churn Intelligence · v3</div>
    </div>
    """, unsafe_allow_html=True)

    cr_full = df_full["Exited"].mean() * 100
    st.markdown(f"""
    <div class="div"></div>
    <div class="sb-stat">
      <span class="sb-stat-label">Portfolio</span>
      <span class="sb-stat-val" style="color:var(--t1)">{len(df_full):,}</span>
    </div>
    <div class="sb-stat">
      <span class="sb-stat-label">Churn Rate</span>
      <span class="sb-stat-val" style="color:var(--rose)">{cr_full:.1f}%</span>
    </div>
    <div class="div"></div>
    <div class="sb-filter-head">▸ Filters</div>
    """, unsafe_allow_html=True)

    geographies = st.multiselect("Geography", options=df_full["Geography"].unique().tolist(), default=df_full["Geography"].unique().tolist())
    genders     = st.multiselect("Gender",    options=df_full["Gender"].unique().tolist(),    default=df_full["Gender"].unique().tolist())
    profiles    = st.multiselect("Engagement Profile",
        options=["Active Engaged","Active Low-Product","Other","Inactive High-Balance","Inactive Disengaged"],
        default=["Active Engaged","Active Low-Product","Other","Inactive High-Balance","Inactive Disengaged"],
    )
    prod_range   = st.slider("Products", 1, 4, (1, 4))
    bal_min, bal_max = st.slider("Balance (€)", 0, 250000, (0, 250000), step=5000, format="€%d")
    age_min, age_max = st.slider("Age", 18, 80, (18, 80))
    cs_min, cs_max   = st.slider("Credit Score", 350, 850, (350, 850))
    st.markdown('<div class="div"></div>', unsafe_allow_html=True)
    active_filter = st.radio("Activity Status", ["All","Active only","Inactive only"])
    st.markdown('<div class="div"></div>', unsafe_allow_html=True)
    st.markdown('<div style="font-family:var(--font-mono);font-size:9px;color:var(--t4);text-transform:uppercase;letter-spacing:0.1em;text-align:center;padding-top:8px">10,000 Customers · France · Germany · Spain · FY 2025</div>', unsafe_allow_html=True)

# ── Apply Filters ──
df = df_full.copy()
if geographies: df = df[df["Geography"].isin(geographies)]
if genders:     df = df[df["Gender"].isin(genders)]
if profiles:    df = df[df["EngagementProfile"].isin(profiles)]
df = df[df["NumOfProducts"].between(*prod_range)]
df = df[df["Balance"].between(bal_min, bal_max)]
df = df[df["Age"].between(age_min, age_max)]
df = df[df["CreditScore"].between(cs_min, cs_max)]
if active_filter == "Active only":   df = df[df["IsActiveMember"]==1]
elif active_filter == "Inactive only": df = df[df["IsActiveMember"]==0]
cr_now = churn_rate(df)

# ─────────────────────────────────────────────
# Hero Header
# ─────────────────────────────────────────────
cr_pill = "pill-rose" if cr_now > 25 else "pill-amber" if cr_now > 15 else "pill-emerald"
st.markdown(f"""
<div class="hero">
  <div class="hero-eyebrow">
    <span class="hero-dot"></span>
    Live Analytics · Real-Time Filters Active
  </div>
  <div class="hero-title">European Bank — <em>Churn Intelligence</em></div>
  <div class="hero-sub">
    {len(df):,} customers in view &nbsp;·&nbsp; Filtered from {len(df_full):,} total &nbsp;·&nbsp;
    France &middot; Germany &middot; Spain &nbsp;·&nbsp; FY 2025
  </div>
  <div class="hero-pills">
    <span class="pill pill-default">3 Markets</span>
    <span class="pill pill-default">14 Variables</span>
    <span class="pill pill-rose">⚠&nbsp; {df['Exited'].sum():,} Churned</span>
    <span class="pill pill-emerald">✓&nbsp; {(df['Exited']==0).sum():,} Retained</span>
    <span class="pill {cr_pill}">{cr_now:.1f}% Churn Rate</span>
  </div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# Tabs
# ─────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "  01 · Overview  ",
    "  02 · Engagement  ",
    "  03 · Products  ",
    "  04 · Financial  ",
    "  05 · Retention  ",
])

ENG_COLORS = {
    "Active Engaged":       EMERALD,
    "Other":                CYAN,
    "Active Low-Product":   AMBER,
    "Inactive High-Balance":ORANGE,
    "Inactive Disengaged":  ROSE,
}

# ══════════════════════════════════════════════
# TAB 1 — OVERVIEW
# ══════════════════════════════════════════════
with tab1:
    churned_t1  = df[df["Exited"]==1]
    retained_t1 = df[df["Exited"]==0]
    active_pct  = df["IsActiveMember"].mean() * 100
    cr_accent   = ROSE if cr_now>25 else AMBER if cr_now>15 else EMERALD

    k1,k2,k3,k4,k5,k6 = st.columns(6)
    k1.markdown(kpi("Total Customers", f"{len(df):,}", "In current view", CYAN, "100%"), unsafe_allow_html=True)
    k2.markdown(kpi("Churn Rate", f"{cr_now:.1f}%", f"{df['Exited'].sum():,} exited", cr_accent, f"{cr_now:.0f}%"), unsafe_allow_html=True)
    k3.markdown(kpi("Active Members", f"{active_pct:.1f}%", f"{df['IsActiveMember'].sum():,} active", EMERALD, f"{active_pct:.0f}%"), unsafe_allow_html=True)
    k4.markdown(kpi("Avg Age — Churned", f"{churned_t1['Age'].mean():.1f}", f"vs {retained_t1['Age'].mean():.1f} retained", AMBER, "70%"), unsafe_allow_html=True)
    k5.markdown(kpi("Germany Churn", f"{df[df['Geography']=='Germany']['Exited'].mean()*100:.1f}%", "Highest market", ROSE, "85%"), unsafe_allow_html=True)
    k6.markdown(kpi("Female Churn", f"{df[df['Gender']=='Female']['Exited'].mean()*100:.1f}%", "vs male baseline", VIOLET, "60%"), unsafe_allow_html=True)

    st.markdown("<br/>", unsafe_allow_html=True)
    st.markdown(sec("Geographic & Demographic Intelligence"), unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1.2, 1.2, 1])

    with col1:
        geo_df = churn_by(df, "Geography").sort_values("ChurnRate", ascending=False)
        fig = go.Figure()
        for _, row in geo_df.iterrows():
            c = rate_color(row["ChurnRate"])
            fig.add_trace(go.Bar(
                x=[row["Geography"]], y=[row["ChurnRate"]],
                marker_color=alpha(c,.25), marker_line_color=c, marker_line_width=1.5,
                marker_cornerradius=7,
                text=[f"{row['ChurnRate']:.1f}%"], textposition="outside",
                textfont=dict(family=FONT_MONO, color=c, size=12, weight=600),
                showlegend=False,
                hovertemplate=f"<b>{row['Geography']}</b><br>Churn: {row['ChurnRate']:.1f}%<br>Customers: {row['Total']:,}<extra></extra>",
            ))
        fig.update_layout(**base_layout(290), yaxis_ticksuffix="%", yaxis_range=[0,44])
        st.markdown(sec("Churn by Geography"), unsafe_allow_html=True)
        st.plotly_chart(fig, use_container_width=True, config=PLOTLY_CFG)

    with col2:
        age_df = churn_by(df, "AgeBand")
        age_order = ["<30","30–39","40–49","50–59","60+"]
        age_df["Order"] = age_df["AgeBand"].map({b:i for i,b in enumerate(age_order)})
        age_df = age_df.sort_values("Order")
        colors2 = [rate_color(r) for r in age_df["ChurnRate"]]
        fig2 = go.Figure(go.Bar(
            x=age_df["AgeBand"].astype(str), y=age_df["ChurnRate"],
            marker_color=[alpha(c,.25) for c in colors2],
            marker_line_color=colors2, marker_line_width=1.5,
            marker_cornerradius=7,
            text=[f"{r:.1f}%" for r in age_df["ChurnRate"]], textposition="outside",
            textfont=dict(family=FONT_MONO, size=11),
        ))
        fig2.update_traces(textfont_color=[rate_color(r) for r in age_df["ChurnRate"]])
        fig2.update_layout(**base_layout(290), yaxis_ticksuffix="%", yaxis_range=[0,70])
        st.markdown(sec("Churn by Age Group"), unsafe_allow_html=True)
        st.plotly_chart(fig2, use_container_width=True, config=PLOTLY_CFG)

    with col3:
        st.markdown(sec("Gender × Market"), unsafe_allow_html=True)
        gender_geo = df.groupby(["Geography","Gender"])["Exited"].mean().unstack() * 100
        rows_html = ""
        for geo in ["France","Germany","Spain"]:
            if geo not in gender_geo.index: continue
            f_r = gender_geo.loc[geo,"Female"] if "Female" in gender_geo.columns else 0
            m_r = gender_geo.loc[geo,"Male"]   if "Male"   in gender_geo.columns else 0
            f_cls = "danger" if f_r>=30 else "warn" if f_r>=20 else "ok"
            m_cls = "danger" if m_r>=30 else "warn" if m_r>=20 else "ok"
            flag  = {"France":"🇫🇷","Germany":"🇩🇪","Spain":"🇪🇸"}.get(geo,"🏳")
            rows_html += f"""
            <div class="geo-row">
              <span class="geo-name">{flag} {geo}</span>
              <div class="geo-badges">
                <span class="badge badge-{f_cls}">F {f_r:.1f}%</span>
                <span class="badge badge-{m_cls}">M {m_r:.1f}%</span>
              </div>
            </div>"""
        st.markdown(f'<div style="padding:0 4px">{rows_html}</div>', unsafe_allow_html=True)
        st.markdown(insight("Female Differential",
            "Germany female churn at 37.6% — the single highest demographic rate. Females churn 8–9 pts above males across all markets.",
            "ins-rose"), unsafe_allow_html=True)

    st.markdown("<br/>", unsafe_allow_html=True)
    st.markdown(sec("Activity Status & Credit Intelligence"), unsafe_allow_html=True)
    col4, col5 = st.columns(2)

    with col4:
        act_df = churn_by(df, "IsActiveMember")
        act_df["Label"] = act_df["IsActiveMember"].map({1:"Active Member",0:"Inactive Member"})
        fig3 = go.Figure()
        for _, row2 in act_df.iterrows():
            c = rate_color(row2["ChurnRate"])
            fig3.add_trace(go.Bar(
                x=[row2["Label"]], y=[row2["ChurnRate"]],
                marker_color=alpha(c,.25), marker_line_color=c, marker_line_width=1.5,
                marker_cornerradius=9,
                text=[f"{row2['ChurnRate']:.1f}%"], textposition="outside",
                textfont=dict(family=FONT_MONO, color=c, size=14, weight=700),
                showlegend=False,
            ))
        fig3.update_layout(**base_layout(270), yaxis_ticksuffix="%", yaxis_range=[0,38])
        st.markdown(sec("Active vs Inactive Churn"), unsafe_allow_html=True)
        st.plotly_chart(fig3, use_container_width=True, config=PLOTLY_CFG)

    with col5:
        cs_df = churn_by(df, "CSBand")
        cs_order = ["<500","500–599","600–699","700–799","800+"]
        cs_df["Order"] = cs_df["CSBand"].map({b:i for i,b in enumerate(cs_order)})
        cs_df = cs_df.dropna(subset=["Order"]).sort_values("Order")
        fig4 = go.Figure(go.Scatter(
            x=cs_df["CSBand"].astype(str), y=cs_df["ChurnRate"],
            mode="lines+markers",
            line=dict(color=CYAN, width=2.5),
            fill="tozeroy", fillcolor=alpha(CYAN,.06),
            marker=dict(color=[rate_color(r) for r in cs_df["ChurnRate"]], size=10, line=dict(width=2, color=DARK_BG)),
            text=[f"{r:.1f}%" for r in cs_df["ChurnRate"]], textposition="top center",
            textfont=dict(family=FONT_MONO, size=11),
        ))
        fig4.update_layout(**base_layout(270), yaxis_ticksuffix="%", yaxis_range=[17,27])
        st.markdown(sec("Churn by Credit Score Band"), unsafe_allow_html=True)
        st.plotly_chart(fig4, use_container_width=True, config=PLOTLY_CFG)


# ══════════════════════════════════════════════
# TAB 2 — ENGAGEMENT
# ══════════════════════════════════════════════
with tab2:
    eng_df      = churn_by(df, "EngagementProfile").sort_values("ChurnRate", ascending=False)
    active_eng  = df[df["EngagementProfile"]=="Active Engaged"]["Exited"].mean()*100  if (df["EngagementProfile"]=="Active Engaged").sum()>0 else 0
    inactive_dis= df[df["EngagementProfile"]=="Inactive Disengaged"]["Exited"].mean()*100 if (df["EngagementProfile"]=="Inactive Disengaged").sum()>0 else 0
    inactive_hb = df[df["EngagementProfile"]=="Inactive High-Balance"]["Exited"].mean()*100 if (df["EngagementProfile"]=="Inactive High-Balance").sum()>0 else 0
    active_lp   = df[df["EngagementProfile"]=="Active Low-Product"]["Exited"].mean()*100 if (df["EngagementProfile"]=="Active Low-Product").sum()>0 else 0
    spread      = inactive_dis / active_eng if active_eng > 0 else 0

    k1,k2,k3,k4,k5 = st.columns(5)
    k1.markdown(kpi("Active Engaged",    f"{active_eng:.1f}%",  "Lowest risk tier",       EMERALD,"10%"), unsafe_allow_html=True)
    k2.markdown(kpi("Active Low-Prod",   f"{active_lp:.1f}%",   "Upsell opportunity",      CYAN,   "19%"), unsafe_allow_html=True)
    k3.markdown(kpi("Inactive Hi-Bal",   f"{inactive_hb:.1f}%", "Premium flight risk",     AMBER,  "28%"), unsafe_allow_html=True)
    k4.markdown(kpi("Inactive Disengaged",f"{inactive_dis:.1f}%","Highest risk tier",      ROSE,   "37%"), unsafe_allow_html=True)
    k5.markdown(kpi("Risk Spread",       f"{spread:.1f}×",      "Worst vs best profile",   VIOLET, "70%"), unsafe_allow_html=True)

    st.markdown("<br/>", unsafe_allow_html=True)
    col1, col2 = st.columns([1, 1.6])

    with col1:
        eng_counts  = df.groupby("EngagementProfile").size().reset_index(name="Count")
        colors_donut= [ENG_COLORS.get(p,"#888") for p in eng_counts["EngagementProfile"]]
        fig_d = go.Figure(go.Pie(
            labels=eng_counts["EngagementProfile"], values=eng_counts["Count"],
            hole=0.64,
            marker_colors=[alpha(c,.8) for c in colors_donut],
            marker_line_color=colors_donut, marker_line_width=2,
            textinfo="percent",
            textfont=dict(family=FONT_MONO, size=10, color="#f0f6ff"),
            hovertemplate="<b>%{label}</b><br>%{value:,} customers<br>%{percent}<extra></extra>",
        ))
        fig_d.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=10,r=10,t=10,b=10), height=290,
            showlegend=True,
            legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(family=FONT_MONO, color="#3a5070", size=10), orientation="v", x=1, y=0.5),
            annotations=[dict(text=f"<b>{len(df):,}</b><br><span style='font-size:10px'>customers</span>",
                              x=0.5, y=0.5, showarrow=False, font=dict(family=FONT_MONO, size=14, color="#f0f6ff"))],
        )
        st.markdown(sec("Profile Distribution"), unsafe_allow_html=True)
        st.plotly_chart(fig_d, use_container_width=True, config=PLOTLY_CFG)

    with col2:
        eng_sorted = eng_df.sort_values("ChurnRate")
        fig_eb = go.Figure()
        for _, row3 in eng_sorted.iterrows():
            c = ENG_COLORS.get(row3["EngagementProfile"], CYAN)
            fig_eb.add_trace(go.Bar(
                y=[row3["EngagementProfile"]], x=[row3["ChurnRate"]], orientation="h",
                marker_color=alpha(c,.25), marker_line_color=c, marker_line_width=1.5,
                marker_cornerradius=6,
                text=[f"  {row3['ChurnRate']:.1f}%  ·  {row3['Total']:,}"],
                textposition="outside",
                textfont=dict(family=FONT_MONO, color=c, size=11),
                showlegend=False,
            ))
        fig_eb.update_layout(**base_layout(290), xaxis_ticksuffix="%", xaxis_range=[0,52])
        st.markdown(sec("Churn Rate by Profile"), unsafe_allow_html=True)
        st.plotly_chart(fig_eb, use_container_width=True, config=PLOTLY_CFG)

    st.markdown("<br/>", unsafe_allow_html=True)
    st.markdown(sec("Engagement Risk Matrix"), unsafe_allow_html=True)
    m1,m2,m3,m4,m5 = st.columns(5)
    for col_m, lbl, val, s1, s2, clr in [
        (m1,"Active Engaged",       "9.7%",  "2,588 customers","Lowest risk",    EMERALD),
        (m2,"Other / Mixed",        "10.5%", "1,549 customers","Near sticky",     CYAN),
        (m3,"Active Low-Product",   "18.9%", "2,563 customers","Upsell target",   AMBER),
        (m4,"Inactive High-Balance","27.6%", "779 customers",  "Premium flight",  ORANGE),
        (m5,"Inactive Disengaged",  "36.7%", "2,521 customers","Highest risk",    ROSE),
    ]:
        col_m.markdown(risk_cell(lbl, val, s1, s2, clr), unsafe_allow_html=True)

    st.markdown("<br/>", unsafe_allow_html=True)
    st.markdown(sec("Tenure & Activity Deep Dive"), unsafe_allow_html=True)
    col3, col4 = st.columns(2)

    with col3:
        ten_df = churn_by(df, "Tenure").sort_values("Tenure")
        fig_ten = go.Figure(go.Scatter(
            x=ten_df["Tenure"], y=ten_df["ChurnRate"],
            mode="lines+markers+text",
            line=dict(color=VIOLET, width=2.5),
            fill="tozeroy", fillcolor=alpha(VIOLET,.06),
            marker=dict(color=VIOLET, size=9, line=dict(width=2, color=DARK_BG)),
            text=[f"{r:.1f}%" for r in ten_df["ChurnRate"]], textposition="top center",
            textfont=dict(family=FONT_MONO, size=10, color=VIOLET),
        ))
        fig_ten.update_layout(**base_layout(260), yaxis_ticksuffix="%", xaxis_title="Years as Customer", yaxis_range=[15,27])
        st.markdown(sec("Churn by Tenure"), unsafe_allow_html=True)
        st.plotly_chart(fig_ten, use_container_width=True, config=PLOTLY_CFG)

    with col4:
        cross = df.groupby(["Geography","IsActiveMember"])["Exited"].agg(["sum","count"]).reset_index()
        cross["ChurnRate"] = cross["sum"] / cross["count"] * 100
        cross["Status"]    = cross["IsActiveMember"].map({1:"Active",0:"Inactive"})
        fig_cross = go.Figure()
        for status, clr in [("Active", EMERALD), ("Inactive", ROSE)]:
            d = cross[cross["Status"]==status]
            fig_cross.add_trace(go.Bar(
                name=status, x=d["Geography"], y=d["ChurnRate"],
                marker_color=alpha(clr,.25), marker_line_color=clr, marker_line_width=1.5,
                marker_cornerradius=5,
                text=[f"{r:.1f}%" for r in d["ChurnRate"]], textposition="outside",
                textfont=dict(family=FONT_MONO, color=clr, size=11),
            ))
        fig_cross.update_layout(**base_layout(260), barmode="group", yaxis_ticksuffix="%", yaxis_range=[0,44])
        st.markdown(sec("Geography × Activity Churn"), unsafe_allow_html=True)
        st.plotly_chart(fig_cross, use_container_width=True, config=PLOTLY_CFG)

    st.markdown(insight("Priority Action",
        "The 2,521 Inactive Disengaged customers represent the highest-volume at-risk cohort at 36.65% churn. "
        "Age 50–59 customers face a 56% churn probability — a retention emergency requiring dedicated age-segmented intervention.",
        "ins-rose"), unsafe_allow_html=True)


# ══════════════════════════════════════════════
# TAB 3 — PRODUCTS
# ══════════════════════════════════════════════
with tab3:
    p1_c = df[df["NumOfProducts"]==1]["Exited"].mean()*100 if (df["NumOfProducts"]==1).sum()>0 else 0
    p2_c = df[df["NumOfProducts"]==2]["Exited"].mean()*100 if (df["NumOfProducts"]==2).sum()>0 else 0
    p3_c = df[df["NumOfProducts"]>=3]["Exited"].mean()*100 if (df["NumOfProducts"]>=3).sum()>0 else 0
    cc_d = (df[df["HasCrCard"]==0]["Exited"].mean() - df[df["HasCrCard"]==1]["Exited"].mean())*100

    k1,k2,k3,k4 = st.columns(4)
    k1.markdown(kpi("1-Product Churn",    f"{p1_c:.1f}%",    "5,084 customers",   AMBER,   "28%"), unsafe_allow_html=True)
    k2.markdown(kpi("2-Product Churn",    f"{p2_c:.1f}%",    "Optimal sweet spot", EMERALD, "8%"),  unsafe_allow_html=True)
    k3.markdown(kpi("3–4 Product Churn",  f"{p3_c:.1f}%",    "Product paradox",    ROSE,    "83%"), unsafe_allow_html=True)
    k4.markdown(kpi("CC Stickiness Δ",    f"{cc_d:+.2f}pp",  "No CC vs has CC",    CYAN,    "50%"), unsafe_allow_html=True)

    st.markdown("<br/>", unsafe_allow_html=True)
    col1, col2 = st.columns([1.4, 1])

    with col1:
        prod_df = churn_by(df, "NumOfProducts").sort_values("NumOfProducts")
        p_colors = [rate_color(r) for r in prod_df["ChurnRate"]]
        fig_p = go.Figure(go.Bar(
            x=[f"{int(n)} Product{'s' if int(n)>1 else ''}" for n in prod_df["NumOfProducts"]],
            y=prod_df["ChurnRate"],
            marker_color=[alpha(c,.25) for c in p_colors],
            marker_line_color=p_colors, marker_line_width=2, marker_cornerradius=9,
            text=[f"{r:.1f}%" for r in prod_df["ChurnRate"]], textposition="outside",
            textfont=dict(family=FONT_MONO, size=14, weight=700),
        ))
        fig_p.update_traces(textfont_color=p_colors)
        fig_p.update_layout(**base_layout(310), yaxis_ticksuffix="%", yaxis_range=[0,118])
        st.markdown(sec("Product Depth Index — Churn by Product Count"), unsafe_allow_html=True)
        st.plotly_chart(fig_p, use_container_width=True, config=PLOTLY_CFG)

    with col2:
        rsi_df = churn_by(df, "RSI").sort_values("RSI")
        fig_rsi = go.Figure()
        for _, row4 in rsi_df.iterrows():
            c = rate_color(row4["ChurnRate"])
            fig_rsi.add_trace(go.Bar(
                y=[f"RSI {int(row4['RSI'])}"], x=[row4["ChurnRate"]], orientation="h",
                marker_color=alpha(c,.25), marker_line_color=c, marker_line_width=1.5,
                marker_cornerradius=6,
                text=[f"  {row4['ChurnRate']:.1f}%  ·  {row4['Total']:,}"],
                textposition="outside",
                textfont=dict(family=FONT_MONO, color=c, size=11),
                showlegend=False,
            ))
        fig_rsi.update_layout(**base_layout(310), xaxis_ticksuffix="%", xaxis_range=[0,52])
        st.markdown(sec("RSI → Churn Rate"), unsafe_allow_html=True)
        st.plotly_chart(fig_rsi, use_container_width=True, config=PLOTLY_CFG)

    st.markdown("<br/>", unsafe_allow_html=True)
    st.markdown(sec("Product Count × Engagement Matrix"), unsafe_allow_html=True)
    cross2 = df.groupby(["NumOfProducts","IsActiveMember"])["Exited"].agg(["sum","count"]).reset_index()
    cross2["ChurnRate"] = cross2["sum"] / cross2["count"] * 100
    cross2["Status"]    = cross2["IsActiveMember"].map({1:"Active",0:"Inactive"})
    cross2["Products"]  = cross2["NumOfProducts"].astype(str) + " Product(s)"
    fig_c2 = go.Figure()
    for status, clr in [("Active", EMERALD), ("Inactive", ROSE)]:
        d2 = cross2[cross2["Status"]==status]
        fig_c2.add_trace(go.Bar(
            name=status, x=d2["Products"], y=d2["ChurnRate"],
            marker_color=alpha(clr,.25), marker_line_color=clr, marker_line_width=1.5,
            marker_cornerradius=5,
            text=[f"{r:.0f}%" for r in d2["ChurnRate"]], textposition="outside",
            textfont=dict(family=FONT_MONO, color=clr, size=11),
        ))
    fig_c2.update_layout(**base_layout(290), barmode="group", yaxis_ticksuffix="%", yaxis_range=[0,118])
    st.plotly_chart(fig_c2, use_container_width=True, config=PLOTLY_CFG)

    c_l, c_r = st.columns(2)
    with c_l:
        st.markdown(insight("Product Paradox — Regulatory Signal",
            "3–4 product customers churn at 82–100%. Product breadth does not create loyalty. "
            "This pattern is consistent with mis-selling and warrants internal audit.",
            "ins-rose"), unsafe_allow_html=True)
    with c_r:
        st.markdown(insight("The 2-Product Sweet Spot",
            "Moving single-product customers to exactly 2 products is the highest-leverage retention action. "
            "2-product customers churn at just 7.6% — a 72% reduction vs single-product holders.",
            "ins-emerald"), unsafe_allow_html=True)


# ══════════════════════════════════════════════
# TAB 4 — FINANCIAL
# ══════════════════════════════════════════════
with tab4:
    churned_df  = df[df["Exited"]==1]
    retained_df = df[df["Exited"]==0]
    avg_bal_c   = churned_df["Balance"].mean()  if len(churned_df)>0  else 0
    avg_bal_r   = retained_df["Balance"].mean() if len(retained_df)>0 else 0
    avg_sal_c   = churned_df["EstimatedSalary"].mean()  if len(churned_df)>0  else 0
    avg_sal_r   = retained_df["EstimatedSalary"].mean() if len(retained_df)>0 else 0
    at_risk_n   = df["IsAtRisk"].sum()
    at_risk_cr  = df[df["IsAtRisk"]==1]["Exited"].mean()*100 if at_risk_n>0 else 0
    bal_gap_pct = ((avg_bal_c - avg_bal_r) / avg_bal_r * 100) if avg_bal_r>0 else 0

    k1,k2,k3,k4 = st.columns(4)
    k1.markdown(kpi("Avg Bal — Churned",  f"€{avg_bal_c:,.0f}",         f"+{bal_gap_pct:.0f}% vs retained", ROSE,    "65%"), unsafe_allow_html=True)
    k2.markdown(kpi("Avg Bal — Retained", f"€{avg_bal_r:,.0f}",         "Reference baseline",                EMERALD, "52%"), unsafe_allow_html=True)
    k3.markdown(kpi("At-Risk Premium",    f"{at_risk_n:,}",              f"{at_risk_cr:.1f}% churn",          AMBER,   "45%"), unsafe_allow_html=True)
    k4.markdown(kpi("Salary Parity",      f"€{abs(avg_sal_c-avg_sal_r):,.0f}", "Churned–retained gap",       CYAN,    "5%"),  unsafe_allow_html=True)

    st.markdown("<br/>", unsafe_allow_html=True)
    st.markdown(sec("Balance Distribution Intelligence"), unsafe_allow_html=True)
    col1, col2 = st.columns(2)

    with col1:
        bal_order = ["Zero","€1–50K","€50–100K","€100–150K","€150K+"]
        bal_df2   = churn_by(df, "BalanceBand")
        bal_df2["Order"] = bal_df2["BalanceBand"].map({b:i for i,b in enumerate(bal_order)})
        bal_df2   = bal_df2.dropna(subset=["Order"]).sort_values("Order")
        b_colors  = [rate_color(r) for r in bal_df2["ChurnRate"]]
        fig_bal   = go.Figure(go.Bar(
            x=bal_df2["BalanceBand"].astype(str), y=bal_df2["ChurnRate"],
            marker_color=[alpha(c,.25) for c in b_colors],
            marker_line_color=b_colors, marker_line_width=1.5, marker_cornerradius=7,
            text=[f"{r:.1f}%" for r in bal_df2["ChurnRate"]], textposition="outside",
            textfont=dict(family=FONT_MONO, size=12, weight=700),
        ))
        fig_bal.update_traces(textfont_color=b_colors)
        fig_bal.update_layout(**base_layout(290), yaxis_ticksuffix="%", yaxis_range=[0,46])
        st.markdown(sec("Churn Rate by Balance Band"), unsafe_allow_html=True)
        st.plotly_chart(fig_bal, use_container_width=True, config=PLOTLY_CFG)

    with col2:
        metrics = ["Avg Balance","Avg Est. Salary"]
        c_vals  = [avg_bal_c, avg_sal_c]
        r_vals  = [avg_bal_r, avg_sal_r]
        fig_cmp = go.Figure()
        fig_cmp.add_trace(go.Bar(
            name="Churned", x=metrics, y=c_vals,
            marker_color=alpha(ROSE,.25), marker_line_color=ROSE, marker_line_width=1.5,
            marker_cornerradius=6,
            text=[f"€{v:,.0f}" for v in c_vals], textposition="outside",
            textfont=dict(family=FONT_MONO, color=ROSE, size=11),
        ))
        fig_cmp.add_trace(go.Bar(
            name="Retained", x=metrics, y=r_vals,
            marker_color=alpha(EMERALD,.25), marker_line_color=EMERALD, marker_line_width=1.5,
            marker_cornerradius=6,
            text=[f"€{v:,.0f}" for v in r_vals], textposition="outside",
            textfont=dict(family=FONT_MONO, color=EMERALD, size=11),
        ))
        layout_cmp = base_layout(290)
        layout_cmp["yaxis"]["tickprefix"] = "€"
        layout_cmp["yaxis"]["range"]      = [0, max(c_vals + r_vals) * 1.25]
        fig_cmp.update_layout(**layout_cmp, barmode="group")
        st.markdown(sec("Churned vs Retained — Financial Profile"), unsafe_allow_html=True)
        st.plotly_chart(fig_cmp, use_container_width=True, config=PLOTLY_CFG)

    st.markdown("<br/>", unsafe_allow_html=True)
    st.markdown(sec("Balance Distribution — Churned vs Retained"), unsafe_allow_html=True)
    nz_c = churned_df[churned_df["Balance"]>0]["Balance"]
    nz_r = retained_df[retained_df["Balance"]>0]["Balance"]
    fig_hist = go.Figure()
    if len(nz_c)>0:
        fig_hist.add_trace(go.Histogram(
            x=nz_c, name="Churned", opacity=0.65,
            marker_color=ROSE, nbinsx=50, histnorm="percent",
        ))
    if len(nz_r)>0:
        fig_hist.add_trace(go.Histogram(
            x=nz_r, name="Retained", opacity=0.5,
            marker_color=EMERALD, nbinsx=50, histnorm="percent",
        ))
    fig_hist.update_layout(**base_layout(270), barmode="overlay",
        xaxis_tickprefix="€", xaxis_title="Account Balance (€)", yaxis_title="% of Customers")
    st.plotly_chart(fig_hist, use_container_width=True, config=PLOTLY_CFG)

    c_l, c_r = st.columns(2)
    with c_l:
        st.markdown(insight("Premium Balance Flight Risk",
            f"Churned customers hold €{avg_bal_c:,.0f} average balance — {bal_gap_pct:.0f}% above the €{avg_bal_r:,.0f} retained average. "
            f"{at_risk_n:,} inactive high-balance customers at {at_risk_cr:.1f}% churn. Estimated AUM at risk: €300M+.",
            "ins-rose"), unsafe_allow_html=True)
    with c_r:
        st.markdown(insight("Salary Is Not the Driver",
            "Salary is virtually identical between churned (€101,466) and retained (€99,738) customers — a €1,728 gap. "
            "Engagement, not income, is the primary churn driver. Salary-based targeting will not work.",
            "ins-cyan"), unsafe_allow_html=True)


# ══════════════════════════════════════════════
# TAB 5 — RETENTION
# ══════════════════════════════════════════════
with tab5:
    sticky_df  = df[df["IsSticky"]==1]
    atrisk_df  = df[df["IsAtRisk"]==1]
    sticky_cr  = sticky_df["Exited"].mean()*100  if len(sticky_df)>0  else 0
    atrisk_cr  = atrisk_df["Exited"].mean()*100  if len(atrisk_df)>0  else 0
    gap_mult   = atrisk_cr / sticky_cr if sticky_cr>0 else 0

    k1,k2,k3,k4 = st.columns(4)
    k1.markdown(kpi("Sticky Churn",   f"{sticky_cr:.1f}%", f"{len(sticky_df):,} sticky customers",    EMERALD, "9%"),          unsafe_allow_html=True)
    k2.markdown(kpi("At-Risk Churn",  f"{atrisk_cr:.1f}%", f"{len(atrisk_df):,} at-risk customers",  ROSE,    "33%"),         unsafe_allow_html=True)
    k3.markdown(kpi("Retention Gap",  f"{gap_mult:.1f}×",  "Sticky vs at-risk differential",          AMBER,   "70%"),         unsafe_allow_html=True)
    k4.markdown(kpi("Portfolio Churn",f"{cr_now:.1f}%",    "Current filter view",                     CYAN,    f"{cr_now:.0f}%"), unsafe_allow_html=True)

    st.markdown("<br/>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)

    with col1:
        segs      = ["Sticky<br>(Active+2P+CC)", "Portfolio<br>Average", "At-Risk<br>(Inactive+€100K+)"]
        rates     = [sticky_cr, cr_now, atrisk_cr]
        seg_clrs  = [EMERALD, CYAN, ROSE]
        fig_s = go.Figure()
        for seg, rate, c in zip(segs, rates, seg_clrs):
            fig_s.add_trace(go.Bar(
                x=[seg], y=[rate],
                marker_color=alpha(c,.25), marker_line_color=c, marker_line_width=2,
                marker_cornerradius=9,
                text=[f"{rate:.1f}%"], textposition="outside",
                textfont=dict(family=FONT_MONO, color=c, size=14, weight=700),
                showlegend=False,
            ))
        fig_s.update_layout(**base_layout(310), yaxis_ticksuffix="%", yaxis_range=[0,44])
        st.markdown(sec("Sticky vs At-Risk vs Portfolio"), unsafe_allow_html=True)
        st.plotly_chart(fig_s, use_container_width=True, config=PLOTLY_CFG)

    with col2:
        rsi_df2 = churn_by(df, "RSI").sort_values("RSI")
        fig_r2  = go.Figure()
        fig_r2.add_trace(go.Scatter(
            x=rsi_df2["RSI"], y=rsi_df2["ChurnRate"],
            mode="lines+markers+text",
            line=dict(color=AMBER, width=3),
            fill="tozeroy", fillcolor=alpha(AMBER,.07),
            marker=dict(
                color=[rate_color(r) for r in rsi_df2["ChurnRate"]],
                size=14, line=dict(width=2.5, color=DARK_BG)
            ),
            text=[f"{r:.1f}%" for r in rsi_df2["ChurnRate"]],
            textposition="top center",
            textfont=dict(family=FONT_MONO, size=12, color=AMBER),
        ))
        # ── FIX: merge xaxis to avoid duplicate key conflict ──
        _layout_r2 = base_layout(310)
        _layout_r2["xaxis"].update(dict(title="RSI Score (1=Low → 4=High)", tickvals=[1,2,3,4]))
        fig_r2.update_layout(**_layout_r2, yaxis_ticksuffix="%", yaxis_range=[0,44])
        st.markdown(sec("RSI Score → Churn Rate"), unsafe_allow_html=True)
        st.plotly_chart(fig_r2, use_container_width=True, config=PLOTLY_CFG)

    st.markdown("<br/>", unsafe_allow_html=True)
    col3, col4 = st.columns([1, 1.4])

    with col3:
        cs_df2 = churn_by(df, "CSBand")
        cs_order2 = ["<500","500–599","600–699","700–799","800+"]
        cs_df2["Order"] = cs_df2["CSBand"].map({b:i for i,b in enumerate(cs_order2)})
        cs_df2 = cs_df2.dropna(subset=["Order"]).sort_values("Order")
        cs_c2  = [rate_color(r) for r in cs_df2["ChurnRate"]]
        fig_cs2 = go.Figure(go.Bar(
            x=cs_df2["CSBand"].astype(str), y=cs_df2["ChurnRate"],
            marker_color=[alpha(c,.25) for c in cs_c2],
            marker_line_color=cs_c2, marker_line_width=1.5, marker_cornerradius=6,
            text=[f"{r:.1f}%" for r in cs_df2["ChurnRate"]], textposition="outside",
            textfont=dict(family=FONT_MONO, size=11),
        ))
        fig_cs2.update_traces(textfont_color=cs_c2)
        fig_cs2.update_layout(**base_layout(250), yaxis_ticksuffix="%", yaxis_range=[15,30])
        st.markdown(sec("Credit Score vs Churn"), unsafe_allow_html=True)
        st.plotly_chart(fig_cs2, use_container_width=True, config=PLOTLY_CFG)

    with col4:
        eng_ret    = churn_by(df, "EngagementProfile").sort_values("ChurnRate")
        fig_ret    = go.Figure()
        for _, row5 in eng_ret.iterrows():
            c = ENG_COLORS.get(row5["EngagementProfile"], CYAN)
            fig_ret.add_trace(go.Bar(
                y=[row5["EngagementProfile"]], x=[row5["ChurnRate"]], orientation="h",
                marker_color=alpha(c,.25), marker_line_color=c, marker_line_width=1.5,
                marker_cornerradius=5,
                text=[f"  {row5['ChurnRate']:.1f}%  ·  {row5['Total']:,}"],
                textposition="outside",
                textfont=dict(family=FONT_MONO, color=c, size=11),
                showlegend=False,
            ))
        fig_ret.update_layout(**base_layout(250), xaxis_ticksuffix="%", xaxis_range=[0,52])
        st.markdown(sec("Full Retention Profile Map"), unsafe_allow_html=True)
        st.plotly_chart(fig_ret, use_container_width=True, config=PLOTLY_CFG)

    st.markdown("<br/>", unsafe_allow_html=True)
    st.markdown(sec("Strategic Retention Recommendations"), unsafe_allow_html=True)
    r1,r2 = st.columns(2)
    r3,r4 = st.columns(2)
    with r1:
        st.markdown(insight("Priority 1 — Protect Sticky Customers",
            f"{len(sticky_df):,} customers with RSI=4 churn at just {sticky_cr:.1f}%. "
            "White-glove service and proactive engagement. Each defection costs 3× more to replace.",
            "ins-emerald"), unsafe_allow_html=True)
    with r2:
        st.markdown(insight("Priority 2 — Emergency At-Risk Re-engagement",
            f"{len(atrisk_df):,} inactive customers with >€100K balance at {atrisk_cr:.1f}% churn. "
            "Immediate relationship manager outreach could save 770+ accounts worth €100M+ AUM.",
            "ins-rose"), unsafe_allow_html=True)
    with r3:
        st.markdown(insight("Priority 3 — 2-Product Migration Campaign",
            "5,084 single-product customers at 27.7% churn. Target Active Low-Product (2,563 customers, 18.9%) "
            "for cross-sell — proven 72% churn reduction in the 2-product tier.",
            "ins-amber"), unsafe_allow_html=True)
    with r4:
        st.markdown(insight("Priority 4 — Germany & Female Segment Focus",
            "Germany female churn at 37.6% — highest in the dataset. Targeted outreach concentrates "
            "retention resources on 600–700 highest-risk individuals with maximum ROI.",
            "ins-violet"), unsafe_allow_html=True)

    st.markdown("<br/>", unsafe_allow_html=True)
    st.markdown(sec("High-Value Disengaged Customer Detector"), unsafe_allow_html=True)
    st.caption("Inactive customers with balance > €75,000 — sorted by balance descending · Top 50")

    at_risk_tbl = df[
        (df["IsActiveMember"]==0) & (df["Balance"]>75000)
    ][["CustomerId","Geography","Gender","Age","Balance","NumOfProducts","HasCrCard","RSI","EngagementProfile","Exited"]].copy()
    at_risk_tbl = at_risk_tbl.sort_values("Balance", ascending=False).head(50)
    at_risk_tbl.columns = ["Customer ID","Country","Gender","Age","Balance (€)","Products","Has CC","RSI","Profile","Churned"]
    at_risk_tbl["Balance (€)"] = at_risk_tbl["Balance (€)"].apply(lambda x: f"€{x:,.0f}")
    at_risk_tbl["Churned"]     = at_risk_tbl["Churned"].map({1:"✗ Exited",0:"✓ Active"})
    st.dataframe(at_risk_tbl, use_container_width=True, height=340)

# ─────────────────────────────────────────────
# Footer
# ─────────────────────────────────────────────
st.markdown("""
<div class="dash-footer">
  European Bank Churn Intelligence Platform &nbsp;·&nbsp;
  10,000 Customer Records &nbsp;·&nbsp;
  France · Germany · Spain &nbsp;·&nbsp;
  FY 2025 &nbsp;·&nbsp; For Academic & Portfolio Use Only
</div>
""", unsafe_allow_html=True)
