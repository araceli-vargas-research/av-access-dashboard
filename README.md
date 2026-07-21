# Autonomous Vehicle Access and Safety Dashboard

Starter repository for a Plotly + Streamlit dashboard tracking:

- Waymo safety metrics
- Consumer access by state and market
- NHTSA ADS incidents
- State AV legislation and policy
- Census demographics and geographic boundaries
- Optional Waymo Open Motion Dataset summaries

## Run locally

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

## Data rules

Keep source files in `data/raw/`.
Save cleaned files in `data/processed/`.
Do not upload full Waymo sensor datasets to GitHub.
