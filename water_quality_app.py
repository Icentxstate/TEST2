import streamlit as st
import pandas as pd
import geopandas as gpd
import folium
from streamlit_folium import st_folium
from folium.plugins import MarkerCluster

# ---------- صفحه ---------- #
st.set_page_config(page_title="نمایش شیپ‌فایل و نقاط", layout="wide")

st.title("📍 نمایش محدوده و نقاط روی نقشه")

# ---------- بارگذاری داده‌ها ---------- #
try:
    # شیپ‌فایل حوضه آبریز
    gdf = gpd.read_file("watershed.shp")

    # CSV نقاط
    df = pd.read_csv("water_points.csv")
    df = df.dropna(subset=["Latitude", "Longitude"])

    # ---------- ساخت نقشه ---------- #
    m = folium.Map(location=[df["Latitude"].mean(), df["Longitude"].mean()], zoom_start=10, tiles="CartoDB positron")

    # اضافه کردن شیپ‌فایل به صورت لایه رنگی نیمه شفاف
    folium.GeoJson(
        gdf,
        name="Watershed",
        style_function=lambda x: {
            "fillColor": "blue",
            "color": "blue",
            "weight": 1,
            "fillOpacity": 0.2
        }
    ).add_to(m)

    # خوشه‌بندی نقاط
    marker_cluster = MarkerCluster().add_to(m)
    for _, row in df.iterrows():
        folium.Marker(
            location=[row["Latitude"], row["Longitude"]],
            popup=f"{row.get('Site Name', 'Unknown Site')}<br>{row.get('Date', '')}"
        ).add_to(marker_cluster)

    # نمایش نقشه در Streamlit
    st_folium(m, use_container_width=True)

except Exception as e:
    st.error(f"❌ خطا در بارگذاری داده‌ها یا ترسیم نقشه: {e}")
