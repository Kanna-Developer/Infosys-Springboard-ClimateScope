import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from math import pi

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
# CUSTOM CSS - PREMIUM DARK NEON GLASS UI
# =========================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background:
        radial-gradient(circle at 10% 20%, rgba(0,255,255,0.08), transparent 22%),
        radial-gradient(circle at 85% 15%, rgba(255,0,153,0.08), transparent 24%),
        radial-gradient(circle at 80% 80%, rgba(0,200,255,0.08), transparent 24%),
        linear-gradient(135deg, #060814 0%, #0b1020 35%, #111827 70%, #0f172a 100%);
    color: #e5f4ff;
}

.block-container {
    padding-top: 1.2rem;
    padding-bottom: 2rem;
    max-width: 1500px;
}

/* Remove Streamlit top spacing look */
header, footer {
    visibility: hidden;
}

/* Hero */
.hero-wrap {
    position: relative;
    padding: 1.6rem 1.8rem 1.4rem 1.8rem;
    border-radius: 26px;
    background: rgba(255,255,255,0.06);
    backdrop-filter: blur(18px);
    -webkit-backdrop-filter: blur(18px);
    border: 1px solid rgba(255,255,255,0.12);
    box-shadow: 0 0 0 1px rgba(255,255,255,0.02), 0 8px 40px rgba(0,0,0,0.35);
    margin-bottom: 1.2rem;
    overflow: hidden;
}

.hero-wrap::before {
    content: "";
    position: absolute;
    inset: -2px;
    background: linear-gradient(90deg, rgba(0,255,255,0.18), rgba(255,0,153,0.14), rgba(0,255,180,0.14));
    filter: blur(24px);
    z-index: 0;
}

.hero-inner {
    position: relative;
    z-index: 1;
}

.hero-title {
    font-size: 2.4rem;
    font-weight: 800;
    line-height: 1.1;
    color: #f8fbff;
    margin-bottom: 0.25rem;
}

.hero-subtitle {
    font-size: 1rem;
    color: #b9d7f0;
    margin-bottom: 0.9rem;
}

.hero-chip-row {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
    margin-top: 0.5rem;
}

.hero-chip {
    padding: 0.45rem 0.85rem;
    border-radius: 999px;
    background: rgba(255,255,255,0.06);
    border: 1px solid rgba(255,255,255,0.10);
    color: #dff7ff;
    font-size: 0.86rem;
    font-weight: 600;
    backdrop-filter: blur(8px);
}

/* Glass top nav feel */
.stRadio > div {
    background: rgba(255,255,255,0.05);
    padding: 0.55rem;
    border-radius: 22px;
    border: 1px solid rgba(255,255,255,0.10);
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    margin-bottom: 1.2rem;
}

div[role="radiogroup"] {
    display: flex;
    justify-content: space-between;
    gap: 8px;
    flex-wrap: wrap;
}

div[role="radiogroup"] > label {
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.10);
    padding: 0.7rem 1rem;
    border-radius: 18px;
    color: #d9f3ff !important;
    font-weight: 600;
    transition: all 0.25s ease;
    min-width: fit-content;
}

div[role="radiogroup"] > label:hover {
    transform: translateY(-2px);
    border-color: rgba(0,255,255,0.35);
    box-shadow: 0 0 18px rgba(0,255,255,0.08);
}

/* Section card */
.glass-card {
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.10);
    border-radius: 24px;
    padding: 1.1rem 1.2rem;
    backdrop-filter: blur(14px);
    -webkit-backdrop-filter: blur(14px);
    box-shadow: 0 10px 35px rgba(0,0,0,0.24);
    margin-bottom: 1rem;
}

/* KPI cards */
.metric-card {
    background: linear-gradient(180deg, rgba(255,255,255,0.06), rgba(255,255,255,0.04));
    border: 1px solid rgba(255,255,255,0.10);
    border-radius: 22px;
    padding: 1rem 1rem;
    min-height: 120px;
    box-shadow: 0 8px 28px rgba(0,0,0,0.22);
    transition: transform 0.25s ease;
}

.metric-card:hover {
    transform: translateY(-3px);
}

