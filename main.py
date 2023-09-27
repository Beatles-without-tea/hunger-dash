import streamlit as st
import pandas as pd

import pydeck as pdk
import geopandas as gpd

st.set_page_config(layout="wide")

# Load geospatial data
world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

wasting = pd.read_csv("cleaned_data/wasting_cleaned.csv")

# Merge the geospatial data with your dataset based on ISO codes
merged = world.set_index('iso_a3').join(wasting.set_index('ISO3Code'))

# Visualize countries based on the National_r column
view_state = pdk.ViewState(latitude=0, longitude=0, zoom=1)

# Adjust the color scaling depending on the range of values in National_r ( Point estimates)
color_expression = "[255, 255 * (1 - properties.National_r / max_value), 0]"
color_expression = color_expression.replace("max_value", str(merged['National_r'].max()))

country_layer = pdk.Layer(
    "GeoJsonLayer",
    data=merged.__geo_interface__,
    opacity=0.8,
    filled=True,
    stroked=False,
    get_fill_color=color_expression,
)

# Display the map in Streamlit
st.title("National_r Visualization based on ISO codes")
st.pydeck_chart(pdk.Deck(layers=[country_layer], initial_view_state=view_state))

