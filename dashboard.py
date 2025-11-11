import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

st.title("Network Coverage Quality Map")

# Load data from CSV URL
url = "https://raw.githubusercontent.com/hassan925/Signal-Strength-Dasboard/refs/heads/main/Signal%20Strength%20Data.csv"
data = pd.read_csv(url)

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

# Monotone color scale for quality
# You can change the base color (blue scale used here)
quality_shades = {
    "Bad": "#a6c8ff",        # light blue
    "Moderate": "#6ba8ff",   # medium blue
    "Good": "#2c7dfc",       # dark blue
    "Great": "#004bb7",      # darkest blue
    "No Coverage": "#bfbfbf" # grey
}

# Add markers
for _, row in filtered_data.iterrows():
    quality = row["Signal Quality"]
    color = quality_shades.get(quality, "#bfbfbf")

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

# Add legend dynamically (for only selected network)
legend_html = f"""
     <div style="
         position: fixed;
         bottom: 50px;
         left: 50px;
         width: 180px;
         height: 160px;
         background-color: white;
         border:2px solid grey;
         z-index:9999;
         font-size:14px;
         padding: 10px;">
     <b>{selected_network} Coverage</b><br>
     <i style="background:{quality_shades['Bad']}; width:15px; height:15px; float:left; margin-right:5px;"></i> Bad<br>
     <i style="background:{quality_shades['Moderate']}; width:15px; height:15px; float:left; margin-right:5px;"></i> Moderate<br>
     <i style="background:{quality_shades['Good']}; width:15px; height:15px; float:left; margin-right:5px;"></i> Good<br>
     <i style="background:{quality_shades['Great']}; width:15px; height:15px; float:left; margin-right:5px;"></i> Great<br>
     <i style="background:{quality_shades['No Coverage']}; width:15px; height:15px; float:left; margin-right:5px;"></i> No Coverage<br>
     </div>
"""
m.get_root().html.add_child(folium.Element(legend_html))

# Show map in Streamlit
st_folium(m, width=850, height=600)