.metric-label {
    color: #a8c7e6;
    font-size: 0.85rem;
    font-weight: 600;
    margin-bottom: 0.45rem;
}

.metric-value {
    color: #f7fbff;
    font-size: 1.8rem;
    font-weight: 800;
    line-height: 1;
    margin-bottom: 0.3rem;
}

.metric-note {
    color: #b8d9ee;
    font-size: 0.82rem;
}

/* Status badges */
.badge {
    display: inline-block;
    padding: 0.42rem 0.8rem;
    border-radius: 999px;
    font-size: 0.82rem;
    font-weight: 700;
    margin-right: 8px;
    margin-bottom: 6px;
    border: 1px solid rgba(255,255,255,0.08);
}

.badge-green {
    background: rgba(0,255,170,0.12);
    color: #8fffe1;
}

.badge-yellow {
    background: rgba(255,214,10,0.12);
    color: #ffe98a;
}

.badge-red {
    background: rgba(255,80,120,0.12);
    color: #ff9db6;
}

.badge-blue {
    background: rgba(0,180,255,0.12);
    color: #8edfff;
}

/* Footer */
.footer-text {
    text-align: center;
    color: #9fc6de;
    font-size: 0.9rem;
    margin-top: 1.5rem;
    padding: 1rem 0 0.5rem 0;
}

