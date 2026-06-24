# Crash Risk Scoring Skill

## Purpose
Score the crash risk at a specific GPS location or named
place in NYC using a trained XGBoost classifier built on
500,000+ historical NYC collision records.

## When to Use This Skill
- User asks about safety of a specific location
- User asks "is it safe to drive through X"
- Route finding skill needs risk scores for waypoints
- User asks about crash history in an area

## Tools Available
- `score_crash_risk(latitude, longitude)` → returns risk_score
  (0.0 to 1.0), risk_level (Low/Medium/High), and explanation

## Risk Score Interpretation
- 0.00 to 0.35 → Low risk, safe to proceed
- 0.35 to 0.65 → Medium risk, proceed with caution
- 0.65 to 1.00 → High risk, human review required

## Execution Steps
1. Convert location name to coordinates if needed
2. Call score_crash_risk with latitude and longitude
3. Return risk level and plain-English explanation
4. If High: trigger human-in-the-loop confirmation

## Model Details
- Algorithm: XGBoost classifier
- Training data: 500,000+ NYC collision records
- Features: location, hour, day of week, month
- Performance: F1 0.848, AUC 0.971