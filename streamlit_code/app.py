# BEFORE YOU BEGIN 
# Add the following packages to the Packages dropdown at the top of the UI:
# plotly, matplotlib, pydeck, snowflake-ml-python

import streamlit as st
import pydeck as pdk
import pandas as pd
import altair as alt
import matplotlib.pyplot as plt
from snowflake.ml.feature_store import FeatureStore, FeatureView, CreationMode
from snowflake.snowpark.context import get_active_session
from datetime import datetime, timedelta

st.title("Credit Card Fraud Detection")
st.write("Current Transactions")

session = get_active_session()
session.sql("USE ROLE SYSADMIN")

# Load and limit queried data
queried_data = session.sql("SELECT * FROM CC_FINS_DB.ANALYTICS.CREDITCARD_TRANSACTIONS").to_pandas()

# Convert date and normalize for display
queried_data['TRANSACTION_DATE'] = pd.to_datetime(queried_data['TRANSACTION_DATE'], format='%m/%d/%y %H:%M')
yesterday = datetime.now() - timedelta(days=1)
yesterday_date = yesterday.date()
queried_data['TRANSACTION_DATE'] = queried_data['TRANSACTION_DATE'].apply(
    lambda dt: dt.replace(year=yesterday_date.year, month=yesterday_date.month, day=yesterday_date.day)
)
queried_data['TRANSACTION_DATE'] = queried_data['TRANSACTION_DATE'].dt.strftime('%m/%d/%y %H:%M')

# Simulate prediction results
queried_data["CLASS"] = queried_data["LOCATION"].apply(lambda loc: 1 if loc == "Moscow" else 0)
queried_data["PROBABILITY"] = queried_data["CLASS"].apply(lambda x: 0.92 if x == 1 else 0.05)
queried_data["RESULT"] = queried_data["CLASS"].apply(lambda x: "FRAUDULENT" if x == 1 else "NORMAL")
queried_data["COLOR"] = queried_data["CLASS"].apply(lambda x: [255, 0, 0, 255] if x == 1 else [0, 128, 0, 255])

# Convert lat/lon to float
queried_data["LATITUDE"] = queried_data["LATITUDE"].astype(float)
queried_data["LONGITUDE"] = queried_data["LONGITUDE"].astype(float)

# Limit dataset size to avoid Streamlit message size error
map_data = queried_data.sort_values(by="TRANSACTION_DATE", ascending=False).head(500)

# Map tooltip
tooltip = {
    "html": "<b>Transaction:</b> {TRANSACTION_ID}<br>"
            "<b>Location:</b> {LATITUDE}, {LONGITUDE}<br>"
            "<b>Fraud Status:</b> {RESULT}<br>"
            "<b>Probability:</b> {PROBABILITY}<br>",
    "style": {"color": "white", "backgroundColor": "rgba(0, 0, 0, 0.7)", "padding": "5px"}
}

# PyDeck layer
layer = pdk.Layer(
    "ScatterplotLayer",
    data=map_data,
    get_position=["LONGITUDE", "LATITUDE"],
    opacity=0.8,
    filled=True,
    elevation_range=[0, 1000],
    extruded=True,
    coverage=1,
    get_fill_color="COLOR",
    get_radius=8000,
    pickable=True,
    radius_min_pixels=5,
    radius_scale=5,
    stroked=True,
    line_width_min_pixels=1,
    line_color=[50, 0, 0, 50],
)

view_state = pdk.ViewState(
    latitude=map_data["LATITUDE"].mean(),
    longitude=map_data["LONGITUDE"].mean(),
    zoom=3.5,
    pitch=0
)

deck = pdk.Deck(
    layers=[layer],
    initial_view_state=view_state,
    map_style="mapbox://styles/mapbox/light-v9",
    tooltip=tooltip
)

# Show map
st.title("Map Showing Transaction Locations")
st.pydeck_chart(deck)

# Show table limited to 300 rows
st.write("Prediction Results (Sample)", map_data[[
    "TRANSACTION_ID", "LOCATION", "LATITUDE", "LONGITUDE", "CLASS", "PROBABILITY", "RESULT"
]].head(300))
