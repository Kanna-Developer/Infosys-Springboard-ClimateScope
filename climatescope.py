import os
import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

# =========================================================
# PAGE CONFIG
# =========================================================
st.set_page_config(
    page_title="ClimateScope X",
    page_icon="🌦️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =========================================================
# CUSTOM CSS - PRO UI
# =========================================================
st.markdown("""
<style>
    :root {
        --bg1: #0a0f1f;
        --bg2: #0f172a;
        --card: rgba(15, 23, 42, 0.68);
        --card-2: rgba(17, 24, 39, 0.72);
        --border: rgba(255,255,255,0.08);
        --text: #E5E7EB;
        --muted: #94A3B8;
        --cyan: #22D3EE;
        --violet: #A78BFA;
        --pink: #F472B6;
        --green: #22C55E;
        --orange: #F97316;
        --red: #EF4444;
    }

    html, body, [class*="css"] {
        font-family: 'Segoe UI', sans-serif;
    }

    .stApp {
        background:
            radial-gradient(circle at 10% 10%, rgba(34,211,238,0.08), transparent 22%),
            radial-gradient(circle at 90% 10%, rgba(167,139,250,0.08), transparent 24%),
            radial-gradient(circle at 50% 100%, rgba(244,114,182,0.05), transparent 25%),
            linear-gradient(135deg, var(--bg1) 0%, #0f172a 45%, #111827 100%);
        color: var(--text);
    }

    .block-container {
        max-width: 1450px;
        padding-top: 1rem !important;
        padding-bottom: 2rem !important;
    }

    /* Hide default radio label spacing */
    div[data-testid="stRadio"] > label {
        display: none !important;
    }

    /* Top Nav */
    div[role="radiogroup"] {
        display: flex !important;
        flex-wrap: wrap;
        gap: 10px;
        justify-content: center;
        align-items: center;
        padding: 10px 12px;
        border-radius: 22px;
        background: rgba(15,23,42,0.55);
        border: 1px solid rgba(255,255,255,0.06);
        backdrop-filter: blur(16px);
        box-shadow: 0 0 25px rgba(34,211,238,0.06);
        margin-bottom: 18px;
    }

    div[role="radiogroup"] label {
        background: linear-gradient(135deg, rgba(30,41,59,0.92), rgba(15,23,42,0.88));
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 16px;
        padding: 10px 16px !important;
        min-height: 46px;
        display: flex !important;
        align-items: center;
        justify-content: center;
        transition: all 0.22s ease;
        box-shadow: inset 0 0 0 rgba(0,0,0,0);
    }

    div[role="radiogroup"] label:hover {
        transform: translateY(-1px);
        border-color: rgba(34,211,238,0.35);
        box-shadow: 0 0 14px rgba(34,211,238,0.12);
    }

    /* Hero */
    .hero-shell {
        position: relative;
        overflow: hidden;
        border-radius: 28px;
        padding: 28px;
        margin-bottom: 18px;
        background:
            linear-gradient(135deg, rgba(17,24,39,0.78), rgba(15,23,42,0.78));
        border: 1px solid rgba(255,255,255,0.08);
        backdrop-filter: blur(18px);
        box-shadow: 0 0 28px rgba(34,211,238,0.08);
    }

    .hero-shell::before {
        content: "";
        position: absolute;
        inset: -30%;
        background:
            radial-gradient(circle, rgba(34,211,238,0.08) 0%, transparent 25%),
            radial-gradient(circle at 80% 20%, rgba(167,139,250,0.08) 0%, transparent 22%);
        pointer-events: none;
    }

    .hero-title {
        font-size: 2.6rem;
        font-weight: 900;
        line-height: 1.1;
        margin-bottom: 8px;
        background: linear-gradient(90deg, #22d3ee, #a78bfa, #f472b6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .hero-sub {
        color: #CBD5E1;
        font-size: 1rem;
        line-height: 1.6;
        max-width: 900px;
    }

    .hero-chip-row {
        display: flex;
        gap: 10px;
        flex-wrap: wrap;
        margin-top: 14px;
    }

    .hero-chip {
        padding: 8px 12px;
        border-radius: 999px;
        background: rgba(30,41,59,0.7);
        border: 1px solid rgba(255,255,255,0.07);
        color: #E2E8F0;
        font-size: 0.85rem;
    }

    /* Cards */
    .metric-card {
        background: rgba(15,23,42,0.64);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 22px;
        padding: 16px 18px;
        min-height: 120px;
        backdrop-filter: blur(14px);
        box-shadow: 0 0 16px rgba(34,211,238,0.06);
    }

    .metric-label {
        color: #94A3B8;
        font-size: 0.92rem;
        margin-bottom: 6px;
    }

    .metric-value {
        font-size: 1.9rem;
        font-weight: 900;
        color: #F8FAFC;
    }

    .metric-note {
        margin-top: 6px;
        color: #22D3EE;
        font-size: 0.84rem;
    }

    .section-box {
        background: rgba(15,23,42,0.54);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 24px;
        padding: 18px;
        margin-top: 12px;
        margin-bottom: 18px;
        backdrop-filter: blur(12px);
    }

    .section-title {
        font-size: 1.45rem;
        font-weight: 800;
        color: #F1F5F9;
        margin-bottom: 6px;
    }

    .section-sub {
        color: #94A3B8;
        font-size: 0.96rem;
        margin-bottom: 12px;
    }

    .insight-card {
        background: linear-gradient(135deg, rgba(30,41,59,0.8), rgba(15,23,42,0.78));
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 18px;
        padding: 14px 16px;
        margin-bottom: 10px;
        color: #E2E8F0;
    }

    .footer-note {
        text-align: center;
        color: #64748B;
        font-size: 0.9rem;
        margin-top: 14px;
    }

    /* Streamlit widget polish */
    .stSelectbox > div > div,
    .stSlider > div > div {
        border-radius: 14px !important;
    }
</style>
""", unsafe_allow_html=True)

# =========================================================
# DATA LOAD
# =========================================================
@st.cache_data(show_spinner=False)
def load_data():
    possible_paths = [
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "GlobalWeatherRepository.csv"),
        "GlobalWeatherRepository.csv"
    ]

    df = None
    for p in possible_paths:
        if os.path.exists(p):
            df = pd.read_csv(p)
            break

    if df is None:
        st.error("❌ GlobalWeatherRepository.csv not found. Keep it in same folder as app.py")
        st.stop()

    df.columns = [c.strip() for c in df.columns]

    if "last_updated" in df.columns:
        df["last_updated"] = pd.to_datetime(df["last_updated"], errors="coerce")

    required = ["country", "temperature_celsius", "humidity", "wind_kph", "pressure_mb"]
    missing = [c for c in required if c not in df.columns]
    if missing:
        st.error(f"❌ Missing required columns: {missing}")
        st.stop()

    optional_defaults = {
        "precip_mm": 0,
        "uv_index": 0,
        "condition_text": "Unknown",
        "feelslike_c": np.nan,
        "visibility_km": np.nan,
        "cloud": np.nan,
        "gust_kph": np.nan,
        "dewpoint_c": np.nan,
        "latitude": np.nan,
        "longitude": np.nan,
        "lat": np.nan,
        "lon": np.nan
    }

    for col, default in optional_defaults.items():
        if col not in df.columns:
            df[col] = default

    numeric_cols = [
        "temperature_celsius", "humidity", "wind_kph", "pressure_mb",
        "precip_mm", "uv_index", "feelslike_c", "visibility_km",
        "cloud", "gust_kph", "dewpoint_c", "latitude", "longitude", "lat", "lon"
    ]
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df = df.dropna(subset=["country", "temperature_celsius", "humidity", "wind_kph", "pressure_mb"])

    return df


