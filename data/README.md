
# Data

This directory contains data resources for the Urban Crash Safety Agent.

## NYC Motor Vehicle Collisions Dataset

The agent is built on top of 500,000+ NYC collision records from the
NYPD Motor Vehicle Collisions dataset, originally used in the
Urban Crash Analytics project (github.com/Saif-Ullah0/urban-crash-analysis-sds).

### Download the dataset

The full dataset is publicly available from NYC Open Data:
https://data.cityofnewyork.us/Public-Safety/Motor-Vehicle-Collisions-Crashes/h9gi-nx95

### Trained model

The XGBoost crash risk model (`crash_risk_model.json`) was trained on this
dataset with the following pipeline:

- 500,000+ collision records (2012 to 2024)
- Features: latitude, longitude, hour, day of week, month
- Class imbalance handled with SMOTE oversampling
- Model: XGBoost classifier
- Performance: F1 score 0.848, AUC-ROC 0.971

### For demo purposes

If the trained model file is not present, the agent falls back to a
coordinate-based simulation so the demo still runs end-to-end without
requiring the full model file. The agent's architecture, tool calling,
and human-in-the-loop logic work identically in both modes.

### How to add the real model

1. Train the model using the Urban Crash Analytics repo:
   github.com/Saif-Ullah0/urban-crash-analysis-sds
2. Export the trained XGBoost model:
   `model.save_model("data/crash_risk_model.json")`
3. Place the file in this directory
4. The agent will automatically detect and load it on startup