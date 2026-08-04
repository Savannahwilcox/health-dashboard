import streamlit as st
import pandas as pd

st.set_page_config(page_title="County Health Explorer", layout="wide")

st.title("County-Level Public Health Explorer")
st.write("Exploring how food insecurity and insurance access relate to chronic disease across US counties.")

@st.cache_data
def load_data():
    data = pd.read_csv("data/places_clean.csv")
    data["fips_str"] = data["CountyFIPS"].astype(str).str.zfill(5)
    return data

df = load_data()
st.dataframe(df.head(20))

st.sidebar.header("Filters")

states = sorted(df["StateDesc"].unique())
selected_states = st.sidebar.multiselect("State(s)", states, default=[])

indicator_options = {
    "Diabetes": "DIABETES_CrudePrev",
    "Obesity": "OBESITY_CrudePrev",
    "No Insurance": "ACCESS2_CrudePrev",
    "Smoking": "CSMOKING_CrudePrev",
    "Food Insecurity": "FOODINSECU_CrudePrev",
}
selected_label = st.sidebar.selectbox("Indicator to explore", list(indicator_options.keys()))
selected_col = indicator_options[selected_label]

filtered = df[df["StateDesc"].isin(selected_states)] if selected_states else df

st.subheader("Summary")
col1, col2, col3 = st.columns(3)
col1.metric(f"Avg {selected_label}", f"{filtered[selected_col].mean():.1f}%")
col2.metric("Highest County", f"{filtered[selected_col].max():.1f}%")
col3.metric("Lowest County", f"{filtered[selected_col].min():.1f}%")

st.subheader(f"{selected_label} by County")
st.dataframe(filtered[["CountyName", "StateAbbr", selected_col]].sort_values(selected_col, ascending=False))

import plotly.express as px

st.subheader(f"Food Insecurity vs. {selected_label}")
scatter_fig = px.scatter(
    filtered, x="FOODINSECU_CrudePrev", y=selected_col,
    hover_data=["CountyName", "StateAbbr"],
    trendline="ols",
    labels={"FOODINSECU_CrudePrev": "Food Insecurity (%)", selected_col: f"{selected_label} (%)"},
)
st.plotly_chart(scatter_fig, use_container_width=True)

import json
from urllib.request import urlopen

@st.cache_resource
def load_geojson():
    with urlopen("https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json") as response:
        return json.load(response)

counties_geojson = load_geojson()

st.subheader(f"{selected_label} by County (Map)")
map_fig = px.choropleth(
    filtered, geojson=counties_geojson, locations="fips_str",
    color=selected_col, color_continuous_scale="Reds",
    labels={selected_col: selected_label},
    hover_data=["CountyName", "StateAbbr"],
)
map_fig.update_traces(marker_line_width=0)
map_fig.update_layout(height=600, margin={"r": 0, "t": 0, "l": 0, "b": 0})
map_fig.update_geos(visible=False, projection_type="albers usa")
st.plotly_chart(map_fig, use_container_width=True)

st.caption(
    "Data: CDC PLACES 2025 release, county-level modeled estimates from BRFSS survey data. "
    "Correlations are ecological (county-level aggregates), not individual-level, and should not "
    "be read as causal. Some counties are excluded due to suppressed estimates (insufficient survey sample size)."
)