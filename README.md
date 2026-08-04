# County-Level Public Health Explorer

An interactive dashboard exploring how food insecurity, insurance access, obesity, and smoking relate to diabetes prevalence across roughly 3,000 US counties.

**Live app:** https://health-dashboard-qbnntdzwx4vrjertgevr4m.streamlit.app/

## Key findings

- Food insecurity is more strongly correlated with diabetes prevalence (r = 0.77) than obesity (r = 0.67), smoking (r = 0.71), or lack of health insurance (r = 0.45).
- A multiple regression controlling for obesity, smoking, insurance access, and food insecurity at the same time (R² = 0.71) shows food insecurity is still the strongest independent predictor. Lack of insurance loses statistical significance (p = 0.076) once the other factors are accounted for. This suggests insurance access's apparent relationship with diabetes in the simple correlation was largely explained by its overlap with food insecurity (r = 0.74 between the two).
- County-level diabetes rates follow the well-documented "Diabetes Belt" pattern, concentrated across the Southeastern US.

## Data source

[CDC PLACES: Local Data for Better Health](https://data.cdc.gov/500-Cities-Places/PLACES-County-Data-GIS-Friendly-Format-2025-releas/i46a-9kgh), 2025 release, county-level modeled estimates from BRFSS survey data.

## Tech stack

- Python, pandas: data cleaning and analysis
- statsmodels: regression analysis
- Plotly: interactive charts and choropleth map
- Streamlit: dashboard framework and deployment

## Running locally

```bash
git clone https://github.com/Savannahwilcox/health-dashboard.git
cd health-dashboard
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

## Limitations

- This is county-level (ecological) data, meaning aggregated averages rather than individual patient records. The relationships shown are population-level patterns, not individual-level or causal claims.
- About 187 counties are excluded due to suppressed CDC estimates (insufficient survey sample size). Food insecurity data is unavailable for Tennessee and Texas, since both states opted out of that BRFSS survey module in this release.
