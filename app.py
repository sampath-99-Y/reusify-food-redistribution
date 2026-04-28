import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import random
import datetime

st.set_page_config(page_title="Reusify", layout="wide")

# =========================
# 🎨 UI
# =========================
st.title("♻️ Reusify - A Responsibility")
st.caption("Smart Food Redistribution Dashboard")

st.caption(f"🕒 Live Time: {datetime.datetime.now().strftime('%H:%M:%S')}")

# =========================
# LOAD DATA
# =========================
ngos = pd.read_csv("data/ngos.csv")
restaurants_df = pd.read_csv("data/restaurants.csv")

# =========================
# BUTTON
# =========================
if st.button("🚀 Run Smart Allocation"):

    restaurants = []
    for _, r in restaurants_df.iterrows():
        restaurants.append({
            "name": r["name"],
            "lat": r["lat"],
            "lon": r["lon"],
            "food": random.randint(30, 100)
        })

    results = []
    for i, r in enumerate(restaurants):
        ngo = ngos.iloc[i % len(ngos)]

        results.append({
            "restaurant": r["name"],
            "r_lat": r["lat"],
            "r_lon": r["lon"],
            "ngo": ngo["name"],
            "n_lat": ngo["lat"],
            "n_lon": ngo["lon"],
            "food": r["food"],
            "demand": ngo["demand"]
        })

    df = pd.DataFrame(results)

    # =========================
    # 🗺️ CLEAR MAP (GOOGLE STYLE)
    # =========================
    st.subheader("🗺️ Global Smart Allocation Map")

    fig = go.Figure()

    # Restaurants
    fig.add_trace(go.Scattermapbox(
        lat=df["r_lat"],
        lon=df["r_lon"],
        mode='markers',
        marker=dict(size=14, color='blue'),
        text=df["restaurant"],
        hovertemplate="<b>%{text}</b><br>Food: %{customdata[0]}<extra></extra>",
        customdata=df[["food"]],
        name="Restaurants"
    ))

    # NGOs
    colors = ["red" if d >= 60 else "green" for d in df["demand"]]

    fig.add_trace(go.Scattermapbox(
        lat=df["n_lat"],
        lon=df["n_lon"],
        mode='markers',
        marker=dict(size=16, color=colors),
        text=df["ngo"],
        hovertemplate="<b>%{text}</b><br>Demand: %{customdata[0]}<extra></extra>",
        customdata=df[["demand"]],
        name="NGOs"
    ))

    # Routes
    for i in range(len(df)):
        fig.add_trace(go.Scattermapbox(
            lat=[df.loc[i, "r_lat"], df.loc[i, "n_lat"]],
            lon=[df.loc[i, "r_lon"], df.loc[i, "n_lon"]],
            mode='lines',
            line=dict(width=3, color='orange'),
            showlegend=False
        ))

    # MAP SETTINGS (THIS IS THE FIX)
    fig.update_layout(
        mapbox_style="open-street-map",   # 🔥 CLEAR MAP WITH LABELS
        mapbox_zoom=12,
        mapbox_center={
            "lat": df["r_lat"].mean(),
            "lon": df["r_lon"].mean()
        },
        height=650,
        margin={"r":0,"t":0,"l":0,"b":0}
    )

    st.plotly_chart(fig, use_container_width=True)

    # =========================
    # TABLE
    # =========================
    st.subheader("📋 Allocation Details")
    st.dataframe(df)

    st.success("✅ Map now shows full roads, labels, and zoom!")