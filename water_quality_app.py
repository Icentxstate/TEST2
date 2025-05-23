import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import folium
from streamlit_folium import st_folium

# Set page configuration
st.set_page_config(layout="wide")

# --- Load Data ---
file_path = r"S:\TSCI\MCWE\MCWE-Projects\Watershed Services\4-Data & Research\Monitoring\Watershed Monitoring\CRP\3 - Data\2. Cypress Creek\Surface water\INPUT.CSV"
df = pd.read_csv(file_path, encoding='latin1')

# --- Preprocess Date ---
df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
df['YearMonth'] = df['Date'].dt.to_period('M').dt.to_timestamp()

# --- Sidebar Selections ---
st.title("📈 Water Quality Time Series Dashboard")

# Site selection
site_options = df[['Site ID', 'Site Name']].drop_duplicates()
site_options['Site Display'] = site_options['Site ID'].astype(str) + " - " + site_options['Site Name']
site_dict = dict(zip(site_options['Site Display'], site_options['Site ID']))

selected_sites_display = st.sidebar.multiselect(
    label="Select Site(s):",
    options=site_dict.keys(),
    default=list(site_dict.keys())[:2]
)
selected_sites = [site_dict[label] for label in selected_sites_display]

# Parameter selection
numeric_columns = df.select_dtypes(include='number').columns.tolist()
default_params = ['TDS', 'Nitrate (µg/L)']
valid_defaults = [p for p in default_params if p in numeric_columns]

selected_parameters = st.sidebar.multiselect(
    label="Select Parameters (up to 10):",
    options=numeric_columns,
    default=valid_defaults
)

# --- Static Site Location Data ---
locations = pd.DataFrame({
    'Site ID': [12673, 12674, 12675, 12676, 12677, 22109, 22110],
    'Description': [
        'CYPRESS CREEK AT BLANCO RIVER',
        'CYPRESS CREEK AT FM 12',
        'CYPRESS CK - BLUE HOLE CAMPGRD',
        'CYPRESS CREEK AT RR 12',
        'CYPRESS CREEK AT JACOBS WELL',
        'CYPRESS CREEK AT CAMP YOUNG JUDAEA',
        'CYPRESS CREEK AT WOODCREEK DRIVE DAM'
    ],
    'Longitude': [-98.094754, -98.09753, -98.09084, -98.104139, -98.126321, -98.12015, -98.117508],
    'Latitude': [29.991514, 29.996859, 30.002777, 30.012356, 30.034408, 30.02434, 30.020925]
})

# --- Layout with Columns ---
col1, col2 = st.columns([1, 3])

with col1:
    st.subheader("🗺️ Monitoring Sites Map")
    m = folium.Map(location=[30.01, -98.11], zoom_start=13)
    for _, row in locations.iterrows():
        folium.Marker(
            location=[row['Latitude'], row['Longitude']],
            popup=f"{row['Site ID']}: {row['Description']}",
            tooltip=row['Description'],
            icon=folium.Icon(color='blue', icon='info-sign')
        ).add_to(m)
    st_folium(m, width=600, height=400)

with col2:
    st.header("📊 Time Series Charts")
    plot_df = df[df['Site ID'].isin(selected_sites)]

    if not selected_parameters:
        st.warning("Please select at least one parameter.")
    else:
        for param in selected_parameters:
            fig, ax = plt.subplots(figsize=(10, 4))
            sns.lineplot(
                data=plot_df,
                x='YearMonth', y=param, hue='Site Name', marker='o', ax=ax
            )
            ax.set_title(f"{param} Over Time (Monthly)")
            ax.set_xlabel("Year-Month")
            ax.set_ylabel(param)
            ax.legend(title='Site')
            ax.grid(True)
            st.pyplot(fig)

st.markdown("---")
st.caption("Data Source: CRP Monitoring at Cypress Creek")