# =========================================================
# PREPROCESS
# =========================================================
@st.cache_data(show_spinner=False)
def preprocess(df):
    summary = (
        df.groupby("country", as_index=False)
        .agg({
            "temperature_celsius": "mean",
            "humidity": "mean",
            "wind_kph": "mean",
            "pressure_mb": "mean",
            "precip_mm": "mean",
            "uv_index": "mean",
            "feelslike_c": "mean",
            "visibility_km": "mean"
        })
        .round(2)
    )

    temp_risk = np.clip((summary["temperature_celsius"] / 50) * 35, 0, 35)
    humidity_risk = np.clip((summary["humidity"] / 100) * 20, 0, 20)
    wind_risk = np.clip((summary["wind_kph"] / 100) * 20, 0, 20)
    precip_risk = np.clip((summary["precip_mm"] / 50) * 15, 0, 15)
    uv_risk = np.clip((summary["uv_index"] / 15) * 10, 0, 10)

    summary["risk_score"] = (temp_risk + humidity_risk + wind_risk + precip_risk + uv_risk).round(1)

    return summary


df = load_data()
summary = preprocess(df)

# =========================================================
# HELPERS
# =========================================================
def metric_card(label, value, note):
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">{label}</div>
        <div class="metric-value">{value}</div>
        <div class="metric-note">{note}</div>
    </div>
    """, unsafe_allow_html=True)

def section_header(title, subtitle):
    st.markdown('<div class="section-box">', unsafe_allow_html=True)
    st.markdown(f'<div class="section-title">{title}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="section-sub">{subtitle}</div>', unsafe_allow_html=True)

def section_close():
    st.markdown('</div>', unsafe_allow_html=True)

def risk_label(score):
    if score >= 70:
        return "🔴 High Risk"
    elif score >= 45:
        return "🟠 Moderate Risk"
    return "🟢 Low Risk"

def plot_layout(title, h=500):
    return dict(
        title=title,
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#E5E7EB"),
        margin=dict(l=20, r=20, t=60, b=20),
        height=h
    )

def similarity_score(summary_df, c1, c2):
    r1 = summary_df[summary_df["country"] == c1]
    r2 = summary_df[summary_df["country"] == c2]
    if r1.empty or r2.empty:
        return 0.0

    metrics = ["temperature_celsius", "humidity", "wind_kph", "pressure_mb", "precip_mm", "uv_index"]
    diffs = []
    for m in metrics:
        v1 = r1[m].values[0]
        v2 = r2[m].values[0]
        if pd.isna(v1) or pd.isna(v2):
            continue
        diffs.append(abs(v1 - v2))

    if not diffs:
        return 0.0

    normalized = min(np.mean(diffs), 100)
    return round(max(0, 100 - normalized), 1)

def best_geo_columns(df_):
    lat_col = None
    lon_col = None
    for c in ["latitude", "lat"]:
        if c in df_.columns and df_[c].notna().any():
            lat_col = c
            break
    for c in ["longitude", "lon"]:
        if c in df_.columns and df_[c].notna().any():
            lon_col = c
            break
    return lat_col, lon_col


# =========================================================
# HERO
# =========================================================
st.markdown("""
<div class="hero-shell">
    <div class="hero-title">🌦️ClimateScope X</div>
    <div class="hero-sub">
        A premium climate intelligence studio built for interactive global weather analysis, dynamic risk exploration,
        country-level storytelling.
    </div>
    <div class="hero-chip-row">
        <div class="hero-chip">⚡ Fast Cached Loading</div>
        <div class="hero-chip">🧠 Dynamic Risk Logic</div>
        <div class="hero-chip">📊 Premium Plotly Visuals</div>
        <div class="hero-chip">🎓 Explanation Ready</div>
        <div class="hero-chip">🌌 Dark Neon Glass UI</div>
    </div>