/* Hide radio label text */
div[data-testid="stRadio"] > label {
    display: none;
}
</style>
""", unsafe_allow_html=True)

# =========================================================
# LOAD DATA
# =========================================================
@st.cache_data
def load_data():
    df = pd.read_csv("GlobalWeatherRepository.csv")
    return df

# =========================================================
# HELPER FUNCTIONS
# =========================================================
def find_column(df, possible_names):
    lower_map = {c.lower().strip(): c for c in df.columns}
    for name in possible_names:
        if name.lower().strip() in lower_map:
            return lower_map[name.lower().strip()]
    for c in df.columns:
        cl = c.lower().strip()
        for name in possible_names:
            if name.lower().strip() in cl:
                return c
    return None

@st.cache_data
def preprocess(df):
    country_col = find_column(df, ["country", "country_name", "location", "region"])
    lat_col = find_column(df, ["latitude", "lat"])
    lon_col = find_column(df, ["longitude", "lon", "lng"])
    temp_col = find_column(df, ["temperature_celsius", "temperature", "temp_c", "temp"])
    humidity_col = find_column(df, ["humidity", "humidity_percent"])
    wind_col = find_column(df, ["wind_kph", "wind_speed", "wind"])
    precip_col = find_column(df, ["precip_mm", "precipitation", "rainfall", "rain"])
    pressure_col = find_column(df, ["pressure_mb", "pressure", "pressure_hpa"])
    uv_col = find_column(df, ["uv_index", "uv"])
    visibility_col = find_column(df, ["visibility_km", "visibility"])

    required = {
        "country": country_col,
        "lat": lat_col,
        "lon": lon_col,
        "temp": temp_col,
        "humidity": humidity_col,
        "wind": wind_col,
        "precip": precip_col,
        "pressure": pressure_col,
        "uv": uv_col,
        "visibility": visibility_col
    }

    missing = [k for k, v in required.items() if v is None]
    if missing:
        st.error(f"Missing expected columns in dataset. Could not detect: {missing}")
        st.stop()

    work = df[[country_col, lat_col, lon_col, temp_col, humidity_col, wind_col, precip_col, pressure_col, uv_col, visibility_col]].copy()
    work.columns = ["Country", "Latitude", "Longitude", "Temperature", "Humidity", "Wind", "Precipitation", "Pressure", "UV", "Visibility"]

    for col in ["Latitude", "Longitude", "Temperature", "Humidity", "Wind", "Precipitation", "Pressure", "UV", "Visibility"]:
        work[col] = pd.to_numeric(work[col], errors="coerce")

    work = work.dropna(subset=["Country", "Latitude", "Longitude", "Temperature", "Humidity", "Wind", "Precipitation", "Pressure", "UV", "Visibility"])
    work["Country"] = work["Country"].astype(str).str.strip()

    grouped = work.groupby("Country", as_index=False).agg({
        "Latitude": "mean",
        "Longitude": "mean",
        "Temperature": "mean",
        "Humidity": "mean",
        "Wind": "mean",
        "Precipitation": "mean",
        "Pressure": "mean",
        "UV": "mean",
        "Visibility": "mean"
    })

    grouped["TravelScore"] = grouped.apply(calculate_travel_score, axis=1)
    grouped["TravelStatus"] = grouped["TravelScore"].apply(score_to_status)
    grouped["FieldReadiness"] = grouped.apply(field_readiness_score, axis=1)
    grouped["AirCaution"] = grouped.apply(air_travel_score, axis=1)
    grouped["RoadReadiness"] = grouped.apply(road_readiness_score, axis=1)

    return work, grouped

def clamp(x, low=0, high=100):
    return max(low, min(high, x))

def calculate_travel_score(row):
    temp = row["Temperature"]
    hum = row["Humidity"]
    wind = row["Wind"]
    rain = row["Precipitation"]
    uv = row["UV"]
    vis = row["Visibility"]

    score = 100

    # Temperature comfort ideal around 18-30
    if temp < 5:
        score -= min(25, (5 - temp) * 2.5)
    elif temp > 35:
        score -= min(30, (temp - 35) * 2.5)
    elif temp > 30:
        score -= (temp - 30) * 1.8

    # Humidity
    if hum > 85:
        score -= (hum - 85) * 0.7
    elif hum < 20:
        score -= (20 - hum) * 0.5

    # Wind
    if wind > 35:
        score -= min(25, (wind - 35) * 0.9)
    elif wind > 20:
        score -= (wind - 20) * 0.4

    # Rain
    if rain > 10:
        score -= min(25, rain * 1.2)
    elif rain > 3:
        score -= rain * 0.8

    # UV
    if uv > 8:
        score -= (uv - 8) * 2.2
    elif uv > 6:
        score -= (uv - 6) * 1.2

    # Visibility
    if vis < 3:
        score -= (3 - vis) * 8
    elif vis < 6:
        score -= (6 - vis) * 4

    return round(clamp(score), 1)

def field_readiness_score(row):
    score = 100
    if row["Temperature"] > 36: score -= 18
    if row["Humidity"] > 85: score -= 10
    if row["Wind"] > 30: score -= 18
    if row["Precipitation"] > 8: score -= 20
    if row["Visibility"] < 5: score -= 18
    if row["UV"] > 9: score -= 10
    return round(clamp(score), 1)

def air_travel_score(row):
    score = 100
    if row["Wind"] > 35: score -= 28
    if row["Visibility"] < 4: score -= 28
    if row["Precipitation"] > 12: score -= 18
    if row["Pressure"] < 990: score -= 10
    return round(clamp(score), 1)

def road_readiness_score(row):
    score = 100
    if row["Precipitation"] > 10: score -= 24
    if row["Visibility"] < 5: score -= 20
    if row["Wind"] > 30: score -= 15
    if row["Temperature"] > 38: score -= 12
    return round(clamp(score), 1)

def score_to_status(score):
    if score >= 75:
        return "Recommended"
    elif score >= 50:
        return "Proceed with Caution"
    else:
        return "Delay / Avoid"

def badge_html(label, kind):
    cls = {
        "green": "badge badge-green",
        "yellow": "badge badge-yellow",
        "red": "badge badge-red",
        "blue": "badge badge-blue"
    }[kind]
    return f'<span class="{cls}">{label}</span>'

def advisory_from_row(row):
    issues = []
    if row["Temperature"] > 35:
        issues.append("High heat stress")
    if row["Humidity"] > 85:
        issues.append("High humidity discomfort")
    if row["Wind"] > 30:
        issues.append("Strong wind caution")
    if row["Precipitation"] > 8:
        issues.append("Rain-related movement disruption")
    if row["Visibility"] < 5:
        issues.append("Low visibility risk")
    if row["UV"] > 8:
        issues.append("Elevated UV exposure")

    if not issues:
        return "Stable travel conditions with relatively low operational weather stress."
    return ", ".join(issues) + "."

def mission_decision(score, tolerance):
    if tolerance == "Low":
        if score >= 80:
            return "GO"
        elif score >= 60:
            return "CAUTION"
        return "AVOID"
    elif tolerance == "Medium":
        if score >= 72:
            return "GO"
        elif score >= 48:
            return "CAUTION"
        return "AVOID"
    else:
        if score >= 65:
            return "GO"
        elif score >= 40:
            return "CAUTION"
        return "AVOID"

def mission_badge(decision):
    if decision == "GO":
        return badge_html("GO", "green")
    elif decision == "CAUTION":
        return badge_html("CAUTION", "yellow")
    return badge_html("AVOID", "red")

def make_gauge(value, title):
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        number={"font": {"size": 32, "color": "#f5fbff"}},
        title={"text": title, "font": {"size": 18, "color": "#cfefff"}},
        gauge={
            "axis": {"range": [0, 100], "tickcolor": "#9fd8ff"},
            "bar": {"color": "#00e5ff"},
            "bgcolor": "rgba(255,255,255,0.04)",
            "borderwidth": 1,
            "bordercolor": "rgba(255,255,255,0.08)",
            "steps": [
                {"range": [0, 40], "color": "rgba(255,80,120,0.25)"},
                {"range": [40, 75], "color": "rgba(255,214,10,0.20)"},
                {"range": [75, 100], "color": "rgba(0,255,170,0.18)"}
            ],
        }
    ))
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=20, r=20, t=50, b=20),
        height=320
    )
    return fig

def radar_compare(row1, row2, name1, name2):
    categories = ["Temperature", "Humidity", "Wind", "Precipitation", "UV", "Visibility"]
    vals1 = [row1[c] for c in categories]
    vals2 = [row2[c] for c in categories]

    # Normalize rough scale for visual comparison
    max_map = {
        "Temperature": 50,
        "Humidity": 100,
        "Wind": 60,
        "Precipitation": 30,
        "UV": 15,
        "Visibility": 15
    }

    vals1n = [vals1[i] / max_map[categories[i]] * 100 for i in range(len(categories))]
    vals2n = [vals2[i] / max_map[categories[i]] * 100 for i in range(len(categories))]

    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=vals1n + [vals1n[0]],
        theta=categories + [categories[0]],
        fill='toself',
        name=name1
    ))
    fig.add_trace(go.Scatterpolar(
        r=vals2n + [vals2n[0]],
        theta=categories + [categories[0]],
        fill='toself',
        name=name2
    ))
    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 100], gridcolor="rgba(255,255,255,0.12)"),
            angularaxis=dict(gridcolor="rgba(255,255,255,0.12)")
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#dff6ff"),
        height=500,
        margin=dict(l=20, r=20, t=40, b=20)
    )
    return fig

# =========================================================
# LOAD + PROCESS
# =========================================================
df = load_data()
raw_df, country_df = preprocess(df)

# =========================================================
# HERO
# =========================================================
st.markdown("""
<div class="hero-wrap">
    <div class="hero-inner">
        <div class="hero-title">🌦️ ClimateScope X</div>
        <div class="hero-subtitle">
            Smart climate-aware travel planning for officials, field teams, and operational decision support.
        </div>
        <div class="hero-chip-row">
            <div class="hero-chip">🧭 Mission Planning</div>
            <div class="hero-chip">🚦 Travel Readiness</div>
            <div class="hero-chip">🛰 Geo Operations View</div>
            <div class="hero-chip">⚖️ Destination Comparison</div>
            <div class="hero-chip">📖 Situation Brief</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# =========================================================
