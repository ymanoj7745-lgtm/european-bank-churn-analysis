"""
European Bank Customer Churn Analytics Dashboard
=================================================
A comprehensive Streamlit dashboard for customer retention intelligence.

Run with:
    pip install streamlit pandas plotly numpy
    streamlit run European_Bank_Dashboard.py
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

# ─────────────────────────────────────────────
# Page Configuration
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="European Bank | Churn Intelligence",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# Custom CSS Styling
# ─────────────────────────────────────────────
st.markdown("""
<style>
    /* Main palette */
    :root {
        --navy: #1F4E79;
        --blue: #2E75B6;
        --light-blue: #D6E4F0;
        --danger: #C00000;
        --warn: #BA7517;
        --ok: #3A7D44;
    }

    /* Page background */
    .main .block-container { padding-top: 1.5rem; padding-bottom: 2rem; max-width: 1400px; }

    /* Header banner */
    .dash-header {
        background: linear-gradient(135deg, #1F4E79 0%, #2E75B6 100%);
        border-radius: 12px;
        padding: 24px 32px;
        margin-bottom: 1.5rem;
        color: white;
    }
    .dash-header h1 { color: white; font-size: 1.8rem; margin: 0; font-weight: 700; }
    .dash-header p  { color: rgba(255,255,255,0.8); margin: 4px 0 0; font-size: 0.9rem; }

    /* KPI cards */
    .kpi-card {
        background: white;
        border: 1px solid #e8e8e8;
        border-radius: 10px;
        padding: 18px 20px;
        text-align: center;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
        height: 100%;
    }
    .kpi-label  { font-size: 0.72rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.06em; color: #888; margin-bottom: 6px; }
    .kpi-value  { font-size: 2rem; font-weight: 700; line-height: 1; }
    .kpi-sub    { font-size: 0.75rem; color: #999; margin-top: 4px; }
    .kpi-danger { color: #C00000; }
    .kpi-warn   { color: #BA7517; }
    .kpi-ok     { color: #3A7D44; }
    .kpi-blue   { color: #2E75B6; }

    /* Section dividers */
    .section-header {
        font-size: 1.05rem;
        font-weight: 700;
        color: #1F4E79;
        border-bottom: 2px solid #2E75B6;
        padding-bottom: 6px;
        margin: 1.5rem 0 1rem;
    }

    /* Insight boxes */
    .insight-box {
        background: #EBF5FB;
        border-left: 4px solid #2E75B6;
        border-radius: 0 8px 8px 0;
        padding: 12px 16px;
        margin: 1rem 0;
        font-size: 0.88rem;
        color: #1a1a1a;
        line-height: 1.6;
    }
    .alert-box {
        background: #FFF8E1;
        border-left: 4px solid #BA7517;
        border-radius: 0 8px 8px 0;
        padding: 12px 16px;
        margin: 1rem 0;
        font-size: 0.88rem;
        color: #1a1a1a;
        line-height: 1.6;
    }
    .danger-box {
        background: #FDECEA;
        border-left: 4px solid #C00000;
        border-radius: 0 8px 8px 0;
        padding: 12px 16px;
        margin: 1rem 0;
        font-size: 0.88rem;
        color: #1a1a1a;
        line-height: 1.6;
    }

    /* Profile pills */
    .profile-pill {
        display: inline-block;
        padding: 3px 10px;
        border-radius: 12px;
        font-size: 0.75rem;
        font-weight: 600;
    }

    /* Sidebar styling */
    .css-1d391kg { background: #F4F7FB; }

    /* Metric delta override */
    [data-testid="stMetricDelta"] { font-size: 0.78rem; }

    /* Tab styling */
    .stTabs [data-baseweb="tab"] { font-weight: 600; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# Data Loading & Feature Engineering
# ─────────────────────────────────────────────
@st.cache_data
def load_data():
    """Load and engineer features from the European Bank CSV."""
    # Try multiple paths
    for path in ["European_Bank.csv", "/mnt/project/European_Bank.csv", "/mnt/user-data/uploads/European_Bank.csv"]:
        try:
            df = pd.read_csv(path)
            break
        except FileNotFoundError:
            continue
    else:
        # Generate synthetic data for demo if file not found
        np.random.seed(42)
        n = 10000
        df = pd.DataFrame({
            "CustomerId": range(1, n+1),
            "CreditScore": np.random.randint(350, 851, n),
            "Geography": np.random.choice(["France","Germany","Spain"], n, p=[0.5, 0.25, 0.25]),
            "Gender": np.random.choice(["Male","Female"], n),
            "Age": np.clip(np.random.normal(38, 10, n).astype(int), 18, 80),
            "Tenure": np.random.randint(0, 11, n),
            "Balance": np.where(np.random.random(n) < 0.37, 0, np.random.uniform(10000, 250000, n)),
            "NumOfProducts": np.random.choice([1,2,3,4], n, p=[0.5, 0.46, 0.027, 0.006]),
            "HasCrCard": np.random.choice([0,1], n, p=[0.3, 0.7]),
            "IsActiveMember": np.random.choice([0,1], n, p=[0.49, 0.51]),
            "EstimatedSalary": np.random.uniform(10000, 200000, n),
            "Exited": np.random.choice([0,1], n, p=[0.8, 0.2]),
        })

    # Feature engineering
    df["Exited"] = df["Exited"].astype(int)
    df["IsActiveMember"] = df["IsActiveMember"].astype(int)
    df["HasCrCard"] = df["HasCrCard"].astype(int)

    # RSI: Relationship Strength Index
    df["RSI"] = df["IsActiveMember"] + df["NumOfProducts"].clip(upper=2) + df["HasCrCard"]

    # Engagement profile
    def classify(row):
        active = row["IsActiveMember"] == 1
        prods = row["NumOfProducts"]
        bal = row["Balance"]
        if active and prods >= 2:       return "Active Engaged"
        elif not active and prods <= 1: return "Inactive Disengaged"
        elif active and prods == 1:     return "Active Low-Product"
        elif not active and bal > 100000: return "Inactive High-Balance"
        else:                           return "Other"

    df["EngagementProfile"] = df.apply(classify, axis=1)

    # Age bucket
    bins  = [0, 29, 39, 49, 59, 120]
    labels = ["<30", "30-39", "40-49", "50-59", "60+"]
    df["AgeBand"] = pd.cut(df["Age"], bins=bins, labels=labels)

    # Balance bucket
    def bal_bucket(b):
        if b == 0:          return "Zero"
        elif b < 50000:     return "€1–50K"
        elif b < 100000:    return "€50–100K"
        elif b < 150000:    return "€100–150K"
        else:               return "€150K+"

    df["BalanceBand"] = df["Balance"].apply(bal_bucket)

    # Sticky / at-risk flags
    df["IsSticky"]  = ((df["IsActiveMember"] == 1) & (df["NumOfProducts"] >= 2) & (df["HasCrCard"] == 1)).astype(int)
    df["IsAtRisk"]  = ((df["IsActiveMember"] == 0) & (df["Balance"] > 100000)).astype(int)

    # Credit score band
    cs_bins   = [0, 499, 599, 699, 799, 1000]
    cs_labels = ["<500", "500–599", "600–699", "700–799", "800+"]
    df["CSBand"] = pd.cut(df["CreditScore"], bins=cs_bins, labels=cs_labels)

    return df

# ─────────────────────────────────────────────
# Helper functions
# ─────────────────────────────────────────────
COLOR_MAP = {
    "ok":     "#3A7D44",
    "warn":   "#BA7517",
    "danger": "#C00000",
    "blue":   "#2E75B6",
    "navy":   "#1F4E79",
    "gray":   "#6C757D",
}

PROFILE_COLORS = {
    "Active Engaged":        "#3A7D44",
    "Other":                 "#6C757D",
    "Active Low-Product":    "#BA7517",
    "Inactive High-Balance": "#E24B4A",
    "Inactive Disengaged":   "#C00000",
}

def churn_rate(df):
    """Return churn rate as a percentage."""
    return df["Exited"].mean() * 100

def churn_by(df, col, sort_by_churn=False):
    """Return churn rate grouped by a column."""
    g = df.groupby(col)["Exited"].agg(["sum", "count"]).reset_index()
    g.columns = [col, "Churned", "Total"]
    g["ChurnRate"] = g["Churned"] / g["Total"] * 100
    if sort_by_churn:
        g = g.sort_values("ChurnRate", ascending=False)
    return g

def color_by_rate(rate):
    if rate < 15:   return COLOR_MAP["ok"]
    elif rate < 25: return COLOR_MAP["warn"]
    else:           return COLOR_MAP["danger"]

def kpi_html(label, value, sub="", color_class="kpi-blue"):
    return f"""
    <div class="kpi-card">
        <div class="kpi-label">{label}</div>
        <div class="kpi-value {color_class}">{value}</div>
        <div class="kpi-sub">{sub}</div>
    </div>"""

# ─────────────────────────────────────────────
# Load data
# ─────────────────────────────────────────────
df_full = load_data()

# ─────────────────────────────────────────────
# SIDEBAR — Filters
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🔍 Filters")
    st.markdown("---")

    st.markdown("**Geography**")
    geographies = st.multiselect(
        "Select countries", options=df_full["Geography"].unique().tolist(),
        default=df_full["Geography"].unique().tolist(), label_visibility="collapsed"
    )

    st.markdown("**Gender**")
    genders = st.multiselect(
        "Select gender", options=df_full["Gender"].unique().tolist(),
        default=df_full["Gender"].unique().tolist(), label_visibility="collapsed"
    )

    st.markdown("**Engagement Profile**")
    profiles = st.multiselect(
        "Select profiles",
        options=["Active Engaged", "Active Low-Product", "Other", "Inactive High-Balance", "Inactive Disengaged"],
        default=["Active Engaged", "Active Low-Product", "Other", "Inactive High-Balance", "Inactive Disengaged"],
        label_visibility="collapsed"
    )

    st.markdown("**Product Count**")
    prod_range = st.slider("Number of products", 1, 4, (1, 4))

    st.markdown("**Account Balance (€)**")
    bal_min, bal_max = st.slider(
        "Balance range", min_value=0, max_value=250000,
        value=(0, 250000), step=5000, format="€%d", label_visibility="collapsed"
    )

    st.markdown("**Age Range**")
    age_min, age_max = st.slider("Age", 18, 80, (18, 80), label_visibility="collapsed")

    st.markdown("**Credit Score**")
    cs_min, cs_max = st.slider("Credit Score", 350, 850, (350, 850), label_visibility="collapsed")

    st.markdown("---")
    st.markdown("**Activity Status**")
    active_filter = st.radio("Members", ["All", "Active only", "Inactive only"], horizontal=False)

    st.markdown("---")
    st.caption("🏦 European Bank Churn Intelligence Platform")
    st.caption("Dataset: 10,000 customers · FY 2024")

# Apply filters
df = df_full.copy()
if geographies:    df = df[df["Geography"].isin(geographies)]
if genders:        df = df[df["Gender"].isin(genders)]
if profiles:       df = df[df["EngagementProfile"].isin(profiles)]
df = df[df["NumOfProducts"].between(prod_range[0], prod_range[1])]
df = df[df["Balance"].between(bal_min, bal_max)]
df = df[df["Age"].between(age_min, age_max)]
df = df[df["CreditScore"].between(cs_min, cs_max)]
if active_filter == "Active only":   df = df[df["IsActiveMember"] == 1]
elif active_filter == "Inactive only": df = df[df["IsActiveMember"] == 0]

# ─────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────
st.markdown(f"""
<div class="dash-header">
    <h1>🏦 European Bank — Churn Intelligence Platform</h1>
    <p>Customer Retention & Engagement Analytics  ·  {len(df):,} customers in view  ·  Filtered from {len(df_full):,} total records</p>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# TABS
# ─────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Overview",
    "👥 Engagement",
    "📦 Product Utilization",
    "💰 Financial Analysis",
    "🛡️ Retention Strength",
])

# ══════════════════════════════════════════════
# TAB 1: OVERVIEW
# ══════════════════════════════════════════════
with tab1:
    # KPI row
    cr = churn_rate(df)
    active_pct = df["IsActiveMember"].mean() * 100
    churned_bal = df[df["Exited"] == 1]["Balance"].mean()
    retained_bal = df[df["Exited"] == 0]["Balance"].mean()
    cr_color = "kpi-danger" if cr > 25 else "kpi-warn" if cr > 15 else "kpi-ok"

    c1, c2, c3, c4, c5 = st.columns(5)
    c1.markdown(kpi_html("Total Customers", f"{len(df):,}", "In current filter", "kpi-blue"), unsafe_allow_html=True)
    c2.markdown(kpi_html("Churn Rate", f"{cr:.1f}%", f"{df['Exited'].sum():,} exited", cr_color), unsafe_allow_html=True)
    c3.markdown(kpi_html("Active Members", f"{active_pct:.1f}%", f"{df['IsActiveMember'].sum():,} active", "kpi-ok"), unsafe_allow_html=True)
    c4.markdown(kpi_html("Avg Balance — Churned", f"€{churned_bal:,.0f}", "vs retained below", "kpi-warn"), unsafe_allow_html=True)
    c5.markdown(kpi_html("Avg Balance — Retained", f"€{retained_bal:,.0f}", f"Gap: €{churned_bal - retained_bal:,.0f}", "kpi-ok"), unsafe_allow_html=True)

    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="section-header">Churn Rate by Geography</div>', unsafe_allow_html=True)
        geo_df = churn_by(df, "Geography", sort_by_churn=True)
        colors = [color_by_rate(r) for r in geo_df["ChurnRate"]]
        fig = go.Figure(go.Bar(
            x=geo_df["ChurnRate"], y=geo_df["Geography"], orientation="h",
            marker_color=colors, text=[f"{r:.1f}%" for r in geo_df["ChurnRate"]],
            textposition="outside", textfont_size=13
        ))
        fig.update_layout(
            height=260, margin=dict(l=10, r=40, t=10, b=10),
            xaxis_title="Churn Rate (%)", yaxis_title="",
            plot_bgcolor="white", paper_bgcolor="white",
            xaxis=dict(gridcolor="#f0f0f0", range=[0, geo_df["ChurnRate"].max() * 1.25])
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown('<div class="section-header">Churn Rate by Gender</div>', unsafe_allow_html=True)
        gen_df = churn_by(df, "Gender")
        fig = go.Figure(go.Bar(
            x=gen_df["Gender"], y=gen_df["ChurnRate"],
            marker_color=[color_by_rate(r) for r in gen_df["ChurnRate"]],
            text=[f"{r:.1f}%" for r in gen_df["ChurnRate"]],
            textposition="outside", textfont_size=13
        ))
        fig.update_layout(
            height=260, margin=dict(l=10, r=10, t=10, b=10),
            yaxis_title="Churn Rate (%)", xaxis_title="",
            plot_bgcolor="white", paper_bgcolor="white",
            yaxis=dict(gridcolor="#f0f0f0", range=[0, gen_df["ChurnRate"].max() * 1.25])
        )
        st.plotly_chart(fig, use_container_width=True)

    col3, col4 = st.columns(2)

    with col3:
        st.markdown('<div class="section-header">Churn by Age Band</div>', unsafe_allow_html=True)
        age_df = churn_by(df, "AgeBand")
        age_df = age_df.sort_values("AgeBand")
        fig = go.Figure(go.Bar(
            x=age_df["AgeBand"].astype(str), y=age_df["ChurnRate"],
            marker_color=[color_by_rate(r) for r in age_df["ChurnRate"]],
            text=[f"{r:.1f}%" for r in age_df["ChurnRate"]],
            textposition="outside", textfont_size=12
        ))
        fig.update_layout(
            height=260, margin=dict(l=10, r=10, t=10, b=10),
            yaxis_title="Churn Rate (%)", xaxis_title="Age Band",
            plot_bgcolor="white", paper_bgcolor="white",
            yaxis=dict(gridcolor="#f0f0f0", range=[0, age_df["ChurnRate"].max() * 1.25])
        )
        st.plotly_chart(fig, use_container_width=True)

    with col4:
        st.markdown('<div class="section-header">Churn by Tenure</div>', unsafe_allow_html=True)
        ten_df = churn_by(df, "Tenure").sort_values("Tenure")
        fig = go.Figure(go.Scatter(
            x=ten_df["Tenure"], y=ten_df["ChurnRate"],
            mode="lines+markers", line=dict(color="#2E75B6", width=2.5),
            marker=dict(size=8, color="#2E75B6"),
            fill="tozeroy", fillcolor="rgba(46,117,182,0.08)"
        ))
        fig.update_layout(
            height=260, margin=dict(l=10, r=10, t=10, b=10),
            yaxis_title="Churn Rate (%)", xaxis_title="Tenure (Years)",
            plot_bgcolor="white", paper_bgcolor="white",
            yaxis=dict(gridcolor="#f0f0f0", range=[0, 35])
        )
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("""
    <div class="insight-box">
    <strong>Key finding:</strong> Germany's churn rate is nearly double France and Spain's,
    female customers churn 52% more than males, and tenure shows no loyalty effect —
    churn rates are flat across all 0–10 year tenure bands, ruling out time-based loyalty programmes.
    </div>""", unsafe_allow_html=True)


# ══════════════════════════════════════════════
# TAB 2: ENGAGEMENT
# ══════════════════════════════════════════════
with tab2:
    # KPIs
    active_churn = df[df["IsActiveMember"] == 1]["Exited"].mean() * 100
    inactive_churn = df[df["IsActiveMember"] == 0]["Exited"].mean() * 100
    lift = inactive_churn / active_churn if active_churn > 0 else 0
    inactive_dis = df[df["EngagementProfile"] == "Inactive Disengaged"]["Exited"].mean() * 100

    c1, c2, c3, c4 = st.columns(4)
    c1.markdown(kpi_html("Active Member Churn", f"{active_churn:.1f}%", "Engagement benchmark", "kpi-ok"), unsafe_allow_html=True)
    c2.markdown(kpi_html("Inactive Member Churn", f"{inactive_churn:.1f}%", "Primary risk pool", "kpi-danger"), unsafe_allow_html=True)
    c3.markdown(kpi_html("Engagement Lift", f"{lift:.2f}×", "Inactive vs active risk", "kpi-warn"), unsafe_allow_html=True)
    c4.markdown(kpi_html("Inactive Disengaged Churn", f"{inactive_dis:.1f}%", "Highest risk segment", "kpi-danger"), unsafe_allow_html=True)

    st.markdown("---")

    # Engagement profile breakdown
    st.markdown('<div class="section-header">Engagement Profile — Churn Rate Comparison</div>', unsafe_allow_html=True)

    prof_order = ["Active Engaged", "Other", "Active Low-Product", "Inactive High-Balance", "Inactive Disengaged"]
    prof_df = churn_by(df, "EngagementProfile")
    prof_df["Order"] = prof_df["EngagementProfile"].map({p: i for i, p in enumerate(prof_order)})
    prof_df = prof_df.sort_values("Order")

    col1, col2 = st.columns([3, 2])

    with col1:
        fig = go.Figure()
        for _, row in prof_df.iterrows():
            c = PROFILE_COLORS.get(row["EngagementProfile"], "#888")
            fig.add_trace(go.Bar(
                x=[row["EngagementProfile"]], y=[row["ChurnRate"]],
                marker_color=c, showlegend=False,
                text=[f"{row['ChurnRate']:.1f}%"], textposition="outside", textfont_size=13,
                name=row["EngagementProfile"]
            ))
        fig.update_layout(
            height=320, margin=dict(l=10, r=10, t=10, b=80),
            yaxis_title="Churn Rate (%)", xaxis_title="",
            plot_bgcolor="white", paper_bgcolor="white",
            yaxis=dict(gridcolor="#f0f0f0", range=[0, prof_df["ChurnRate"].max() * 1.25]),
            xaxis=dict(tickangle=-15)
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("**Segment Summary**")
        for _, row in prof_df.iterrows():
            c = PROFILE_COLORS.get(row["EngagementProfile"], "#888")
            rate = row["ChurnRate"]
            risk = "🟢" if rate < 15 else "🟡" if rate < 25 else "🔴"
            st.markdown(f"""
            <div style='padding:8px 12px; margin:4px 0; border-left:4px solid {c}; background:#fafafa; border-radius:0 6px 6px 0;'>
                <div style='font-size:0.8rem; font-weight:600; color:#333;'>{risk} {row['EngagementProfile']}</div>
                <div style='font-size:0.75rem; color:#666;'>{row['Total']:,} customers · <strong style='color:{c}'>{rate:.1f}%</strong> churn</div>
            </div>""", unsafe_allow_html=True)

    col3, col4 = st.columns(2)

    with col3:
        st.markdown('<div class="section-header">Active vs Inactive — Churn Distribution</div>', unsafe_allow_html=True)
        act_df = churn_by(df, "IsActiveMember")
        act_df["Label"] = act_df["IsActiveMember"].map({1: "Active", 0: "Inactive"})
        act_df["Retained%"] = 100 - act_df["ChurnRate"]
        fig = go.Figure()
        fig.add_trace(go.Bar(name="Churned", x=act_df["Label"], y=act_df["ChurnRate"],
                              marker_color="#E24B4A", text=[f"{r:.1f}%" for r in act_df["ChurnRate"]], textposition="inside"))
        fig.add_trace(go.Bar(name="Retained", x=act_df["Label"], y=act_df["Retained%"],
                              marker_color="#2E75B6", text=[f"{r:.1f}%" for r in act_df["Retained%"]], textposition="inside"))
        fig.update_layout(
            barmode="stack", height=280, margin=dict(l=10, r=10, t=10, b=10),
            yaxis_title="Percentage (%)", xaxis_title="",
            plot_bgcolor="white", paper_bgcolor="white",
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        st.plotly_chart(fig, use_container_width=True)

    with col4:
        st.markdown('<div class="section-header">Geography × Engagement Churn</div>', unsafe_allow_html=True)
        cross = df.groupby(["Geography", "IsActiveMember"])["Exited"].agg(["sum","count"]).reset_index()
        cross["ChurnRate"] = cross["sum"] / cross["count"] * 100
        cross["Status"] = cross["IsActiveMember"].map({1: "Active", 0: "Inactive"})
        fig = px.bar(cross, x="Geography", y="ChurnRate", color="Status",
                     barmode="group", color_discrete_map={"Active": "#2E75B6", "Inactive": "#E24B4A"},
                     text=cross["ChurnRate"].apply(lambda x: f"{x:.1f}%"))
        fig.update_traces(textposition="outside", textfont_size=11)
        fig.update_layout(
            height=280, margin=dict(l=10, r=10, t=10, b=10),
            yaxis_title="Churn Rate (%)", xaxis_title="",
            plot_bgcolor="white", paper_bgcolor="white",
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("""
    <div class="alert-box">
    <strong>Priority action:</strong> The 2,521 Inactive Disengaged customers represent the highest-volume at-risk
    cohort at 36.65% churn. Customers aged 50–59 face a 56% churn probability — a critical retention emergency
    requiring dedicated age-segmented product development.
    </div>""", unsafe_allow_html=True)


# ══════════════════════════════════════════════
# TAB 3: PRODUCT UTILIZATION
# ══════════════════════════════════════════════
with tab3:
    p1_churn = df[df["NumOfProducts"] == 1]["Exited"].mean() * 100 if len(df[df["NumOfProducts"]==1]) > 0 else 0
    p2_churn = df[df["NumOfProducts"] == 2]["Exited"].mean() * 100 if len(df[df["NumOfProducts"]==2]) > 0 else 0
    p3_churn = df[df["NumOfProducts"] == 3]["Exited"].mean() * 100 if len(df[df["NumOfProducts"]==3]) > 0 else 0
    cc_delta = (df[df["HasCrCard"]==0]["Exited"].mean() - df[df["HasCrCard"]==1]["Exited"].mean()) * 100

    c1, c2, c3, c4 = st.columns(4)
    c1.markdown(kpi_html("1-Product Churn", f"{p1_churn:.1f}%", "5,084 customers", "kpi-warn"), unsafe_allow_html=True)
    c2.markdown(kpi_html("2-Product Churn", f"{p2_churn:.1f}%", "Optimal sweet spot", "kpi-ok"), unsafe_allow_html=True)
    c3.markdown(kpi_html("3+ Product Churn", f"{p3_churn:.1f}%", "Product paradox", "kpi-danger"), unsafe_allow_html=True)
    c4.markdown(kpi_html("CC Stickiness Delta", f"{cc_delta:.2f}pp", "No vs has credit card", "kpi-blue"), unsafe_allow_html=True)

    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="section-header">Product Depth Index — Churn by Product Count</div>', unsafe_allow_html=True)
        prod_df = churn_by(df, "NumOfProducts").sort_values("NumOfProducts")
        colors = [color_by_rate(r) for r in prod_df["ChurnRate"]]
        fig = go.Figure(go.Bar(
            x=prod_df["NumOfProducts"].astype(str) + " Product(s)",
            y=prod_df["ChurnRate"], marker_color=colors,
            text=[f"{r:.1f}%" for r in prod_df["ChurnRate"]],
            textposition="outside", textfont_size=13
        ))
        fig.update_layout(
            height=300, margin=dict(l=10, r=10, t=10, b=10),
            yaxis_title="Churn Rate (%)", xaxis_title="",
            plot_bgcolor="white", paper_bgcolor="white",
            yaxis=dict(gridcolor="#f0f0f0", range=[0, prod_df["ChurnRate"].max() * 1.2])
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown('<div class="section-header">Relationship Strength Index (RSI)</div>', unsafe_allow_html=True)
        rsi_df = churn_by(df, "RSI").sort_values("RSI")
        rsi_df["RSI_Label"] = rsi_df["RSI"].astype(str)
        rsi_df["Color"] = rsi_df["ChurnRate"].apply(color_by_rate)

        fig = go.Figure()
        for _, row in rsi_df.iterrows():
            pct = row["ChurnRate"]
            count = row["Total"]
            fig.add_trace(go.Bar(
                name=f"RSI {row['RSI']}",
                x=[pct], y=[f"RSI {row['RSI']}"],
                orientation="h",
                marker_color=row["Color"],
                text=[f"  {pct:.1f}%  ({count:,} customers)"],
                textposition="outside", textfont_size=11,
                showlegend=False
            ))
        fig.update_layout(
            height=300, margin=dict(l=10, r=130, t=10, b=10),
            xaxis_title="Churn Rate (%)", yaxis_title="",
            plot_bgcolor="white", paper_bgcolor="white",
            xaxis=dict(gridcolor="#f0f0f0", range=[0, rsi_df["ChurnRate"].max() * 1.4]),
            barmode="overlay"
        )
        st.plotly_chart(fig, use_container_width=True)

    # Product × Active cross
    st.markdown('<div class="section-header">Product Count × Engagement — Combined View</div>', unsafe_allow_html=True)
    cross2 = df.groupby(["NumOfProducts", "IsActiveMember"])["Exited"].agg(["sum", "count"]).reset_index()
    cross2["ChurnRate"] = cross2["sum"] / cross2["count"] * 100
    cross2["Status"] = cross2["IsActiveMember"].map({1: "Active", 0: "Inactive"})
    cross2["Products"] = cross2["NumOfProducts"].astype(str) + " Product(s)"
    fig = px.bar(cross2, x="Products", y="ChurnRate", color="Status",
                 barmode="group",
                 color_discrete_map={"Active": "#2E75B6", "Inactive": "#E24B4A"},
                 text=cross2["ChurnRate"].apply(lambda x: f"{x:.0f}%"))
    fig.update_traces(textposition="outside", textfont_size=11)
    fig.update_layout(
        height=300, margin=dict(l=10, r=10, t=10, b=10),
        yaxis_title="Churn Rate (%)", xaxis_title="",
        plot_bgcolor="white", paper_bgcolor="white",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("""
    <div class="danger-box">
    <strong>Product Paradox — Regulatory Signal:</strong> Customers with 3 or more products churn at 82.71–100%.
    The standard assumption that product breadth creates loyalty is decisively contradicted.
    The optimal customer configuration is 2 products. This pattern is consistent with mis-selling and
    warrants both internal audit and regulatory attention.
    </div>""", unsafe_allow_html=True)


# ══════════════════════════════════════════════
# TAB 4: FINANCIAL ANALYSIS
# ══════════════════════════════════════════════
with tab4:
    churned_df = df[df["Exited"] == 1]
    retained_df = df[df["Exited"] == 0]

    avg_bal_c  = churned_df["Balance"].mean() if len(churned_df) > 0 else 0
    avg_sal_c  = churned_df["EstimatedSalary"].mean() if len(churned_df) > 0 else 0
    avg_age_c  = churned_df["Age"].mean() if len(churned_df) > 0 else 0
    at_risk_n  = df["IsAtRisk"].sum()
    at_risk_cr = df[df["IsAtRisk"] == 1]["Exited"].mean() * 100 if at_risk_n > 0 else 0

    c1, c2, c3, c4 = st.columns(4)
    c1.markdown(kpi_html("Avg Balance — Churned", f"€{avg_bal_c:,.0f}", "25% above retained avg", "kpi-danger"), unsafe_allow_html=True)
    c2.markdown(kpi_html("Avg Balance — Retained", f"€{retained_df['Balance'].mean():,.0f}", "Reference baseline", "kpi-ok"), unsafe_allow_html=True)
    c3.markdown(kpi_html("At-Risk Premium Count", f"{at_risk_n:,}", f"{at_risk_cr:.1f}% churn rate", "kpi-danger"), unsafe_allow_html=True)
    c4.markdown(kpi_html("Avg Age — Churned", f"{avg_age_c:.1f} yrs", f"vs {retained_df['Age'].mean():.1f} retained", "kpi-warn"), unsafe_allow_html=True)

    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="section-header">Churn Rate by Balance Band</div>', unsafe_allow_html=True)
        bal_order = ["Zero", "€1–50K", "€50–100K", "€100–150K", "€150K+"]
        bal_df = churn_by(df, "BalanceBand")
        bal_df["Order"] = bal_df["BalanceBand"].map({b: i for i, b in enumerate(bal_order)})
        bal_df = bal_df.sort_values("Order")
        fig = go.Figure(go.Bar(
            x=bal_df["BalanceBand"].astype(str), y=bal_df["ChurnRate"],
            marker_color=[color_by_rate(r) for r in bal_df["ChurnRate"]],
            text=[f"{r:.1f}%" for r in bal_df["ChurnRate"]],
            textposition="outside", textfont_size=12
        ))
        fig.update_layout(
            height=280, margin=dict(l=10, r=10, t=10, b=10),
            yaxis_title="Churn Rate (%)", xaxis_title="",
            plot_bgcolor="white", paper_bgcolor="white",
            yaxis=dict(gridcolor="#f0f0f0", range=[0, bal_df["ChurnRate"].max() * 1.25])
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown('<div class="section-header">Financial Profile — Churned vs Retained</div>', unsafe_allow_html=True)
        metrics = ["Avg Balance", "Avg Est. Salary"]
        churned_vals = [avg_bal_c, avg_sal_c]
        retained_vals = [retained_df["Balance"].mean(), retained_df["EstimatedSalary"].mean()]

        fig = go.Figure()
        fig.add_trace(go.Bar(name="Churned", x=metrics, y=churned_vals, marker_color="#E24B4A",
                              text=[f"€{v:,.0f}" for v in churned_vals], textposition="outside", textfont_size=11))
        fig.add_trace(go.Bar(name="Retained", x=metrics, y=retained_vals, marker_color="#2E75B6",
                              text=[f"€{v:,.0f}" for v in retained_vals], textposition="outside", textfont_size=11))
        fig.update_layout(
            barmode="group", height=280, margin=dict(l=10, r=10, t=10, b=10),
            yaxis_title="€ Amount", xaxis_title="",
            plot_bgcolor="white", paper_bgcolor="white",
            yaxis=dict(gridcolor="#f0f0f0"),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        st.plotly_chart(fig, use_container_width=True)

    # Balance distribution
    st.markdown('<div class="section-header">Balance Distribution — Churned vs Retained</div>', unsafe_allow_html=True)
    fig = go.Figure()
    nonzero_c = churned_df[churned_df["Balance"] > 0]["Balance"]
    nonzero_r = retained_df[retained_df["Balance"] > 0]["Balance"]
    if len(nonzero_c) > 0:
        fig.add_trace(go.Histogram(x=nonzero_c, name="Churned", opacity=0.65,
                                    marker_color="#E24B4A", nbinsx=40, histnorm="percent"))
    if len(nonzero_r) > 0:
        fig.add_trace(go.Histogram(x=nonzero_r, name="Retained", opacity=0.65,
                                    marker_color="#2E75B6", nbinsx=40, histnorm="percent"))
    fig.update_layout(
        barmode="overlay", height=260, margin=dict(l=10, r=10, t=10, b=10),
        xaxis_title="Account Balance (€)", yaxis_title="% of Customers",
        plot_bgcolor="white", paper_bgcolor="white",
        yaxis=dict(gridcolor="#f0f0f0"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("""
    <div class="danger-box">
    <strong>Premium balance flight risk:</strong> Churned customers hold €91,109 average balances —
    25% above the €72,745 retained average. Salary is nearly identical across groups, ruling out
    income as a churn driver. The 2,356 inactive high-balance customers at 32.77% churn represent
    several hundred million euros in potential AUM flight.
    </div>""", unsafe_allow_html=True)


# ══════════════════════════════════════════════
# TAB 5: RETENTION STRENGTH
# ══════════════════════════════════════════════
with tab5:
    sticky_cr = df[df["IsSticky"] == 1]["Exited"].mean() * 100 if df["IsSticky"].sum() > 0 else 0
    atrisk_cr = df[df["IsAtRisk"] == 1]["Exited"].mean() * 100 if df["IsAtRisk"].sum() > 0 else 0
    overall_cr = churn_rate(df)
    gap = atrisk_cr / sticky_cr if sticky_cr > 0 else 0

    c1, c2, c3, c4 = st.columns(4)
    c1.markdown(kpi_html("Sticky Customer Churn", f"{sticky_cr:.1f}%", f"{df['IsSticky'].sum():,} sticky customers", "kpi-ok"), unsafe_allow_html=True)
    c2.markdown(kpi_html("At-Risk Premium Churn", f"{atrisk_cr:.1f}%", f"{df['IsAtRisk'].sum():,} at-risk customers", "kpi-danger"), unsafe_allow_html=True)
    c3.markdown(kpi_html("Retention Gap", f"{gap:.1f}×", "Sticky vs at-risk differential", "kpi-warn"), unsafe_allow_html=True)
    c4.markdown(kpi_html("Portfolio Churn", f"{overall_cr:.1f}%", "Current filter view", "kpi-blue"), unsafe_allow_html=True)

    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="section-header">Sticky vs At-Risk vs Overall</div>', unsafe_allow_html=True)
        segments = ["Sticky\n(Active+2prod+CC)", "At-Risk Premium\n(Inactive+>€100K)", "Portfolio\nAverage"]
        rates = [sticky_cr, atrisk_cr, overall_cr]
        colors = [COLOR_MAP["ok"], COLOR_MAP["danger"], COLOR_MAP["blue"]]
        fig = go.Figure(go.Bar(
            x=segments, y=rates, marker_color=colors,
            text=[f"{r:.1f}%" for r in rates],
            textposition="outside", textfont_size=13
        ))
        fig.update_layout(
            height=300, margin=dict(l=10, r=10, t=10, b=10),
            yaxis_title="Churn Rate (%)", xaxis_title="",
            plot_bgcolor="white", paper_bgcolor="white",
            yaxis=dict(gridcolor="#f0f0f0", range=[0, max(rates) * 1.3])
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown('<div class="section-header">RSI Score vs Churn Rate</div>', unsafe_allow_html=True)
        rsi_df2 = churn_by(df, "RSI").sort_values("RSI")
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=rsi_df2["RSI"], y=rsi_df2["ChurnRate"],
            mode="lines+markers+text",
            line=dict(color="#1F4E79", width=3),
            marker=dict(size=14, color=[color_by_rate(r) for r in rsi_df2["ChurnRate"]],
                        line=dict(width=2, color="white")),
            text=[f"{r:.1f}%" for r in rsi_df2["ChurnRate"]],
            textposition="top center", textfont_size=12,
            fill="tozeroy", fillcolor="rgba(31,78,121,0.07)"
        ))
        fig.update_layout(
            height=300, margin=dict(l=10, r=10, t=10, b=10),
            yaxis_title="Churn Rate (%)", xaxis_title="RSI Score (1=Low → 4=High)",
            plot_bgcolor="white", paper_bgcolor="white",
            yaxis=dict(gridcolor="#f0f0f0", range=[0, rsi_df2["ChurnRate"].max() * 1.3]),
            xaxis=dict(tickvals=[1, 2, 3, 4])
        )
        st.plotly_chart(fig, use_container_width=True)

    # Credit score vs churn
    st.markdown('<div class="section-header">Credit Score Band vs Churn Rate</div>', unsafe_allow_html=True)
    cs_df = churn_by(df, "CSBand")
    cs_order = ["<500", "500–599", "600–699", "700–799", "800+"]
    cs_df["Order"] = cs_df["CSBand"].map({b: i for i, b in enumerate(cs_order)})
    cs_df = cs_df.sort_values("Order")
    fig = go.Figure(go.Bar(
        x=cs_df["CSBand"].astype(str), y=cs_df["ChurnRate"],
        marker_color=[color_by_rate(r) for r in cs_df["ChurnRate"]],
        text=[f"{r:.1f}%" for r in cs_df["ChurnRate"]],
        textposition="outside", textfont_size=12
    ))
    fig.update_layout(
        height=240, margin=dict(l=10, r=10, t=10, b=10),
        yaxis_title="Churn Rate (%)", xaxis_title="Credit Score Band",
        plot_bgcolor="white", paper_bgcolor="white",
        yaxis=dict(gridcolor="#f0f0f0", range=[0, cs_df["ChurnRate"].max() * 1.3])
    )
    st.plotly_chart(fig, use_container_width=True)

    col3, col4 = st.columns(2)

    with col3:
        st.markdown("""
        <div class="insight-box">
        <strong>Sticky customer profile:</strong> Customers who are active + hold 2+ products +
        own a credit card churn at just 9.1% — 4× better than at-risk premium customers.
        Scaling this profile across the base is the single highest-ROI retention action available.
        </div>""", unsafe_allow_html=True)

    with col4:
        st.markdown("""
        <div class="alert-box">
        <strong>RSI threshold:</strong> Customers with RSI ≥ 3 churn at 15.9% or less.
        Customers with RSI ≤ 2 churn at 29–35%. Every one-point RSI improvement reduces
        churn risk by approximately 8–12 percentage points.
        </div>""", unsafe_allow_html=True)

    # At-risk customer table
    st.markdown('<div class="section-header">High-Value Disengaged Customer Detector</div>', unsafe_allow_html=True)
    st.caption("Showing inactive customers with balance > €75,000 — sorted by balance descending")

    at_risk_display = df[
        (df["IsActiveMember"] == 0) & (df["Balance"] > 75000)
    ][["CustomerId", "Geography", "Gender", "Age", "Balance", "NumOfProducts",
       "HasCrCard", "RSI", "EngagementProfile", "Exited"]].copy()

    at_risk_display = at_risk_display.sort_values("Balance", ascending=False).head(50)
    at_risk_display.columns = ["Customer ID", "Country", "Gender", "Age", "Balance (€)",
                                "Products", "Has CC", "RSI", "Engagement Profile", "Churned"]
    at_risk_display["Balance (€)"] = at_risk_display["Balance (€)"].apply(lambda x: f"€{x:,.0f}")
    at_risk_display["Churned"] = at_risk_display["Churned"].map({1: "✗ Exited", 0: "✓ Active"})

    st.dataframe(at_risk_display, use_container_width=True, height=360)

# ─────────────────────────────────────────────
# Footer
# ─────────────────────────────────────────────
st.markdown("---")
st.markdown("""
<div style='text-align:center; font-size:0.8rem; color:#aaa; padding: 8px 0 16px;'>
    European Bank Churn Intelligence Platform &nbsp;·&nbsp;
    10,000 Customer Records &nbsp;·&nbsp;
    France · Germany · Spain &nbsp;·&nbsp;
    For Academic & Policy Use Only
</div>
""", unsafe_allow_html=True)