</div>
""", unsafe_allow_html=True)

# =========================================================
# TOP NAV (BOOKMARK FEEL)
# =========================================================
view = st.radio(
    "topnav",
    ["🌐 Global Command", "🔎 Country Studio", "⚠️ Risk Reactor", "⚖️ Twin Compare", "🛰 Geo View", "📖 Story Deck", "🎓 About"],
    horizontal=True,
    label_visibility="collapsed"
)

# =========================================================
# GLOBAL METRICS STRIP
# =========================================================
avg_temp = summary["temperature_celsius"].mean()
avg_humidity = summary["humidity"].mean()
avg_wind = summary["wind_kph"].mean()
avg_risk = summary["risk_score"].mean()

m1, m2, m3, m4 = st.columns(4)
with m1:
    metric_card("🌡 Avg Global Temp", f"{avg_temp:.1f}°C", "Thermal overview")
with m2:
    metric_card("💧 Avg Humidity", f"{avg_humidity:.1f}%", "Moisture profile")
with m3:
    metric_card("💨 Avg Wind", f"{avg_wind:.1f} kph", "Atmospheric flow")
with m4:
    metric_card("⚠️ Avg Risk", f"{avg_risk:.1f}/100", risk_label(avg_risk))

# =========================================================
# 1. GLOBAL COMMAND
# =========================================================
if view == "🌐 Global Command":
    section_header("🌐 Global Command", "A command-center style overview of climate intensity, outliers, and risk concentration across countries.")

    c1, c2 = st.columns([1.7, 1])

    with c1:
        metric_choice = st.selectbox(
            "Choose spotlight metric",
            ["temperature_celsius", "humidity", "wind_kph", "pressure_mb", "precip_mm", "uv_index", "risk_score"]
        )

        top_n = st.slider("Countries to spotlight", 5, min(30, len(summary)), 12)

        top_df = summary.sort_values(metric_choice, ascending=False).head(top_n)

        fig_spot = px.bar(
            top_df,
            x="country",
            y=metric_choice,
            color=metric_choice,
            text=metric_choice,
            color_continuous_scale="Turbo"
        )
        fig_spot.update_traces(textposition="outside")
        fig_spot.update_layout(**plot_layout(f"🔥 Spotlight Ranking: {metric_choice.replace('_', ' ').title()}"))
        st.plotly_chart(fig_spot, use_container_width=True)

    with c2:
        fig_g = go.Figure(go.Indicator(
            mode="gauge+number",
            value=float(avg_risk),
            title={"text": "Global Climate Pressure"},
            gauge={
                "axis": {"range": [0, 100]},
                "bar": {"color": "#22D3EE"},
                "steps": [
                    {"range": [0, 45], "color": "rgba(34,197,94,0.22)"},
                    {"range": [45, 70], "color": "rgba(249,115,22,0.22)"},
                    {"range": [70, 100], "color": "rgba(239,68,68,0.22)"}
                ]
            }
        ))
        fig_g.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", height=500)
        st.plotly_chart(fig_g, use_container_width=True)

    c3, c4 = st.columns(2)

    with c3:
        fig_bubble = px.scatter(
            summary,
            x="humidity",
            y="temperature_celsius",
            size="wind_kph",
            color="risk_score",
            hover_name="country",
            color_continuous_scale="Plasma"
        )
        fig_bubble.update_layout(**plot_layout("🌦 Climate Bubble Matrix"))
        st.plotly_chart(fig_bubble, use_container_width=True)

    with c4:
        fig_tree = px.treemap(
            summary,
            path=["country"],
            values="risk_score",
            color="risk_score",
            color_continuous_scale="RdYlGn_r"
        )
        fig_tree.update_layout(
            title="🧭 Risk Density Treemap",
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            height=500,
            margin=dict(l=10, r=10, t=50, b=10)
        )
        st.plotly_chart(fig_tree, use_container_width=True)

    st.markdown("""
    <div class="insight-card">
        <b>Why this section is unique:</b> Instead of a normal dashboard homepage, this acts like a climate command center —
        one selected metric becomes the "spotlight", while supporting visuals reveal pressure zones, outliers, and climate intensity patterns.
    </div>
    """, unsafe_allow_html=True)

    section_close()

# =========================================================
# 2. COUNTRY STUDIO
# =========================================================
elif view == "🔎 Country Studio":
    section_header("🔎 Country Studio", "A large immersive country exploration page with trend analysis, climate fingerprint, and explainable insights.")

    countries = sorted(df["country"].dropna().unique())
    selected = st.selectbox("Choose country", countries)

    cdf = df[df["country"] == selected].copy()
    srow = summary[summary["country"] == selected].iloc[0]

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        metric_card("🌡 Temperature", f"{srow['temperature_celsius']:.1f}°C", "Average condition")
    with c2:
        metric_card("💧 Humidity", f"{srow['humidity']:.1f}%", "Moisture behavior")
    with c3:
        metric_card("💨 Wind", f"{srow['wind_kph']:.1f} kph", "Atmospheric motion")
    with c4:
        metric_card("⚠️ Risk", f"{srow['risk_score']:.1f}/100", risk_label(srow['risk_score']))

    left, right = st.columns([1.55, 1])

    with left:
        if "last_updated" in cdf.columns and cdf["last_updated"].notna().any():
            cdf = cdf.sort_values("last_updated")
            fig_line = go.Figure()
            fig_line.add_trace(go.Scatter(
                x=cdf["last_updated"], y=cdf["temperature_celsius"],
                mode="lines+markers", name="Temperature °C"
            ))
            fig_line.add_trace(go.Scatter(
                x=cdf["last_updated"], y=cdf["humidity"],
                mode="lines+markers", name="Humidity %"
            ))
            fig_line.add_trace(go.Scatter(
                x=cdf["last_updated"], y=cdf["wind_kph"],
                mode="lines", name="Wind kph"
            ))
            fig_line.update_layout(**plot_layout(f"📈 {selected} Multi-Variable Climate Timeline", h=540))
            st.plotly_chart(fig_line, use_container_width=True)
        else:
            fig_dist = px.histogram(
                cdf, x="temperature_celsius", nbins=25,
                color_discrete_sequence=["#22D3EE"]
            )
            fig_dist.update_layout(**plot_layout(f"📊 {selected} Temperature Distribution", h=540))
            st.plotly_chart(fig_dist, use_container_width=True)

    with right:
        radar = pd.DataFrame({
            "metric": ["Temp", "Humidity", "Wind", "Pressure", "Precip", "UV"],
            "value": [
                srow["temperature_celsius"],
                srow["humidity"],
                srow["wind_kph"],
                srow["pressure_mb"] / 20,
                srow["precip_mm"] * 2,
                srow["uv_index"] * 6
            ]
        })

        fig_rad = go.Figure()
        fig_rad.add_trace(go.Scatterpolar(
            r=radar["value"],
            theta=radar["metric"],
            fill="toself",
            name=selected
        ))
        fig_rad.update_layout(
            title=f"🧬 {selected} Climate Fingerprint",
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            polar=dict(bgcolor="rgba(0,0,0,0)"),
            height=540
        )
        st.plotly_chart(fig_rad, use_container_width=True)

    c5, c6 = st.columns(2)
    with c5:
        fig_box = px.box(
            cdf,
            y="temperature_celsius",
            points="all",
            color_discrete_sequence=["#A78BFA"]
        )
        fig_box.update_layout(**plot_layout(f"🌡 {selected} Temperature Spread", h=420))
        st.plotly_chart(fig_box, use_container_width=True)

    with c6:
        cond_df = (
            cdf["condition_text"]
            .fillna("Unknown")
            .value_counts()
            .rename_axis("Condition")
            .reset_index(name="Count")
        )

    fig_cond = px.pie(
        cond_df,
        names="Condition",
        values="Count",
        hole=0.35
    )
    fig_cond.update_traces(textinfo="percent+label")
    fig_cond.update_layout(
        title=f"☁️ {selected} Condition Mix",
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=420
    )
    st.plotly_chart(fig_cond, use_container_width=True)

    with st.expander("🧠 Explain this country page", expanded=False):
        st.write(f"""
        This page creates a full country-specific climate profile for **{selected}**.

        What it shows:
        - A large multi-variable trend chart (temperature, humidity, wind)
        - A radar chart that acts like a climate fingerprint
        - A distribution chart to show spread/variation
        - A weather condition composition chart
        - A derived risk score to simplify interpretation

        Why it matters:
        - It transforms raw weather records into a country-level behavioral view.
        - It is easier to explain than isolated charts.
        """)

    section_close()

# =========================================================
# 3. RISK REACTOR
# =========================================================
elif view == "⚠️ Risk Reactor":
    section_header("⚠️ Risk Reactor", "An interactive simulation lab where the importance of each climate factor can be changed live to see how rankings shift.")

    c1, c2, c3 = st.columns(3)
    with c1:
        w_temp = st.slider("Temperature Influence", 10, 50, 35)
    with c2:
        w_hum = st.slider("Humidity Influence", 5, 30, 20)
    with c3:
        w_wind = st.slider("Wind Influence", 5, 30, 20)

    c4, c5 = st.columns(2)
    with c4:
        w_prec = st.slider("Precipitation Influence", 5, 25, 15)
    with c5:
        w_uv = st.slider("UV Influence", 5, 20, 10)

    total = w_temp + w_hum + w_wind + w_prec + w_uv

    lab = summary.copy()
    lab["dynamic_risk"] = (
        np.clip((lab["temperature_celsius"] / 50) * w_temp, 0, w_temp) +
        np.clip((lab["humidity"] / 100) * w_hum, 0, w_hum) +
        np.clip((lab["wind_kph"] / 100) * w_wind, 0, w_wind) +
        np.clip((lab["precip_mm"] / 50) * w_prec, 0, w_prec) +
        np.clip((lab["uv_index"] / 15) * w_uv, 0, w_uv)
    )
    lab["dynamic_risk"] = (lab["dynamic_risk"] / total * 100).round(1)

    c6, c7 = st.columns([1.8, 1])

    with c6:
        topk = st.slider("Show top risky countries", 5, min(25, len(lab)), 12)
        risky = lab.sort_values("dynamic_risk", ascending=False).head(topk)

        fig_risk = px.bar(
            risky,
            x="country",
            y="dynamic_risk",
            color="dynamic_risk",
            text="dynamic_risk",
            color_continuous_scale="Inferno"
        )
        fig_risk.update_traces(textposition="outside")
        fig_risk.update_layout(**plot_layout("🚨 Dynamic Risk Leaderboard", h=540))
        st.plotly_chart(fig_risk, use_container_width=True)

    with c7:
        avg_dyn = float(lab["dynamic_risk"].mean())
        fig_g2 = go.Figure(go.Indicator(
            mode="gauge+number",
            value=avg_dyn,
            title={"text": "Dynamic Pressure"},
            gauge={
                "axis": {"range": [0, 100]},
                "bar": {"color": "#A78BFA"},
                "steps": [
                    {"range": [0, 45], "color": "rgba(34,197,94,0.22)"},
                    {"range": [45, 70], "color": "rgba(249,115,22,0.22)"},
                    {"range": [70, 100], "color": "rgba(239,68,68,0.22)"}
                ]
            }
        ))
        fig_g2.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", height=540)
        st.plotly_chart(fig_g2, use_container_width=True)

    fig_heat = px.density_heatmap(
        lab,
        x="temperature_celsius",
        y="humidity",
        z="dynamic_risk",
        histfunc="avg",
        color_continuous_scale="Magma"
    )
    fig_heat.update_layout(**plot_layout("🌡💧 Dynamic Risk Heat Surface", h=450))
    st.plotly_chart(fig_heat, use_container_width=True)

    st.markdown("""
    <div class="insight-card">
        <b>Why this is standout:</b> This is not a static risk score. It behaves like a small simulation engine.
        When we changes factor weights, the risk ranking changes instantly. That makes the project feel analytical and decision-oriented.
    </div>
    """, unsafe_allow_html=True)

    section_close()

# =========================================================
# 4. TWIN COMPARE
# =========================================================
elif view == "⚖️ Twin Compare":
    section_header("⚖️ Twin Compare", "A premium side-by-side nation comparison module with similarity score, grouped metrics, and dual fingerprint view.")

    countries = sorted(summary["country"].unique())
    c1, c2 = st.columns(2)
    with c1:
        a = st.selectbox("Country A", countries, index=0)
    with c2:
        b = st.selectbox("Country B", countries, index=1 if len(countries) > 1 else 0)

    ra = summary[summary["country"] == a].iloc[0]
    rb = summary[summary["country"] == b].iloc[0]

    sim = similarity_score(summary, a, b)
    st.success(f"🔗 Climate Similarity Index: {sim}/100")

    comp = pd.DataFrame({
        "Metric": ["Temp", "Humidity", "Wind", "Pressure", "Precip", "UV", "Risk"],
        a: [ra["temperature_celsius"], ra["humidity"], ra["wind_kph"], ra["pressure_mb"], ra["precip_mm"], ra["uv_index"], ra["risk_score"]],
        b: [rb["temperature_celsius"], rb["humidity"], rb["wind_kph"], rb["pressure_mb"], rb["precip_mm"], rb["uv_index"], rb["risk_score"]]
    })

    c3, c4 = st.columns(2)

    with c3:
        fig_bar = go.Figure()
        fig_bar.add_trace(go.Bar(name=a, x=comp["Metric"], y=comp[a]))
        fig_bar.add_trace(go.Bar(name=b, x=comp["Metric"], y=comp[b]))
        fig_bar.update_layout(**plot_layout(f"📊 {a} vs {b} Metric Battle", h=520), barmode="group")
        st.plotly_chart(fig_bar, use_container_width=True)

    with c4:
        fig_rad2 = go.Figure()
        fig_rad2.add_trace(go.Scatterpolar(r=comp[a], theta=comp["Metric"], fill="toself", name=a))
        fig_rad2.add_trace(go.Scatterpolar(r=comp[b], theta=comp["Metric"], fill="toself", name=b))
        fig_rad2.update_layout(
            title="🧬 Dual Climate Fingerprint",
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            polar=dict(bgcolor="rgba(0,0,0,0)"),
            height=520
        )
        st.plotly_chart(fig_rad2, use_container_width=True)

    diff_df = pd.DataFrame({
        "Metric": comp["Metric"],
        "Difference": np.abs(comp[a] - comp[b]).round(2)
    })

    fig_diff = px.bar(
        diff_df,
        x="Metric",
        y="Difference",
        color="Difference",
        text="Difference",
        color_continuous_scale="Tealgrn"
    )
    fig_diff.update_traces(textposition="outside")
    fig_diff.update_layout(**plot_layout("📏 Absolute Difference Profile", h=420))
    st.plotly_chart(fig_diff, use_container_width=True)

    section_close()

# =========================================================
# 5. GEO VIEW
# =========================================================
elif view == "🛰 Geo View":
    section_header("🛰 Geo View", "A map-centric visual layer for spatial exploration. If coordinates exist, you get a glowing geographic climate spread.")

    lat_col, lon_col = best_geo_columns(df)

    if lat_col and lon_col:
        geo_df = (
            df.dropna(subset=[lat_col, lon_col])
              .groupby("country", as_index=False)
              .agg({
                  lat_col: "mean",
                  lon_col: "mean",
                  "temperature_celsius": "mean",
                  "humidity": "mean",
                  "wind_kph": "mean"
              })
              .round(3)
        )

        fig_map = px.scatter_geo(
            geo_df,
            lat=lat_col,
            lon=lon_col,
            color="temperature_celsius",
            size="wind_kph",
            hover_name="country",
            hover_data={"humidity": True, "temperature_celsius": True, "wind_kph": True},
            projection="natural earth",
            color_continuous_scale="Turbo"
        )
        fig_map.update_layout(
            title="🌍 Geo Climate Signal Map",
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            geo=dict(
                bgcolor="rgba(0,0,0,0)",
                showland=True,
                landcolor="rgba(148,163,184,0.10)",
                showocean=True,
                oceancolor="rgba(34,211,238,0.04)"
            ),
            height=650,
            margin=dict(l=10, r=10, t=60, b=10)
        )
        st.plotly_chart(fig_map, use_container_width=True)

        c1, c2 = st.columns(2)

        with c1:
            fig_geo_sc = px.scatter(
                geo_df,
                x="humidity",
                y="temperature_celsius",
                size="wind_kph",
                color="temperature_celsius",
                hover_name="country",
                color_continuous_scale="Turbo"
            )
            fig_geo_sc.update_layout(**plot_layout("🌐 Spatial Climate Cluster View", h=430))
            st.plotly_chart(fig_geo_sc, use_container_width=True)

        with c2:
            fig_geo_bar = px.bar(
                geo_df.sort_values("temperature_celsius", ascending=False).head(12),
                x="country",
                y="temperature_celsius",
                color="temperature_celsius",
                text="temperature_celsius",
                color_continuous_scale="Turbo"
            )
            fig_geo_bar.update_traces(textposition="outside")
            fig_geo_bar.update_layout(**plot_layout("🔥 Hottest Geo-Tagged Countries", h=430))
            st.plotly_chart(fig_geo_bar, use_container_width=True)
    else:
        st.warning("⚠️ No usable latitude/longitude columns found (`latitude/longitude` or `lat/lon`). Geo View needs coordinates.")
        st.info("If your dataset has coordinates, keep columns named: latitude + longitude OR lat + lon")

    section_close()

# =========================================================
# 6. STORY DECK
# =========================================================
elif view == "📖 Story Deck":
    section_header("📖 Story Deck", "A narrative-first climate storytelling page that turns analytics into friendly conclusions.")

    hottest = summary.loc[summary["temperature_celsius"].idxmax()]
    humidest = summary.loc[summary["humidity"].idxmax()]
    windiest = summary.loc[summary["wind_kph"].idxmax()]
    riskiest = summary.loc[summary["risk_score"].idxmax()]

    c1, c2 = st.columns([1, 1.3])

    with c1:
        st.markdown(f"""
        <div class="insight-card">🔥 <b>Thermal Leader:</b> {hottest['country']} with {hottest['temperature_celsius']:.1f}°C average temperature.</div>
        <div class="insight-card">💧 <b>Moisture Peak:</b> {humidest['country']} with {humidest['humidity']:.1f}% humidity.</div>
        <div class="insight-card">💨 <b>Wind Dominance:</b> {windiest['country']} with {windiest['wind_kph']:.1f} kph average wind.</div>
        <div class="insight-card">⚠️ <b>Risk Focus:</b> {riskiest['country']} with {riskiest['risk_score']:.1f}/100 climate risk.</div>
        """, unsafe_allow_html=True)

    with c2:
        fig_story = px.scatter(
            summary,
            x="temperature_celsius",
            y="risk_score",
            size="humidity",
            color="wind_kph",
            hover_name="country",
            color_continuous_scale="Turbo"
        )
        fig_story.update_layout(**plot_layout("🧠 Climate Narrative Matrix", h=480))
        st.plotly_chart(fig_story, use_container_width=True)

    st.markdown("### 📝 Auto-Generated Narrative")
    st.write(f"""
    ClimateScope X identifies **{hottest['country']}** as the hottest observed climate profile in the dataset, 
    while **{humidest['country']}** shows the strongest moisture concentration.  
    **{windiest['country']}** stands out with the highest average wind movement, indicating more dynamic atmospheric behavior.  
    Using the derived multi-factor climate risk formula, **{riskiest['country']}** emerges as the most climate-sensitive country in the current data sample.

    This section is important because it converts raw analytics into an explainable story:
    - what stands out,
    - why it matters,
    - and how a decision-maker can interpret it quickly.
    """)

    section_close()

# =========================================================
# 7. ABOUT
# =========================================================
elif view == "🎓 About":
    
    with st.expander("1️⃣ Project Objective", expanded=True):
        st.write("""
        ClimateScope X is an interactive climate intelligence dashboard built using Streamlit + Plotly.
        The aim is to convert global weather observations into:
        - meaningful country-level summaries
        - interactive visual analytics
        - dynamic risk-based insights
        - comparative climate understanding
        """)

    with st.expander("2️⃣ Why this is different from a normal weather dashboard"):
        st.write("""
        Most dashboards only show static charts or current weather style panels.

        This project is different because it includes:
        - a premium product-style UI
        - top bookmark-like navigation
        - a country studio for deep analysis
        - a dynamic Risk Reactor
        - a Twin Compare system with similarity score
        - a Story Deck for explainable interpretation
        """)

    with st.expander("3️⃣ Dataset Used"):
        st.write("""
        Dataset: `GlobalWeatherRepository.csv`

        Core fields used:
        - country
        - temperature_celsius
        - humidity
        - wind_kph
        - pressure_mb
        - precip_mm
        - uv_index
        - condition_text
        - last_updated (if available)
        """)

    with st.expander("4️⃣ Risk Score Formula"):
        st.write("""
        A custom derived climate risk score is created by combining:
        - temperature contribution
        - humidity contribution
        - wind contribution
        - precipitation contribution
        - UV contribution

        Each feature is normalized and scaled, then combined into a score out of 100.
        This makes the data easier to interpret as a simplified climate stress indicator.
        """)

    with st.expander("5️⃣ Technical Stack"):
        st.write("""
        - Python
        - Streamlit for UI
        - Pandas for data processing
        - NumPy for numeric logic
        - Plotly for interactive charts
        - Custom CSS for premium neon glass interface
        """)

    with st.expander("6️⃣ Future Scope"):
        st.write("""
        Future upgrades can include:
        - machine learning for anomaly detection
        - future weather forecasting
        - live API integration
        - regional drill-down maps
        - climate recommendation or alert engine
        - AI-generated summaries from user-selected filters
        """)

    with st.expander("7️⃣ Best 30-second explanation you can say"):
        st.write("""
        “ClimateScope X is a climate intelligence dashboard that transforms global weather data into interactive,
        explainable insights. Instead of only showing normal weather visuals, it introduces country-level deep analysis,
        a dynamic climate risk simulator, nation comparison, spatial geo exploration, and a storytelling layer.
        This makes the project more analytical, friendly, and closer to a real product experience.”
        """)

    section_close()

# =========================================================
# FOOTER
# =========================================================
st.markdown("""
<div class="footer-note">
    Dinesh Kanna's Infosys Springboard Internship Project "ClimateScope X"
</div>
""", unsafe_allow_html=True)