# TOP NAV
# =========================================================
view = st.radio(
    "Navigation",
    [
        "🧭 Mission Planner",
        "🌍 Destination Lens",
        "🚦 Travel Readiness",
        "⚖️ Compare Destinations",
        "🛰 Geo Operations",
        "📖 Situation Brief",
        "ℹ️ About"
    ],
    horizontal=True
)

# =========================================================
# SECTION: MISSION PLANNER
# =========================================================
if view == "🧭 Mission Planner":
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("🧭 Mission Planner")

    col1, col2, col3, col4 = st.columns([2, 1.2, 1.2, 1.2])

    with col1:
        country = st.selectbox("Select Destination Country", sorted(country_df["Country"].unique()))
    with col2:
        purpose = st.selectbox("Travel Purpose", ["Field Inspection", "Emergency Coordination", "Tourism Screening", "Logistics Review"])
    with col3:
        tolerance = st.selectbox("Risk Tolerance", ["Low", "Medium", "High"])
    with col4:
        mode = st.selectbox("Travel Mode", ["Road", "Air", "Mixed"])

    row = country_df[country_df["Country"] == country].iloc[0].copy()

    base_score = row["TravelScore"]
    if purpose == "Emergency Coordination":
        adjusted_score = base_score + 5
    elif purpose == "Tourism Screening":
        adjusted_score = base_score
    elif purpose == "Logistics Review":
        adjusted_score = base_score - 2
    else:
        adjusted_score = base_score - 1

    if mode == "Air":
        adjusted_score = (adjusted_score * 0.6) + (row["AirCaution"] * 0.4)
    elif mode == "Road":
        adjusted_score = (adjusted_score * 0.6) + (row["RoadReadiness"] * 0.4)
    else:
        adjusted_score = (adjusted_score * 0.5) + (row["RoadReadiness"] * 0.25) + (row["AirCaution"] * 0.25)

    adjusted_score = round(clamp(adjusted_score), 1)
    decision = mission_decision(adjusted_score, tolerance)

    st.markdown(mission_badge(decision), unsafe_allow_html=True)
    st.markdown(badge_html(f"Travel Score: {adjusted_score}/100", "blue"), unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Temperature</div>
            <div class="metric-value">{row['Temperature']:.1f}°C</div>
            <div class="metric-note">Operational thermal condition</div>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Humidity</div>
            <div class="metric-value">{row['Humidity']:.0f}%</div>
            <div class="metric-note">Comfort & equipment stress</div>
        </div>
        """, unsafe_allow_html=True)
    with c3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Wind</div>
            <div class="metric-value">{row['Wind']:.1f}</div>
            <div class="metric-note">Movement and air caution</div>
        </div>
        """, unsafe_allow_html=True)
    with c4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Visibility</div>
            <div class="metric-value">{row['Visibility']:.1f} km</div>
            <div class="metric-note">Navigation clarity</div>
        </div>
        """, unsafe_allow_html=True)

    left, right = st.columns([1.1, 1.4])
    with left:
        st.plotly_chart(make_gauge(adjusted_score, "Mission Suitability"), use_container_width=True)
    with right:
        st.markdown("### Operational Advisory")
        st.info(advisory_from_row(row))

        precautions = []
        if row["Temperature"] > 35: precautions.append("Carry hydration and heat protection gear.")
        if row["UV"] > 8: precautions.append("Limit prolonged outdoor exposure during peak hours.")
        if row["Precipitation"] > 8: precautions.append("Prepare rain-safe transport and waterproof documentation.")
        if row["Wind"] > 30: precautions.append("Secure lightweight equipment and outdoor installations.")
        if row["Visibility"] < 5: precautions.append("Use route buffers and avoid low-visibility movement windows.")
        if not precautions:
            precautions = ["Standard travel conditions. Routine planning is sufficient."]

        for p in precautions:
            st.markdown(f"- {p}")

    st.markdown('</div>', unsafe_allow_html=True)

# =========================================================
# SECTION: DESTINATION LENS
# =========================================================
elif view == "🌍 Destination Lens":
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("🌍 Destination Lens")

    country = st.selectbox("Choose a Country", sorted(country_df["Country"].unique()), key="destination_lens")
    row = country_df[country_df["Country"] == country].iloc[0]

    status_kind = "green" if row["TravelStatus"] == "Recommended" else "yellow" if row["TravelStatus"] == "Proceed with Caution" else "red"
    st.markdown(badge_html(row["TravelStatus"], status_kind), unsafe_allow_html=True)

    c1, c2, c3, c4, c5 = st.columns(5)
    metrics = [
        ("Travel Score", f"{row['TravelScore']:.1f}/100", "Overall destination suitability"),
        ("Field Readiness", f"{row['FieldReadiness']:.1f}/100", "Ground operation readiness"),
        ("Air Caution", f"{row['AirCaution']:.1f}/100", "Aviation condition score"),
        ("Road Readiness", f"{row['RoadReadiness']:.1f}/100", "Road movement suitability"),
        ("UV Index", f"{row['UV']:.1f}", "Exposure intensity")
    ]

    for col, (label, value, note) in zip([c1, c2, c3, c4, c5], metrics):
        with col:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">{label}</div>
                <div class="metric-value">{value}</div>
                <div class="metric-note">{note}</div>
            </div>
            """, unsafe_allow_html=True)

    l1, l2 = st.columns([1.1, 1.4])

    with l1:
        st.plotly_chart(make_gauge(row["TravelScore"], f"{country} Travel Score"), use_container_width=True)

    with l2:
        details = pd.DataFrame({
            "Metric": ["Temperature", "Humidity", "Wind", "Precipitation", "Pressure", "Visibility"],
            "Value": [
                f"{row['Temperature']:.1f} °C",
                f"{row['Humidity']:.0f} %",
                f"{row['Wind']:.1f}",
                f"{row['Precipitation']:.1f} mm",
                f"{row['Pressure']:.1f} mb",
                f"{row['Visibility']:.1f} km"
            ]
        })
        st.dataframe(details, use_container_width=True, hide_index=True)

        st.markdown("### Destination Brief")
        st.write(advisory_from_row(row))

    # Mini radar vs global average
    global_avg = country_df.mean(numeric_only=True)
    fig = radar_compare(row, global_avg, country, "Global Avg")
    st.plotly_chart(fig, use_container_width=True)

    st.markdown('</div>', unsafe_allow_html=True)

