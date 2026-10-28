"""
Data Loading Module
Dataset: Indian Netflix Customer Churn Dataset
"""
import pandas as pd
import numpy as np
import os

TARGET_COL = "Churn"

# Columns to exclude from ML features
EXCLUDE_COLS = [
    "Customer_ID",   # identifier
    "Customer_Name", # not predictive
    "Churn_Type",    # target-derived → data leakage
    "Churn"          # target
]


def load_dataset(filepath: str) -> pd.DataFrame:
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Dataset not found at: {filepath}")
    df = pd.read_csv(filepath)
    print(f"Loaded: {len(df):,} rows x {len(df.columns)} columns")
    return df


def validate_dataset(df: pd.DataFrame) -> dict:
    report = {
        "total_records":  len(df),
        "total_columns":  len(df.columns),
        "missing_values": df.isnull().sum().to_dict(),
        "duplicate_rows": int(df.duplicated().sum()),
        "dtypes":         df.dtypes.astype(str).to_dict(),
    }
    print(f"Records: {report['total_records']:,} | Duplicates: {report['duplicate_rows']} | "
          f"Missing: {sum(report['missing_values'].values())}")
    return report


def get_churn_summary(df: pd.DataFrame) -> dict:
    total   = len(df)
    churned = int(df[TARGET_COL].sum())
    active  = total - churned
    summary = {
        "total_customers":   total,
        "active_customers":  active,
        "churned_customers": churned,
        "churn_rate_pct":    round(churned / total * 100, 2),
    }
    for k, v in summary.items():
        print(f"  {k}: {v}")
    return summary


def identify_features(df: pd.DataFrame) -> dict:
    feature_cols = [c for c in df.columns if c not in EXCLUDE_COLS]
    numerical    = df[feature_cols].select_dtypes(include=[np.number]).columns.tolist()
    categorical  = df[feature_cols].select_dtypes(include=["object", "category"]).columns.tolist()
    print(f"Numerical  ({len(numerical)}): {numerical}")
    print(f"Categorical({len(categorical)}): {categorical}")
    return {"numerical": numerical, "categorical": categorical, "excluded": EXCLUDE_COLS}
