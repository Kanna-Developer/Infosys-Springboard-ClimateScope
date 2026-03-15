import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os
import numpy as np

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
# PREMIUM DARK NEON GLASS CSS
# =========================================================
st.markdown("""
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

html, body, [data-testid="stAppViewContainer"], .main {
    background:
        radial-gradient(circle at 15% 20%, rgba(0, 255, 200, 0.08), transparent 22%),
        radial-gradient(circle at 85% 15%, rgba(0, 180, 255, 0.08), transparent 22%),
        radial-gradient(circle at 50% 85%, rgba(180, 0, 255, 0.06), transparent 28%),
        linear-gradient(135deg, #060816 0%, #0b1020 45%, #070b17 100%);
    color: #f8fafc;
}

.block-container {
    padding-top: 1rem;
    padding-bottom: 1rem;
    max-width: 1500px;
}

.hero-title {
    font-size: 3.2rem;
    font-weight: 900;
    letter-spacing: 0.5px;
    margin-bottom: 0.2rem;
    background: linear-gradient(90deg, #67e8f9, #22d3ee, #a78bfa, #38bdf8);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.hero-subtitle {
    color: #cbd5e1;
    font-size: 1rem;
    margin-bottom: 1rem;
}

.glass-nav {
    background: rgba(255,255,255,0.06);
    border: 1px solid rgba(255,255,255,0.12);
    border-radius: 22px;
    padding: 12px 16px;
    backdrop-filter: blur(18px);
    -webkit-backdrop-filter: blur(18px);
    box-shadow: 0 8px 28px rgba(0,0,0,0.28);
    margin-bottom: 1rem;
}

.glass-card {
    background: rgba(255,255,255,0.055);
    border: 1px solid rgba(255,255,255,0.10);
    border-radius: 22px;
    padding: 18px;
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    box-shadow: 0 10px 30px rgba(0,0,0,0.25);
    margin-bottom: 1rem;
}

.metric-card {
    background: linear-gradient(145deg, rgba(255,255,255,0.07), rgba(255,255,255,0.035));
    border: 1px solid rgba(255,255,255,0.12);
    border-radius: 24px;
    padding: 18px;
    text-align: center;
    box-shadow: 0 10px 30px rgba(0,0,0,0.22);
    min-height: 120px;
}

.metric-label {
    color: #94a3b8;
    font-size: 0.95rem;
    margin-bottom: 8px;
}

.metric-value {
    font-size: 2rem;
    font-weight: 800;
    color: #f8fafc;
}

.metric-sub {
    color: #67e8f9;
    font-size: 0.85rem;
    margin-top: 6px;
}

.section-title {
    font-size: 1.4rem;
    font-weight: 800;
    margin-bottom: 0.8rem;
    color: #e2e8f0;
}

.info-chip {
    display: inline-block;
    padding: 8px 14px;
    margin: 4px 8px 4px 0;
    border-radius: 999px;
    background: rgba(255,255,255,0.06);
    border: 1px solid rgba(255,255,255,0.12);
    color: #cbd5e1;
    font-size: 0.85rem;
}

.insight-box {
    background: linear-gradient(135deg, rgba(34,211,238,0.12), rgba(168,85,247,0.10));
    border: 1px solid rgba(255,255,255,0.10);
    border-left: 4px solid #22d3ee;
    border-radius: 18px;
    padding: 14px 16px;
    margin-bottom: 10px;
    color: #e2e8f0;
}

.footer-note {
    text-align: center;
    color: #94a3b8;
    padding: 18px 0 8px 0;
    font-size: 0.95rem;
}

[data-testid="stSelectbox"] > div > div,
[data-testid="stMultiSelect"] > div > div {
    background: rgba(255,255,255,0.06) !important;
    border: 1px solid rgba(255,255,255,0.12) !important;
    border-radius: 14px !important;
}

.stTabs [data-baseweb="tab-list"] {
    gap: 12px;
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 18px;
    padding: 10px;
    backdrop-filter: blur(12px);
}

.stTabs [data-baseweb="tab"] {
    height: 54px;
    border-radius: 14px;
    padding: 0px 18px;
    color: #cbd5e1;
    font-weight: 700;
    background: rgba(255,255,255,0.03);
}

.stTabs [aria-selected="true"] {
    background: linear-gradient(90deg, rgba(34,211,238,0.18), rgba(168,85,247,0.18)) !important;
    color: white !important;
    border: 1px solid rgba(255,255,255,0.12);
}

.stButton>button {
    width: 100%;
    border-radius: 14px;
    border: 1px solid rgba(255,255,255,0.12);
    background: linear-gradient(90deg, rgba(34,211,238,0.18), rgba(59,130,246,0.18));
    color: white;
    font-weight: 700;
}

div[data-testid="stImage"] img {
    border-radius: 22px;
    border: 1px solid rgba(255,255,255,0.08);
}
</style>
""", unsafe_allow_html=True)