# =========================================================
# SECTION: TRAVEL READINESS
# =========================================================
elif view == "🚦 Travel Readiness":
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("🚦 Travel Readiness")

    readiness_mode = st.selectbox(
        "Select Operational Readiness View",
        ["Overall Travel Score", "Field Readiness", "Air Travel Caution", "Road Readiness"]
    )

    metric_map = {
        "Overall Travel Score": "TravelScore",
        "Field Readiness": "FieldReadiness",
        "Air Travel Caution": "AirCaution",
        "Road Readiness": "RoadReadiness"
    }

    metric = metric_map[readiness_mode]

    top_good = country_df.sort_values(metric, ascending=False).head(10)[["Country", metric]]
    top_risk = country_df.sort_values(metric, ascending=True).head(10)[["Country", metric]]

    c1, c2 = st.columns(2)

    with c1:
        fig1 = px.bar(
            top_good,
            x=metric,
            y="Country",
            orientation="h",
            title=f"Top 10 Best: {readiness_mode}",
            color=metric,
            color_continuous_scale="Tealgrn"
        )
        fig1.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#dff6ff"),
            yaxis=dict(categoryorder="total ascending"),
            height=500
        )
        st.plotly_chart(fig1, use_container_width=True)

    with c2:
        fig2 = px.bar(
            top_risk,
            x=metric,
            y="Country",
            orientation="h",
            title=f"Top 10 Risky: {readiness_mode}",
            color=metric,
            color_continuous_scale="RdPu"
        )
        fig2.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#dff6ff"),
            yaxis=dict(categoryorder="total ascending"),
            height=500
        )
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown("### Quick Interpretation")
    st.write(
        "This view helps planners quickly identify which destinations are more suitable for immediate travel or field deployment "
        "and which ones may require delay, mitigation, or alternate transport strategies."
    )

    st.markdown('</div>', unsafe_allow_html=True)

