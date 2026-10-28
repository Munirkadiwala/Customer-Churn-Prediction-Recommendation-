"""
Data Preprocessing Module
"""
import pandas as pd
import numpy as np
import pickle
import os
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split
from src.data_loader import TARGET_COL, EXCLUDE_COLS


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    before = len(df)
    df = df.drop_duplicates()
    print(f"Removed {before - len(df)} duplicates")
    for col in df.select_dtypes(include=[np.number]).columns:
        if df[col].isnull().any():
            df[col] = df[col].fillna(df[col].median())
    for col in df.select_dtypes(include=["object"]).columns:
        if df[col].isnull().any():
            df[col] = df[col].fillna(df[col].mode()[0])
    print(f"Missing after cleaning: {df.isnull().sum().sum()}")
    return df


def encode_target(df: pd.DataFrame) -> pd.DataFrame:
    col = df[TARGET_COL]
    if col.dtype == object:
        df[TARGET_COL] = (col.str.strip().str.lower() == "yes").astype(int)
    elif col.dtype == bool:
        df[TARGET_COL] = col.astype(int)
    else:
        df[TARGET_COL] = col.astype(int)
    print(f"Target — Active(0): {(df[TARGET_COL]==0).sum():,} | Churned(1): {(df[TARGET_COL]==1).sum():,}")
    return df


def encode_features(df: pd.DataFrame, categorical_cols: list,
                     save_dir: str = None) -> pd.DataFrame:
    encoders = {}
    for col in categorical_cols:
        if col in df.columns:
            le = LabelEncoder()
            df[col] = le.fit_transform(df[col].astype(str))
            encoders[col] = le
    if save_dir:
        os.makedirs(save_dir, exist_ok=True)
        with open(os.path.join(save_dir, "label_encoders.pkl"), "wb") as f:
            pickle.dump(encoders, f)
    print(f"Encoded {len(categorical_cols)} categorical columns")
    return df


def scale_features(df: pd.DataFrame, numerical_cols: list,
                    save_dir: str = None) -> pd.DataFrame:
    scaler = StandardScaler()
    df[numerical_cols] = scaler.fit_transform(df[numerical_cols])
    if save_dir:
        os.makedirs(save_dir, exist_ok=True)
        with open(os.path.join(save_dir, "scaler.pkl"), "wb") as f:
            pickle.dump(scaler, f)
    print(f"Scaled {len(numerical_cols)} numerical columns")
    return df


def split_data(df: pd.DataFrame, feature_cols: list,
               test_size: float = 0.2, random_state: int = 42):
    X = df[feature_cols]
    y = df[TARGET_COL]
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state, stratify=y
    )
    print(f"Train: {len(X_train):,} | Test: {len(X_test):,}")
    return X_train, X_test, y_train, y_test
