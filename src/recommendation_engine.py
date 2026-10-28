"""
Rule-Based Recommendation Engine
Uses actual dataset columns:
  Customer_Satisfaction, Support_Tickets, Buffering_Complaints,
  Subscription_Plan, Tenure_Months, Monthly_Fee, Risk_Level
"""
import pandas as pd


def generate_recommendation(row: pd.Series) -> str:
    risk         = str(row.get("Risk_Level", "Low"))
    satisfaction = row.get("Customer_Satisfaction", 5)
    tickets      = row.get("Support_Tickets", 0)
    buffering    = row.get("Buffering_Complaints", 0)
    plan         = str(row.get("Subscription_Plan", "")).lower()
    tenure       = row.get("Tenure_Months", 12)

    recs = []

    if risk == "High":
        recs.append("Offer 20% discount on next 3 months.")
        if tickets >= 5:
            recs.append("Assign priority customer support immediately.")
        if buffering >= 5:
            recs.append("Escalate buffering issues to tech team urgently.")
        if satisfaction <= 2:
            recs.append("Schedule personal satisfaction call.")
        if "mobile" in plan or "basic" in plan:
            recs.append("Offer free 1-month Premium plan upgrade.")
        recs.append("Send personalised loyalty reward.")

    elif risk == "Medium":
        recs.append("Offer 10% loyalty discount on renewal.")
        if satisfaction <= 3:
            recs.append("Send customer satisfaction survey.")
        if tenure < 6:
            recs.append("Provide early-loyalty bonus reward.")
        recs.append("Recommend premium content based on Favorite Genre.")

    else:  # Low risk
        recs.append("Send thank-you message for continued loyalty.")
        recs.append("Notify about new features and upcoming content.")

    return " | ".join(recs)


def apply_recommendations(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["Recommendation"] = df.apply(generate_recommendation, axis=1)
    return df


def get_recommendation_summary(df: pd.DataFrame) -> pd.DataFrame:
    if "Risk_Level" not in df.columns:
        raise ValueError("DataFrame must have 'Risk_Level' column.")
    summary = df["Risk_Level"].value_counts().reset_index()
    summary.columns = ["Risk_Level", "Customer_Count"]
    return summary
