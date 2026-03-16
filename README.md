<div align="center">

# 🏦 European Bank — Customer Churn Intelligence

<img src="https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white"/>
<img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white"/>
<img src="https://img.shields.io/badge/Plotly-3F4F75?style=for-the-badge&logo=plotly&logoColor=white"/>
<img src="https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white"/>
<img src="https://img.shields.io/badge/Status-Complete-2ea44f?style=for-the-badge"/>

<br/><br/>

> **Reframing customer churn from a behavioral and relationship-strength perspective.**
> Built on 10,000 customer records across France, Germany & Spain.

</div>

---

## 📌 Project Overview
```
Dataset   →   EDA   →   Engagement Profiling   →   RSI Scoring   →   Streamlit Dashboard
10,000 rows    14 vars     5 segments              1–4 score          5 interactive tabs
```

This project reframes churn as a **relationship failure**, not a demographic inevitability.
The key insight: customers leave because they are **disengaged** — not because they can't afford to stay.

---

## 🗂️ Repository Contents
```
european-bank-churn-analysis/
│
├── 📊  European_Bank_Dashboard.py        ← Streamlit live analytics app
├── 📄  European_Bank_Research_Paper.docx ← Full EDA & academic paper
├── 📋  European_Bank_Executive_Summary.docx ← Government policy brief
└── 🗃️  European_Bank.csv                 ← Source dataset (10,000 records)
```

---

## 🚀 Run the Dashboard
```bash
# 1. Install dependencies
pip install streamlit pandas plotly numpy

# 2. Launch
streamlit run European_Bank_Dashboard.py
```

> Make sure `European_Bank.csv` is in the same directory.

---

## 📊 Key Findings at a Glance

| # | Finding | Metric | Signal |
|---|---------|--------|--------|
| 1 | Overall churn rate | **20.37%** | 🔴 Baseline risk |
| 2 | Germany churn | **32.44%** | 🔴 2× France & Spain |
| 3 | Active member churn | **14.27%** | 🟢 Engagement works |
| 4 | Inactive member churn | **26.85%** | 🔴 Primary risk pool |
| 5 | 2-product churn | **7.58%** | 🟢 Sweet spot |
| 6 | 3-product churn | **82.71%** | 🚨 Mis-selling signal |
| 7 | Age 50–59 churn | **56.04%** | 🔴 Critical cohort |
| 8 | Sticky customer churn | **9.12%** | 🟢 Best-in-class |
| 9 | At-risk premium churn | **32.77%** | 🔴 AUM flight risk |
| 10 | Churned avg balance | **€91,109** | 🔴 25% above retained |

---

## 👥 Engagement Profiles
```
╔══════════════════════════════╦════════╦══════════════╗
║ Profile                      ║   n    ║  Churn Rate  ║
╠══════════════════════════════╬════════╬══════════════╣
║ 🟢 Active Engaged            ║  2,588 ║    9.66%     ║
║ 🟢 Other                     ║  1,549 ║   10.52%     ║
║ 🟡 Active Low-Product        ║  2,563 ║   18.92%     ║
║ 🔴 Inactive High-Balance     ║    779 ║   27.60%     ║
║ 🔴 Inactive Disengaged       ║  2,521 ║   36.65%     ║
╚══════════════════════════════╩════════╩══════════════╝
```

---

## 🧮 Relationship Strength Index (RSI)
```
RSI  =  IsActiveMember  +  min(NumOfProducts, 2)  +  HasCrCard
```
```
RSI 1  ████████████████████████████████████  34.54% churn  🔴
RSI 2  ████████████████████████████░░░░░░░░  29.26% churn  🔴
RSI 3  ████████████████░░░░░░░░░░░░░░░░░░░░  15.90% churn  🟡
RSI 4  █████████░░░░░░░░░░░░░░░░░░░░░░░░░░░   9.12% churn  🟢
```

> Every +1 RSI point reduces churn risk by **8–12 percentage points**.

---

## 🎯 Strategic Recommendations

| Priority | Action | Target |
|----------|--------|--------|
| 🔴 P1 | Re-engage 2,356 inactive high-balance customers | < 24% churn |
| 🔴 P1 | Audit all 3+ product customers for mis-selling | Zero 4-product accounts |
| 🟡 P2 | Germany Retention Task Force | < 24% churn |
| 🟡 P2 | Senior Wealth Programme for age 50–59 | < 35% churn |
| 🟢 P3 | Optimise cross-sell to 2-product sweet spot | +30% 2-product base |
| 🟢 P3 | Deploy RSI early warning system in CRM | 100% RSI 1–2 flagged |

---

## 📦 Dashboard Modules

| Tab | Module | Key Visual |
|-----|--------|------------|
| 📊 | Overview | Geo, gender, age, tenure churn charts |
| 👥 | Engagement | 5-profile segmentation + activity cross-analysis |
| 📦 | Product Utilization | Product depth index + RSI bar chart |
| 💰 | Financial Analysis | Balance bands + churned vs retained profiles |
| 🛡️ | Retention Strength | Sticky detector + at-risk customer live table |

---

## 🛠️ Tech Stack

<div align="center">

<img src="https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white"/>
<img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=flat-square&logo=streamlit&logoColor=white"/>
<img src="https://img.shields.io/badge/Plotly-3F4F75?style=flat-square&logo=plotly&logoColor=white"/>
<img src="https://img.shields.io/badge/Pandas-150458?style=flat-square&logo=pandas&logoColor=white"/>
<img src="https://img.shields.io/badge/NumPy-013243?style=flat-square&logo=numpy&logoColor=white"/>
<img src="https://img.shields.io/badge/Microsoft_Word-2B579A?style=flat-square&logo=microsoft-word&logoColor=white"/>

</div>

---

<div align="center">

📁 **Dataset:** European Bank (anonymised) &nbsp;·&nbsp; 👤 **Records:** 10,000 &nbsp;·&nbsp; 🌍 **Markets:** France · Germany · Spain

*Course Project · FY 2024 · For Academic Use*

</div>
