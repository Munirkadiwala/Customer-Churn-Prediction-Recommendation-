"""
Machine Learning Model Training & Evaluation
Models: Logistic Regression, Decision Tree, Random Forest, XGBoost
"""
import pandas as pd
import numpy as np
import pickle
import os
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score,
    f1_score, roc_auc_score
)

MODELS = {
    "Logistic Regression": LogisticRegression(max_iter=1000, random_state=42),
    "Decision Tree":       DecisionTreeClassifier(random_state=42),
    "Random Forest":       RandomForestClassifier(n_estimators=100, random_state=42),
    "XGBoost":             XGBClassifier(use_label_encoder=False,
                                         eval_metric="logloss",
                                         random_state=42, verbosity=0),
}


def train_all_models(X_train, y_train) -> dict:
    trained = {}
    for name, model in MODELS.items():
        model.fit(X_train, y_train)
        trained[name] = model
        print(f"Trained: {name}")
    return trained


def evaluate_model(model, X_test, y_test, model_name: str = "") -> dict:
    y_pred = model.predict(X_test)
    y_prob = model.predict_proba(X_test)[:, 1]
    return {
        "model":     model_name,
        "accuracy":  round(accuracy_score(y_test, y_pred)  * 100, 2),
        "precision": round(precision_score(y_test, y_pred) * 100, 2),
        "recall":    round(recall_score(y_test, y_pred)    * 100, 2),
        "f1_score":  round(f1_score(y_test, y_pred)        * 100, 2),
        "roc_auc":   round(roc_auc_score(y_test, y_prob)   * 100, 2),
    }


def compare_models(trained_models: dict, X_test, y_test) -> pd.DataFrame:
    results = [evaluate_model(m, X_test, y_test, n) for n, m in trained_models.items()]
    df = pd.DataFrame(results).sort_values("roc_auc", ascending=False).reset_index(drop=True)
    print("\nModel Comparison:")
    print(df.to_string(index=False))
    return df


def get_best_model(trained_models: dict, X_test, y_test):
    comparison = compare_models(trained_models, X_test, y_test)
    best_name  = comparison.iloc[0]["model"]
    print(f"\nBest Model: {best_name}")
    return best_name, trained_models[best_name], comparison


def save_model(model, model_name: str, save_dir: str = "models") -> str:
    os.makedirs(save_dir, exist_ok=True)
    path = os.path.join(save_dir, model_name.replace(" ", "_").lower() + ".pkl")
    with open(path, "wb") as f:
        pickle.dump(model, f)
    print(f"Saved: {path}")
    return path


def load_model(filepath: str):
    with open(filepath, "rb") as f:
        return pickle.load(f)


def predict_churn(model, X) -> pd.DataFrame:
    proba = model.predict_proba(X)[:, 1]
    return pd.DataFrame({
        "Churn_Probability": np.round(proba, 4),
        "Risk_Level": pd.cut(
            proba,
            bins=[-0.001, 0.3, 0.6, 1.0],
            labels=["Low", "Medium", "High"]
        )
    })
