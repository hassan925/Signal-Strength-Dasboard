import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

st.title("Network Coverage Quality Map (Dynamic Averages)")

# Load data from CSV URL
url = "https://raw.githubusercontent.com/hassan925/Signal-Strength-Dasboard/refs/heads/main/Signal%20Strength%20Data.csv"
data = pd.read_csv(url)
data.columns = data.columns.str.strip()  # remove extra spaces

# Dropdown filter
selected_network = st.selectbox(
    "Select a Network",
    sorted(data["Network"].unique())
)

# Filter data by selected network
filtered_data = data[data["Network"] == selected_network]

# Create base map
m = folium.Map(
    location=[filtered_data['Y'].mean(), filtered_data['X'].mean()],
    zoom_start=10
)

# Color scheme
quality_colors = {
    "Bad": "red",
    "Moderate": "orange",
    "Good": "blue",
    "Great": "green",
    "No Coverage": "grey"
}

# Add markers
for _, row in filtered_data.iterrows():
    quality = row["Signal Quality"]
    color = quality_colors.get(quality, "#bfbfbf")

    folium.CircleMarker(
        location=[row['Y'], row['X']],
        radius=2,
        color=color,
        fill=True,
        fill_color=color,
        fill_opacity=0.7,
        tooltip=(
            f"<b>Network:</b> {row['Network']}<br>"
            f"<b>Signal Quality:</b> {row['Signal Quality']}<br>"
            f"<b>Signal Strength:</b> {row['Signal Strength']}"
        )
    ).add_to(m)

# Display map and capture map movement
returned = st_folium(m, width=850, height=600)

# -----------------------------
# 🔥 DYNAMIC AVERAGE CALCULATION
# -----------------------------
if returned and "bounds" in returned and returned["bounds"]:

    bounds = returned["bounds"]
    min_lat = bounds["south"]
    max_lat = bounds["north"]
    min_lon = bounds["west"]
    max_lon = bounds["east"]

    # Filter data within map window
    zoomed_data = filtered_data[
        (filtered_data["Y"] >= min_lat) &
        (filtered_data["Y"] <= max_lat) &
        (filtered_data["X"] >= min_lon) &
        (filtered_data["X"] <= max_lon)
    ]

    # Compute average signal quality ranking
    quality_rank = {
        "No Coverage": 0,
        "Bad": 1,
        "Moderate": 2,
        "Good": 3,
        "Great": 4
    }

    if len(zoomed_data) > 0:
        avg_rank = zoomed_data["Signal Quality"].map(quality_rank).mean()
    else:
        avg_rank = None

    # Convert numeric avg back to label
    if avg_rank is not None:
        # Find the closest label
        avg_quality = min(quality_rank, key=lambda k: abs(quality_rank[k] - avg_rank))
    else:
        avg_quality = "No Data"

else:
    avg_quality = "Zoom/Pan to update"


# -----------------------------
# 🔥 DYNAMIC LEGEND BASED ON ZOOM
# -----------------------------
legend_html = f"""
     <div style="
         position: fixed;
         bottom: 50px;
         left: 50px;
         width: 220px;
         background-color: white;
         border:2px solid grey;
         z-index:9999;
         font-size:14px;
         padding: 10px;">
     <b>{selected_network} Coverage</b><br><br>

        <b>Avg Quality (Visible Area):</b><br>
        <div style="padding:5px; background-color:#f2f2f2; border-radius:5px;">
            {avg_quality}
        </div><br>

        <i style="background:red; width:15px; height:15px; float:left; margin-right:5px;"></i> Bad<br>
        <i style="background:orange; width:15px; height:15px; float:left; margin-right:5px;"></i> Moderate<br>
        <i style="background:blue; width:15px; height:15px; float:left; margin-right:5px;"></i> Good<br>
        <i style="background:green; width:15px; height:15px; float:left; margin-right:5px;"></i> Great<br>
        <i style="background:grey; width:15px; height:15px; float:left; margin-right:5px;"></i> No Coverage<br>
     </div>
"""

m.get_root().html.add_child(folium.Element(legend_html))