# =========================================================
# SECTION: COMPARE DESTINATIONS
# =========================================================
elif view == "⚖️ Compare Destinations":
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("⚖️ Compare Destinations")

    countries = sorted(country_df["Country"].unique())
    c1, c2 = st.columns(2)

    with c1:
        country1 = st.selectbox("Select Country A", countries, index=0)
    with c2:
        default_index = 1 if len(countries) > 1 else 0
        country2 = st.selectbox("Select Country B", countries, index=default_index)

    row1 = country_df[country_df["Country"] == country1].iloc[0]
    row2 = country_df[country_df["Country"] == country2].iloc[0]

    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">{country1} Travel Score</div>
            <div class="metric-value">{row1['TravelScore']:.1f}</div>
            <div class="metric-note">{row1['TravelStatus']}</div>
        </div>
        """, unsafe_allow_html=True)
    with m2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">{country2} Travel Score</div>
            <div class="metric-value">{row2['TravelScore']:.1f}</div>
            <div class="metric-note">{row2['TravelStatus']}</div>
        </div>
        """, unsafe_allow_html=True)
    with m3:
        winner = country1 if row1["TravelScore"] >= row2["TravelScore"] else country2
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Safer Choice</div>
            <div class="metric-value" style="font-size:1.15rem;">{winner}</div>
            <div class="metric-note">Higher mission suitability</div>
        </div>
        """, unsafe_allow_html=True)
    with m4:
        gap = abs(row1["TravelScore"] - row2["TravelScore"])
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Score Gap</div>
            <div class="metric-value">{gap:.1f}</div>
            <div class="metric-note">Difference in conditions</div>
        </div>
        """, unsafe_allow_html=True)

    fig = radar_compare(row1, row2, country1, country2)
    st.plotly_chart(fig, use_container_width=True)

    compare_df = pd.DataFrame({
        "Metric": ["Temperature", "Humidity", "Wind", "Precipitation", "UV", "Visibility", "Field Readiness", "Air Caution", "Road Readiness"],
        country1: [
            round(row1["Temperature"], 2), round(row1["Humidity"], 2), round(row1["Wind"], 2),
            round(row1["Precipitation"], 2), round(row1["UV"], 2), round(row1["Visibility"], 2),
            round(row1["FieldReadiness"], 2), round(row1["AirCaution"], 2), round(row1["RoadReadiness"], 2)
        ],
        country2: [
            round(row2["Temperature"], 2), round(row2["Humidity"], 2), round(row2["Wind"], 2),
            round(row2["Precipitation"], 2), round(row2["UV"], 2), round(row2["Visibility"], 2),
            round(row2["FieldReadiness"], 2), round(row2["AirCaution"], 2), round(row2["RoadReadiness"], 2)
        ]
    })
    st.dataframe(compare_df, use_container_width=True, hide_index=True)

    st.markdown('</div>', unsafe_allow_html=True)

