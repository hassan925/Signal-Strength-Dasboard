import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

st.title("Network Availability Map")

# Load data from CSV URL
url = "https://raw.githubusercontent.com/hassan925/Signal-Strength-Dasboard/refs/heads/main/Signal%20Strength%20Data.csv"
data = pd.read_csv(url)

# Create Folium map centered around mean coordinates
m = folium.Map(location=[data['Y'].mean(), data['X'].mean()], zoom_start=10)

# Define colors for networks
network_colors = {
    "Jazz": "red",
    "Zong": "green",
    "Telenor": "blue",
}

# Default fallback color
default_color = "gray"

# Add circle markers
for _, row in data.iterrows():
    network = row['Network']
    color = network_colors.get(network, default_color)

    folium.CircleMarker(
        location=[row['Y'], row['X']],
        radius=1,
        color=color,
        fill=True,
        fill_color=color,
        fill_opacity=0.7,
        tooltip=(
            f"Network: {network}<br>"
            f"Signal Strength: {row['Signal Strength']}"
        )
    ).add_to(m)

# Add custom legend
legend_html = """
     <div style="
         position: fixed; 
         bottom: 50px; 
         left: 50px; 
         width: 150px; 
         height: 130px; 
         background-color: white; 
         border:2px solid grey; 
         z-index:9999; 
         font-size:14px;
         padding: 10px;">
     <b>Legend</b><br>
     <i style="background:red; width:10px; height:10px; float:left; margin-right:5px;"></i> Jazz<br>
     <i style="background:green; width:10px; height:10px; float:left; margin-right:5px;"></i> Zong<br>
     <i style="background:blue; width:10px; height:10px; float:left; margin-right:5px;"></i> Telenor<br>
     </div>
"""
m.get_root().html.add_child(folium.Element(legend_html))

# Render map
st_folium(m, width=800, height=600)