# =========================================================
# LOAD DATA
# =========================================================
@st.cache_data(show_spinner=False)
def load_data():
    file_path = "GlobalWeatherRepository.csv"

    if not os.path.exists(file_path):
        st.error("Dataset file 'GlobalWeatherRepository.csv' not found. Keep it in the same folder as app.py.")
        st.stop()

    df = pd.read_csv(file_path)

    if "last_updated" in df.columns:
        df["last_updated"] = pd.to_datetime(df["last_updated"], errors="coerce")

    numeric_cols = [
        "temperature_celsius", "humidity", "wind_kph", "uv_index",
        "precip_mm", "pressure_mb", "visibility_km", "feels_like_celsius"
    ]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    return df

# =========================================================
# HELPERS
# =========================================================
def climate_risk_score(row):
    score = 0
    temp = row.get("temperature_celsius", np.nan)
    humidity = row.get("humidity", np.nan)
    wind = row.get("wind_kph", np.nan)
    uv = row.get("uv_index", np.nan)
    precip = row.get("precip_mm", np.nan)
    pressure = row.get("pressure_mb", np.nan)

    if pd.notna(temp):
        if temp > 40:
            score += 30
        elif temp > 35:
            score += 22
        elif temp < 0:
            score += 25
        elif temp < 5:
            score += 18

    if pd.notna(humidity) and humidity > 85:
        score += 14

    if pd.notna(wind):
        if wind > 60:
            score += 22
        elif wind > 40:
            score += 16

    if pd.notna(uv):
        if uv > 10:
            score += 18
        elif uv > 8:
            score += 12

    if pd.notna(precip):
        if precip > 80:
            score += 20
        elif precip > 40:
            score += 12

    if pd.notna(pressure):
        if pressure < 990:
            score += 10

    return min(score, 100)

def risk_label(score):
    if score < 25:
        return "🟢 Low Risk"
    elif score < 50:
        return "🟡 Moderate Risk"
    elif score < 75:
        return "🟠 High Risk"
    return "🔴 Severe Risk"

def safe_mean(df, col):
    if col in df.columns and df[col].notna().any():
        return round(df[col].mean(), 2)
    return 0

def safe_max(df, col):
    if col in df.columns and df[col].notna().any():
        return round(df[col].max(), 2)
    return 0

def safe_min(df, col):
    if col in df.columns and df[col].notna().any():
        return round(df[col].min(), 2)
    return 0