# =========================================================
# SECTION: GEO OPERATIONS
# =========================================================
elif view == "🛰 Geo Operations":
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("🛰 Geo Operations")

    map_metric = st.selectbox(
        "Select Geo Layer",
        ["Travel Score", "Field Readiness", "Air Travel Caution", "Road Readiness", "Temperature", "Precipitation", "UV"]
    )

    metric_map = {
        "Travel Score": "TravelScore",
        "Field Readiness": "FieldReadiness",
        "Air Travel Caution": "AirCaution",
        "Road Readiness": "RoadReadiness",
        "Temperature": "Temperature",
        "Precipitation": "Precipitation",
        "UV": "UV"
    }

    metric = metric_map[map_metric]

    fig = px.scatter_geo(
        country_df,
        lat="Latitude",
        lon="Longitude",
        hover_name="Country",
        size=metric,
        color=metric,
        projection="natural earth",
        title=f"Global {map_metric} View",
        size_max=22,
        color_continuous_scale="Turbo",
        hover_data={
            "TravelScore": True,
            "FieldReadiness": True,
            "AirCaution": True,
            "RoadReadiness": True,
            "Temperature": ':.1f',
            "Humidity": ':.1f',
            "Wind": ':.1f',
            "Precipitation": ':.1f',
            "Visibility": ':.1f'
        }
    )
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        geo=dict(
            bgcolor="rgba(0,0,0,0)",
            showland=True,
            landcolor="rgba(255,255,255,0.04)",
            showocean=True,
            oceancolor="rgba(0,180,255,0.03)",
            showcountries=True,
            countrycolor="rgba(255,255,255,0.12)"
        ),
        font=dict(color="#e8f8ff"),
        height=650,
        margin=dict(l=10, r=10, t=50, b=10)
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown('</div>', unsafe_allow_html=True)

