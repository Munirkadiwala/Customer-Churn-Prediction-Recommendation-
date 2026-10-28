# Customer Churn Prediction and Recommendation

**Student:** Kadiwala Munir Ahmed Moh. Husen | **Enrollment:** 25IC03CA009  
**Program:** MCA (ICA-10) | **Mentor:** Mr. Srikant Singh  
**Domain:** Data Science – Machine Learning

---

## Dataset
The dashboard and pipeline expect `data/indian_netflix_churn_dataset_v2.csv`.
The customer-level dataset is not included in this repository. Add a dataset
you are authorized to use at that path, or upload a CSV in the dashboard.

| Column | Description |
|---|---|
| Customer_ID | Unique identifier (excluded from ML) |
| Customer_Name | Customer name (excluded from ML) |
| Gender | Male / Female |
| Age | Customer age |
| State / City | Location |
| Occupation | Job type |
| Monthly_Income | Monthly income (₹) |
| Subscription_Plan | Mobile / Basic / Standard / Premium |
| Monthly_Fee | Plan fee (₹) |
| Tenure_Months | Months as customer |
| Watch_Hours_Per_Month | Monthly usage |
| Favorite_Genre | Preferred content genre |
| Device_Type | Smart TV / Mobile / Laptop / Tablet / Desktop |
| Payment_Method | UPI / Credit Card / Debit Card / etc. |
| Customer_Satisfaction | Rating 1–5 |
| Support_Tickets | Number of tickets raised |
| Buffering_Complaints | Number of buffering issues |
| Concurrent_Screens | Screens used simultaneously |
| Recommendation_Clicks | Content recommendations clicked |
| **Churn** | **Target: 0 = Active, 1 = Churned** |
| Churn_Type | Reason (excluded — data leakage) |

---

## Project Structure

```
customer_churn_project/
├── data/                  ← Place the authorized CSV here (not tracked)
├── notebooks/
│   └── 05_ml_models.ipynb ← Full ML pipeline
├── src/
│   ├── data_loader.py
│   ├── preprocessor.py
│   ├── model_trainer.py
│   └── recommendation_engine.py
├── dashboard/
│   └── app.py             ← Streamlit dashboard
├── models/                ← Saved models (auto-created)
├── outputs/               ← Charts & CSV (auto-created; CSVs are not tracked)
└── requirements.txt
```

## Setup

```bash
cd customer_churn_project
pip install -r requirements.txt
```

Put an authorized dataset at `data/indian_netflix_churn_dataset_v2.csv` before
running the pipeline. Customer-level input data and generated prediction CSVs
are excluded from version control.

## Run Dashboard

```bash
streamlit run dashboard/app.py
```

## Run ML Pipeline

Run the complete pipeline from the project root:

```bash
python run_pipeline.py
```

You can also open a notebook under `notebooks/` in Jupyter and run its cells.

## ML Models

| Model | Library |
|---|---|
| Logistic Regression | scikit-learn |
| Decision Tree | scikit-learn |
| Random Forest | scikit-learn |
| XGBoost | xgboost |

**Metrics:** Accuracy · Precision · Recall · F1-Score · ROC-AUC
"# Customer-Churn-Prediction-Recommendation-" 