def metric_card(title, value, sub=""):
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">{title}</div>
        <div class="metric-value">{value}</div>
        <div class="metric-sub">{sub}</div>
    </div>
    """, unsafe_allow_html=True)

def section_title(title):
    st.markdown(f'<div class="section-title">{title}</div>', unsafe_allow_html=True)

def insight(text):
    st.markdown(f'<div class="insight-box">{text}</div>', unsafe_allow_html=True)

def build_country_summary(country_df, country):
    items = []
    avg_temp = safe_mean(country_df, "temperature_celsius")
    avg_humidity = safe_mean(country_df, "humidity")
    avg_wind = safe_mean(country_df, "wind_kph")
    avg_uv = safe_mean(country_df, "uv_index")
    avg_risk = round(country_df["climate_risk_score"].mean(), 2)

    if avg_temp > 35:
        items.append(f"🔥 {country} is facing elevated heat levels with average temperature near {avg_temp}°C.")
    elif avg_temp < 10:
        items.append(f"❄️ {country} shows relatively cold climate behavior with average temperature around {avg_temp}°C.")
    else:
        items.append(f"🌡️ {country} has a balanced average temperature around {avg_temp}°C.")

    if avg_humidity > 80:
        items.append(f"💧 High humidity ({avg_humidity}%) may increase discomfort and rainfall probability.")
    else:
        items.append(f"💨 Humidity remains moderate at {avg_humidity}% for current observations.")

    if avg_wind > 35:
        items.append(f"🌬️ Wind intensity is notable at {avg_wind} kph, affecting outdoor conditions.")
    if avg_uv > 8:
        items.append(f"☀️ UV exposure is high ({avg_uv}), suggesting stronger sun risk.")
    items.append(f"🚨 Overall climate risk is {avg_risk}/100, categorized as {risk_label(avg_risk)}.")

    return items

def plot_theme(fig):
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=20, r=20, t=50, b=20),
        font=dict(color="#E2E8F0")
    )
    return fig

# =========================================================
# MAIN APP
# =========================================================
def main():
    df = load_data()
    df["climate_risk_score"] = df.apply(climate_risk_score, axis=1)

    countries = sorted(df["country"].dropna().unique().tolist()) if "country" in df.columns else []

    # Header
    st.markdown('<div class="hero-title">🌦️ ClimateScope X</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="hero-subtitle">A premium climate intelligence dashboard for interactive weather analytics, dynamic risk discovery, and powerful country-level comparisons.</div>',
        unsafe_allow_html=True
    )

    # Top glass nav style tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🌍 Command Center",
        "📍 Country Lens",
        "⚖️ Compare",
        "🧠 Insight Engine",
        "ℹ️ About"
    ])

    # =====================================================
    # TAB 1: COMMAND CENTER
    # =====================================================
    with tab1:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        section_title("Global Climate Command Center")

        c1, c2, c3, c4, c5 = st.columns(5)
        with c1:
            metric_card("Countries", len(countries), "Tracked")
        with c2:
            metric_card("Avg Temp", f"{safe_mean(df, 'temperature_celsius')}°C", "Global")
        with c3:
            metric_card("Avg Humidity", f"{safe_mean(df, 'humidity')}%", "Global")
        with c4:
            metric_card("Avg Wind", f"{safe_mean(df, 'wind_kph')} kph", "Global")
        with c5:
            metric_card("Avg Risk", f"{round(df['climate_risk_score'].mean(), 2)}", "Risk / 100")
        st.markdown('</div>', unsafe_allow_html=True)

        top_row1, top_row2 = st.columns([1.2, 1])

        with top_row1:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            section_title("Spotlight Metric Explorer")

            spotlight_metric = st.selectbox(
                "Choose a metric to spotlight",
                ["temperature_celsius", "humidity", "wind_kph", "uv_index", "precip_mm", "pressure_mb"]
            )

            if spotlight_metric in df.columns:
                top_metric = (
                    df.groupby("country", as_index=False)[spotlight_metric]
                    .mean()
                    .sort_values(spotlight_metric, ascending=False)
                    .head(12)
                )

                fig = px.bar(
                    top_metric,
                    x="country",
                    y=spotlight_metric,
                    color=spotlight_metric,
                    color_continuous_scale="Turbo",
                    title=f"Top 12 Countries by {spotlight_metric.replace('_', ' ').title()}"
                )
                plot_theme(fig)
                st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

        with top_row2:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            section_title("Climate Visual")
            st.image(
                "https://images.unsplash.com/photo-1500375592092-40eb2168fd21?auto=format&fit=crop&w=1400&q=80",
                use_container_width=True
            )
            st.markdown('</div>', unsafe_allow_html=True)

        lower1, lower2 = st.columns([1.15, 1])

        with lower1:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            section_title("Global Climate Risk Map")
            map_df = df.groupby("country", as_index=False)["climate_risk_score"].mean()

            fig_map = px.choropleth(
                map_df,
                locations="country",
                locationmode="country names",
                color="climate_risk_score",
                hover_name="country",
                color_continuous_scale="Turbo",
                title="Average Climate Risk by Country"
            )
            plot_theme(fig_map)
            st.plotly_chart(fig_map, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

        with lower2:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            section_title("Risk Distribution Radar")

            avg_vals = {
                "Temperature": safe_mean(df, "temperature_celsius"),
                "Humidity": safe_mean(df, "humidity"),
                "Wind": safe_mean(df, "wind_kph"),
                "UV": safe_mean(df, "uv_index"),
                "Precip": safe_mean(df, "precip_mm")
            }

            radar = go.Figure()
            radar.add_trace(go.Scatterpolar(
                r=list(avg_vals.values()),
                theta=list(avg_vals.keys()),
                fill='toself',
                name='Global Avg Profile'
            ))
            radar.update_layout(
                polar=dict(bgcolor="rgba(0,0,0,0)"),
                template="plotly_dark",
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                title="Global Climate Signature"
            )
            st.plotly_chart(radar, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

    # =====================================================
    # TAB 2: COUNTRY LENS
    # =====================================================
    with tab2:
        section_title("Country Lens")

        if not countries:
            st.warning("No country column found in dataset.")
        else:
            top1, top2 = st.columns([1.1, 1])

            with top1:
                selected_country = st.selectbox("Select Country", countries)
            with top2:
                chart_mode = st.selectbox(
                    "Select View",
                    ["Trend View", "Distribution View", "Risk Breakdown"]
                )

            country_df = df[df["country"] == selected_country].copy()

            if not country_df.empty:
                row1 = st.columns(5)
                with row1[0]:
                    metric_card("Avg Temp", f"{safe_mean(country_df, 'temperature_celsius')}°C", "Country")
                with row1[1]:
                    metric_card("Max Temp", f"{safe_max(country_df, 'temperature_celsius')}°C", "Peak")
                with row1[2]:
                    metric_card("Avg Humidity", f"{safe_mean(country_df, 'humidity')}%", "Country")
                with row1[3]:
                    metric_card("Avg Wind", f"{safe_mean(country_df, 'wind_kph')} kph", "Country")
                with row1[4]:
                    avg_risk = round(country_df["climate_risk_score"].mean(), 2)
                    metric_card("Risk Score", f"{avg_risk}", risk_label(avg_risk))

                st.markdown('<div class="glass-card">', unsafe_allow_html=True)
                section_title(f"{selected_country} Dynamic View")

                if chart_mode == "Trend View":
                    if "last_updated" in country_df.columns:
                        fig = make_subplots(
                            rows=2, cols=2,
                            subplot_titles=("Temperature", "Humidity", "Wind", "Risk Score")
                        )

                        sorted_df = country_df.sort_values("last_updated")

                        if "temperature_celsius" in sorted_df.columns:
                            fig.add_trace(go.Scatter(
                                x=sorted_df["last_updated"], y=sorted_df["temperature_celsius"],
                                mode="lines+markers", name="Temp"
                            ), row=1, col=1)

                        if "humidity" in sorted_df.columns:
                            fig.add_trace(go.Scatter(
                                x=sorted_df["last_updated"], y=sorted_df["humidity"],
                                mode="lines+markers", name="Humidity"
                            ), row=1, col=2)

                        if "wind_kph" in sorted_df.columns:
                            fig.add_trace(go.Scatter(
                                x=sorted_df["last_updated"], y=sorted_df["wind_kph"],
                                mode="lines+markers", name="Wind"
                            ), row=2, col=1)

                        fig.add_trace(go.Scatter(
                            x=sorted_df["last_updated"], y=sorted_df["climate_risk_score"],
                            mode="lines+markers", name="Risk"
                        ), row=2, col=2)

                        fig.update_layout(height=700, template="plotly_dark",
                                          paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
                        st.plotly_chart(fig, use_container_width=True)

                elif chart_mode == "Distribution View":
                    dist_metric = st.selectbox(
                        "Select metric distribution",
                        ["temperature_celsius", "humidity", "wind_kph", "uv_index", "precip_mm"],
                        key="dist_metric"
                    )

                    if dist_metric in country_df.columns:
                        fig = px.histogram(
                            country_df,
                            x=dist_metric,
                            nbins=20,
                            color_discrete_sequence=["#22d3ee"],
                            title=f"{selected_country} {dist_metric.replace('_', ' ').title()} Distribution"
                        )
                        plot_theme(fig)
                        st.plotly_chart(fig, use_container_width=True)

                else:
                    breakdown = pd.DataFrame({
                        "Factor": ["Temperature", "Humidity", "Wind", "UV", "Precipitation"],
                        "Average": [
                            safe_mean(country_df, "temperature_celsius"),
                            safe_mean(country_df, "humidity"),
                            safe_mean(country_df, "wind_kph"),
                            safe_mean(country_df, "uv_index"),
                            safe_mean(country_df, "precip_mm")
                        ]
                    })
                    fig = px.treemap(
                        breakdown,
                        path=["Factor"],
                        values="Average",
                        color="Average",
                        color_continuous_scale="Turbo",
                        title=f"{selected_country} Climate Factor Breakdown"
                    )
                    plot_theme(fig)
                    st.plotly_chart(fig, use_container_width=True)

                st.markdown('</div>', unsafe_allow_html=True)

                st.markdown('<div class="glass-card">', unsafe_allow_html=True)
                section_title("Smart Observations")
                for line in build_country_summary(country_df, selected_country):
                    insight(line)
                st.markdown('</div>', unsafe_allow_html=True)

    # =====================================================
    # TAB 3: COMPARE
    # =====================================================
    with tab3:
        section_title("Country vs Country Analyzer")

        if len(countries) >= 2:
            r1, r2 = st.columns(2)
            with r1:
                country1 = st.selectbox("Select Country 1", countries, key="compare1")
            with r2:
                country2 = st.selectbox("Select Country 2", countries, index=1, key="compare2")

            df1 = df[df["country"] == country1]
            df2 = df[df["country"] == country2]

            comparison = pd.DataFrame({
                "Metric": ["Temperature", "Humidity", "Wind", "Pressure", "UV", "Precipitation", "Risk Score"],
                country1: [
                    safe_mean(df1, "temperature_celsius"),
                    safe_mean(df1, "humidity"),
                    safe_mean(df1, "wind_kph"),
                    safe_mean(df1, "pressure_mb"),
                    safe_mean(df1, "uv_index"),
                    safe_mean(df1, "precip_mm"),
                    round(df1["climate_risk_score"].mean(), 2)
                ],
                country2: [
                    safe_mean(df2, "temperature_celsius"),
                    safe_mean(df2, "humidity"),
                    safe_mean(df2, "wind_kph"),
                    safe_mean(df2, "pressure_mb"),
                    safe_mean(df2, "uv_index"),
                    safe_mean(df2, "precip_mm"),
                    round(df2["climate_risk_score"].mean(), 2)
                ]
            })

            c1, c2 = st.columns([1, 1])

            with c1:
                st.markdown('<div class="glass-card">', unsafe_allow_html=True)
                section_title("Comparison Table")
                st.dataframe(comparison, use_container_width=True, hide_index=True)
                st.markdown('</div>', unsafe_allow_html=True)

            with c2:
                st.markdown('<div class="glass-card">', unsafe_allow_html=True)
                section_title("Radar Comparison")

                fig = go.Figure()
                fig.add_trace(go.Scatterpolar(
                    r=comparison[country1],
                    theta=comparison["Metric"],
                    fill='toself',
                    name=country1
                ))
                fig.add_trace(go.Scatterpolar(
                    r=comparison[country2],
                    theta=comparison["Metric"],
                    fill='toself',
                    name=country2
                ))
                fig.update_layout(
                    template="plotly_dark",
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    polar=dict(bgcolor="rgba(0,0,0,0)"),
                    title="Climate Profile Radar"
                )
                st.plotly_chart(fig, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)

            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            section_title("Metric Battle View")
            fig_bar = go.Figure()
            fig_bar.add_trace(go.Bar(x=comparison["Metric"], y=comparison[country1], name=country1))
            fig_bar.add_trace(go.Bar(x=comparison["Metric"], y=comparison[country2], name=country2))
            fig_bar.update_layout(
                barmode="group",
                template="plotly_dark",
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                title="Country Metric Battle"
            )
            st.plotly_chart(fig_bar, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

    # =====================================================
    # TAB 4: INSIGHT ENGINE
    # =====================================================
    with tab4:
        section_title("Insight Engine")

        top1, top2 = st.columns(2)

        with top1:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            section_title("Top 10 Highest Climate Risk Countries")
            risk_df = (
                df.groupby("country", as_index=False)["climate_risk_score"]
                .mean()
                .sort_values("climate_risk_score", ascending=False)
                .head(10)
            )
            st.dataframe(risk_df, use_container_width=True, hide_index=True)

            fig = px.bar(
                risk_df,
                x="country",
                y="climate_risk_score",
                color="climate_risk_score",
                color_continuous_scale="Turbo",
                title="Highest Climate Risk Countries"
            )
            plot_theme(fig)
            st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

        with top2:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            section_title("Temperature vs Humidity Bubble Matrix")

            if all(col in df.columns for col in ["country", "temperature_celsius", "humidity", "wind_kph"]):
                bubble_df = (
                    df.groupby("country", as_index=False)[["temperature_celsius", "humidity", "wind_kph", "climate_risk_score"]]
                    .mean()
                )

                fig_bubble = px.scatter(
                    bubble_df,
                    x="temperature_celsius",
                    y="humidity",
                    size="wind_kph",
                    color="climate_risk_score",
                    hover_name="country",
                    color_continuous_scale="Turbo",
                    title="Climate Pattern Bubble View"
                )
                plot_theme(fig_bubble)
                st.plotly_chart(fig_bubble, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

        bottom1, bottom2 = st.columns(2)

        with bottom1:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            section_title("Top 8 Hottest Countries")
            hottest = (
                df.groupby("country", as_index=False)["temperature_celsius"]
                .mean()
                .sort_values("temperature_celsius", ascending=False)
                .head(8)
            )
            st.dataframe(hottest, use_container_width=True, hide_index=True)
            st.markdown('</div>', unsafe_allow_html=True)

        with bottom2:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            section_title("Top 8 Most Humid Countries")
            humid = (
                df.groupby("country", as_index=False)["humidity"]
                .mean()
                .sort_values("humidity", ascending=False)
                .head(8)
            )
            st.dataframe(humid, use_container_width=True, hide_index=True)
            st.markdown('</div>', unsafe_allow_html=True)

    # =====================================================
    # TAB 5: ABOUT
    # =====================================================
    with tab5:
        section_title("About")

        st.markdown("""
        <div class="glass-card">
        <h4>🎯 Project Objective</h4>
        <p>
        ClimateScope X is a data analytics dashboard developed using Streamlit and Plotly.
        It helps users understand weather conditions across countries using interactive charts,
        climate risk scoring, and country comparison.
        </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="glass-card">
        <h4>🛠️ Technologies Used</h4>
        <ul>
            <li>Python</li>
            <li>Streamlit</li>
            <li>Pandas</li>
            <li>Plotly</li>
            <li>CSV Dataset (GlobalWeatherRepository)</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="glass-card">
        <p>
        This project loads a global weather dataset, processes key weather parameters like
        temperature, humidity, wind speed, UV index, and precipitation, and then generates
        a simple climate risk score. Users can explore overall trends, analyze one country,
        compare two countries, and view smart insights through visual dashboards.
        </p>
        </div>
        """, unsafe_allow_html=True)

    # Footer
    st.markdown(
        '<div class="footer-note">Dinesh Kanna\'s Infosys Springboard ClimateScope Project</div>',
        unsafe_allow_html=True
    )

# =========================================================
# RUN
# =========================================================
main()