# =========================================================
# SECTION: SITUATION BRIEF
# =========================================================
elif view == "📖 Situation Brief":
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("📖 Situation Brief")

    avg_score = country_df["TravelScore"].mean()
    best_country = country_df.loc[country_df["TravelScore"].idxmax(), "Country"]
    worst_country = country_df.loc[country_df["TravelScore"].idxmin(), "Country"]
    high_heat = (country_df["Temperature"] > 35).sum()
    low_visibility = (country_df["Visibility"] < 5).sum()
    rain_disruption = (country_df["Precipitation"] > 8).sum()

    c1, c2, c3, c4 = st.columns(4)
    summary_cards = [
        ("Global Avg Travel Score", f"{avg_score:.1f}", "Average mission suitability"),
        ("Best Current Destination", best_country, "Highest travel score"),
        ("Most Challenging Destination", worst_country, "Lowest travel score"),
        ("High Heat Risk Zones", str(int(high_heat)), "Countries above 35°C")
    ]

    for col, (label, value, note) in zip([c1, c2, c3, c4], summary_cards):
        with col:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">{label}</div>
                <div class="metric-value" style="font-size:1.25rem;">{value}</div>
                <div class="metric-note">{note}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("### Executive Situation Summary")

    summary_text = f"""
- The current global average travel suitability score across tracked destinations is approximately {avg_score:.1f}/100.
- {best_country} currently appears as one of the most favorable destinations for travel planning based on the combined weather-driven suitability model.
- {worst_country} shows the highest operational caution based on environmental stress factors such as temperature, wind, rain, UV, or visibility.
- {int(high_heat)} countries show elevated heat exposure conditions above 35°C, which may affect outdoor movement and field operations.
- {int(low_visibility)} countries show low-visibility concerns below 5 km, which can influence road or air navigation.
- {int(rain_disruption)} countries show moderate-to-high precipitation pressure, increasing the possibility of movement disruption.
"""
    st.write(summary_text)

    # Bubble chart
    fig = px.scatter(
        country_df,
        x="Temperature",
        y="Humidity",
        size="TravelScore",
        color="TravelScore",
        hover_name="Country",
        title="Climate Pressure vs Travel Suitability",
        color_continuous_scale="Turbo"
    )
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#e8f8ff"),
        height=550
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown('</div>', unsafe_allow_html=True)

# =========================================================
# SECTION: ABOUT
# =========================================================
elif view == "ℹ️ About":
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("ℹ️ About")

    st.write("""
ClimateScope X is a smart climate-aware travel planning application designed to support destination assessment, field movement readiness, and operational decision-making using global weather conditions.

This project transforms raw climate data into practical travel suitability intelligence by evaluating:

- destination travel score
- field deployment readiness
- air travel caution
- road movement suitability
- climate-driven operational risk indicators

### Core Idea
Instead of showing weather values as raw numbers alone, the application converts them into a travel planning decision-support system that can help evaluate whether a destination is:

- Recommended
- Suitable with caution
- Better delayed or avoided

### Dataset Basis
The application uses `GlobalWeatherRepository.csv` and automatically detects key climate fields such as:

- Country
- Latitude / Longitude
- Temperature
- Humidity
- Wind
- Precipitation
- Pressure
- UV Index
- Visibility

### Technical Highlights
- Fast cached loading with `@st.cache_data`
- Premium dark neon glass UI in Streamlit
- Travel suitability scoring logic
- Interactive destination comparison
- Geo operations mapping
- Actionable climate brief generation

### Use Cases
- Field inspection planning
- Government / disaster response pre-checks
- Travel risk screening
- Outdoor operation readiness
- Climate-aware route or destination prioritization
""")

    st.markdown('</div>', unsafe_allow_html=True)

# =========================================================
# FOOTER
# =========================================================
st.markdown("""
<div class="footer-text">
Dinesh Kanna's Infosys Springboard ClimateScope Project
</div>
""", unsafe_allow_html=True)