"""
Interactive Dashboard - Customer Churn Prediction & Recommendation
Streamlit App
"""
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

st.set_page_config(page_title="Customer Churn Dashboard", layout="wide",
                   page_icon="📊")

# ── Sidebar ──────────────────────────────────────────────────────────────────
st.sidebar.title("📁 Upload Dataset")
uploaded = st.sidebar.file_uploader("Upload customer_churn.csv", type=["csv"])

st.sidebar.markdown("---")
st.sidebar.markdown("**Project:** Customer Churn Prediction")
st.sidebar.markdown("**Domain:** MCA / Data Science - ML")

# ── Load data ─────────────────────────────────────────────────────────────────
@st.cache_data
def load_data(file):
    df = pd.read_csv(file)
    return df

if uploaded:
    df = load_data(uploaded)
else:
    sample_path = os.path.join(os.path.dirname(__file__), "..", "data", "indian_netflix_churn_dataset_v2.csv")
    if os.path.exists(sample_path):
        df = pd.read_csv(sample_path)
    else:
        st.warning("Please upload a CSV dataset using the sidebar.")
        st.stop()

# ── Normalise target column ───────────────────────────────────────────────────
churn_col = None
for c in df.columns:
    if c.lower() == "churn":
        churn_col = c
        break

if churn_col:
    if df[churn_col].dtype == object:
        df["Churn_Flag"] = (df[churn_col].str.strip().str.lower() == "yes").astype(int)
    else:
        df["Churn_Flag"] = df[churn_col].astype(int)
else:
    st.error("No 'Churn' column found in dataset.")
    st.stop()

# ── KPI Calculations ──────────────────────────────────────────────────────────
total       = len(df)
churned     = int(df["Churn_Flag"].sum())
active      = total - churned
churn_rate  = round(churned / total * 100, 2)

monthly_col = next((c for c in df.columns if "monthly" in c.lower() and
                    "charge" in c.lower()), None) or \
              next((c for c in df.columns if "fee" in c.lower()), None)
monthly_rev = round(df[monthly_col].sum(), 2) if monthly_col else 0

prediction_output_path = os.path.join(
    os.path.dirname(__file__), "..", "outputs", "predictions_with_recommendations.csv"
)
high_risk_count = None
if os.path.exists(prediction_output_path) and "Customer_ID" in df.columns:
    try:
        previous_predictions = pd.read_csv(prediction_output_path, usecols=["Customer_ID", "Risk_Level"])
        high_risk_count = int((previous_predictions["Risk_Level"] == "High").sum())
    except (ValueError, KeyError, pd.errors.EmptyDataError):
        high_risk_count = None


def recommendation_category(recommendation):
    text = str(recommendation).lower()
    if "discount" in text or "reward" in text or "loyalty" in text:
        return "Offers & Loyalty"
    if "support" in text or "buffering" in text or "satisfaction" in text:
        return "Service Recovery"
    if "premium" in text or "content" in text or "feature" in text:
        return "Content & Upgrade"
    return "Engagement"

# ── Navigation Tabs ───────────────────────────────────────────────────────────
tabs = st.tabs(["🏠 Executive Overview", "📊 Customer Analytics",
                "🔮 Churn Prediction", "💡 Recommendations", "📈 Business Insights"])

# ══════════════════════════════════════════════════════════════════════════════
# TAB 1 — Executive Overview
# ══════════════════════════════════════════════════════════════════════════════
with tabs[0]:
    st.title("📊 Customer Churn - Executive Overview")

    col1, col2, col3, col4, col5, col6 = st.columns(6)
    col1.metric("Total Customers",   f"{total:,}")
    col2.metric("Active Customers",  f"{active:,}")
    col3.metric("Churn Rate",        f"{churn_rate}%")
    col4.metric("Revenue",            f"₹{monthly_rev:,.0f}" if monthly_rev else "N/A")
    col5.metric("High Risk Customers", f"{high_risk_count:,}" if high_risk_count is not None else "Run model")
    col6.metric("Churned Customers", f"{churned:,}")

    st.markdown("---")
    c1, c2 = st.columns(2)

    # Churn vs Active donut
    with c1:
        fig = px.pie(
            names=["Active", "Churned"], values=[active, churned],
            title="Churn vs Active Customers",
            hole=0.58,
            color_discrete_sequence=["#16a085", "#e74c3c"]
        )
        fig.update_traces(textinfo="label+percent", textposition="inside")
        fig.update_layout(template="plotly_white", showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

    # Monthly churn trend using customer tenure months
    tenure_col = next((c for c in df.columns if "tenure" in c.lower()), None)
    with c2:
        if tenure_col:
            monthly_churn = df.groupby(tenure_col).agg(
                Churn_Rate=("Churn_Flag", "mean"),
                Customers=("Churn_Flag", "count")
            ).reset_index().sort_values(tenure_col)
            fig_trend = px.line(
                monthly_churn, x=tenure_col, y="Churn_Rate", markers=True,
                title="Monthly Churn Trend by Customer Tenure",
                hover_data=["Customers"], template="plotly_white"
            )
            fig_trend.update_traces(line=dict(color="#2878b5", width=3))
            fig_trend.update_yaxes(tickformat=".0%", title="Churn Rate")
            fig_trend.update_xaxes(title="Tenure (Months)")
            st.plotly_chart(fig_trend, use_container_width=True)
        else:
            st.info("No tenure-month column detected for the churn trend.")

    # Contract / plan churn bar and customer distribution column chart
    plan_col = next((c for c in df.columns if "plan" in c.lower() or
                     "contract" in c.lower()), None)
    if plan_col:
        plan_churn = df.groupby(plan_col)["Churn_Flag"].mean().reset_index()
        plan_churn.columns = [plan_col, "Churn Rate"]
        plan_churn["Churn Rate"] = plan_churn["Churn Rate"] * 100
        plan_churn = plan_churn.sort_values("Churn Rate", ascending=False)
        plan_counts = df[plan_col].value_counts().rename_axis(plan_col).reset_index(name="Customers")

        c3, c4 = st.columns(2)
        with c3:
            fig_contract = px.bar(
                plan_churn, x=plan_col, y="Churn Rate", text="Churn Rate",
                title="Churn by Contract Type", color="Churn Rate",
                color_continuous_scale="Reds", template="plotly_white"
            )
            fig_contract.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
            fig_contract.update_layout(showlegend=False, yaxis_title="Churn Rate (%)")
            st.plotly_chart(fig_contract, use_container_width=True)

        with c4:
            fig_distribution = px.bar(
                plan_counts, x=plan_col, y="Customers", text="Customers",
                title="Customer Distribution by Contract Type",
                color="Customers", color_continuous_scale="Blues",
                template="plotly_white"
            )
            fig_distribution.update_traces(textposition="outside")
            fig_distribution.update_layout(showlegend=False, yaxis_title="Customers")
            st.plotly_chart(fig_distribution, use_container_width=True)
    else:
        st.info("No subscription plan or contract column detected.")

    if high_risk_count is None:
        st.caption("High-risk count is populated after running the prediction model.")

# ══════════════════════════════════════════════════════════════════════════════
# TAB 2 — Customer Analytics
# ══════════════════════════════════════════════════════════════════════════════
with tabs[1]:
    st.title("👥 Customer Analytics")

    c1, c2 = st.columns(2)

    gender_col = next((c for c in df.columns if "gender" in c.lower()), None)
    age_col    = next((c for c in df.columns if "age" in c.lower()), None)
    state_col  = next((c for c in df.columns if "state" in c.lower()), None)

    with c1:
        if gender_col:
            gender_counts = df[gender_col].value_counts().reset_index()
            gender_counts.columns = ["Gender", "Count"]
            fig = px.pie(gender_counts, names="Gender", values="Count",
                         title="Gender Distribution",
                         color_discrete_sequence=px.colors.qualitative.Set2)
            st.plotly_chart(fig, use_container_width=True)

    with c2:
        if age_col:
            fig = px.histogram(df, x=age_col, color="Churn_Flag",
                               title="Age Distribution by Churn",
                               barmode="overlay",
                               color_discrete_map={0: "#2ecc71", 1: "#e74c3c"},
                               labels={"Churn_Flag": "Churned"})
            st.plotly_chart(fig, use_container_width=True)

    if plan_col:
        plan_counts = df[plan_col].value_counts().rename_axis("Subscription Plan").reset_index(name="Customers")
        fig = px.bar(plan_counts, x="Subscription Plan", y="Customers",
                     title="Customers by Subscription Plan", text="Customers",
                     color="Customers", color_continuous_scale="Blues",
                     template="plotly_white")
        fig.update_traces(textposition="outside")
        fig.update_layout(showlegend=False, yaxis_title="Customers")
        st.plotly_chart(fig, use_container_width=True)

    if state_col:
        state_counts = df[state_col].value_counts().rename_axis("State").reset_index(name="Customers")
        state_counts = state_counts.head(15).sort_values("Customers", ascending=False)
        fig = px.bar(
            state_counts,
            x="State",
            y="Customers",
            title="Top 15 States by Customer Count",
            text="Customers",
            color="Customers",
            color_continuous_scale="Greens",
            template="plotly_white"
        )
        fig.update_traces(textposition="outside")
        fig.update_layout(
            showlegend=False,
            xaxis_title="State",
            yaxis_title="Customers",
            xaxis_tickangle=-45
        )
        st.plotly_chart(fig, use_container_width=True)

        state_churn = df.groupby(state_col)["Churn_Flag"].sum().reset_index()
        state_churn.columns = ["State", "Churned"]
        state_churn = state_churn.sort_values("Churned", ascending=False).head(15)
        fig = px.bar(
            state_churn,
            x="State",
            y="Churned",
            title="Top 15 States by Churned Customers",
            text="Churned",
            color="Churned",
            color_continuous_scale="Oranges",
            template="plotly_white"
        )
        fig.update_traces(textposition="outside")
        fig.update_layout(
            showlegend=False,
            xaxis_title="State",
            yaxis_title="Churned Customers",
            xaxis_tickangle=-45
        )
        st.plotly_chart(fig, use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 3 — Churn Prediction (run inline with RandomForest)
# ══════════════════════════════════════════════════════════════════════════════
with tabs[2]:
    st.title("🔮 Churn Prediction")

    if st.button("Run Churn Prediction Model"):
        with st.spinner("Training Random Forest model..."):
            from sklearn.ensemble import RandomForestClassifier
            from sklearn.model_selection import train_test_split
            from sklearn.preprocessing import LabelEncoder
            from sklearn.metrics import classification_report

            df_ml = df.copy()

            # Drop leakage columns
            drop_cols = [c for c in df_ml.columns if c.lower() in [
                "customer_id", "customerid", "customer_name", "customername",
                "churn_type", "churntype", churn_col.lower(), "churn_flag"
            ]]
            df_ml.drop(columns=[c for c in drop_cols if c in df_ml.columns],
                       inplace=True, errors="ignore")

            # Encode categoricals
            for col in df_ml.select_dtypes(include="object").columns:
                df_ml[col] = LabelEncoder().fit_transform(df_ml[col].astype(str))

            df_ml.fillna(df_ml.median(numeric_only=True), inplace=True)

            X = df_ml
            y = df["Churn_Flag"]

            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.2, random_state=42, stratify=y)

            model = RandomForestClassifier(n_estimators=100, random_state=42)
            model.fit(X_train, y_train)

            y_pred  = model.predict(X_test)
            y_proba = model.predict_proba(X_test)[:, 1]

        st.success("Model trained successfully!")

        from sklearn.metrics import accuracy_score, f1_score, roc_auc_score
        col1, col2, col3 = st.columns(3)
        col1.metric("Accuracy",  f"{accuracy_score(y_test, y_pred)*100:.2f}%")
        col2.metric("F1-Score",  f"{f1_score(y_test, y_pred)*100:.2f}%")
        col3.metric("ROC-AUC",   f"{roc_auc_score(y_test, y_proba)*100:.2f}%")

        # Risk levels on full dataset
        proba_full = model.predict_proba(X)[:, 1]
        risk = pd.cut(proba_full, bins=[-0.001, 0.3, 0.6, 1.0],
                      labels=["Low", "Medium", "High"])
        prediction_results = df[[c for c in ["Customer_ID", "Customer_Name"] if c in df.columns]].copy()
        prediction_results["Churn_Probability"] = proba_full
        prediction_results["Risk_Level"] = risk.astype(str)
        st.session_state["prediction_results"] = prediction_results

        high_risk_count = int((risk == "High").sum())
        st.metric("High Risk Customers", f"{high_risk_count:,}")

        fig = px.histogram(x=risk, title="Customer Risk Level Distribution",
                           color=risk, color_discrete_map={
                               "Low": "#2ecc71", "Medium": "#f39c12", "High": "#e74c3c"})
        st.plotly_chart(fig, use_container_width=True)

        st.subheader("Prediction Probability")
        probability_view = prediction_results.sort_values("Churn_Probability", ascending=False).head(20)
        probability_view = probability_view.reset_index(drop=True)
        probability_view["Customer Rank"] = np.arange(1, len(probability_view) + 1)
        fig_probability = px.bar(
            probability_view,
            x="Customer Rank",
            y="Churn_Probability",
            hover_data=["Risk_Level"],
            title="Top 20 Customer Churn Probabilities",
            color="Churn_Probability",
            color_continuous_scale="Reds",
            labels={"Churn_Probability": "Churn Probability"}
        )
        fig_probability.update_yaxes(tickformat=".0%", range=[0, 1.05])
        fig_probability.update_layout(showlegend=False, xaxis_title="Customer Rank")
        st.plotly_chart(fig_probability, use_container_width=True)
        st.dataframe(prediction_results.sort_values("Churn_Probability", ascending=False).head(50),
                 use_container_width=True, hide_index=True)

        # Feature importance
        importance = pd.DataFrame({
            "Feature": X.columns,
            "Importance": model.feature_importances_
        }).sort_values("Importance", ascending=False).head(10)

        fig2 = px.scatter(importance, x="Importance", y="Feature",
                  size="Importance", color="Importance",
                  title="Top 10 Feature Importances",
                  color_continuous_scale="Viridis")
        st.plotly_chart(fig2, use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 4 — Recommendations
# ══════════════════════════════════════════════════════════════════════════════
with tabs[3]:
    st.title("💡 Retention Recommendations")

    st.markdown("""
    | Risk Level | Strategy |
    |---|---|
    | 🔴 High | 20% discount · Priority support · Free premium trial · Loyalty reward |
    | 🟡 Medium | 10% loyalty discount · Satisfaction survey · Early-loyalty bonus |
    | 🟢 Low | Thank-you message · New features notification |
    """)

    # Quick single-customer recommender
    st.subheader("Single Customer Lookup")
    cust_idx = st.number_input("Enter customer row index", min_value=0,
                               max_value=len(df)-1, value=0, step=1)
    row = df.iloc[int(cust_idx)]
    st.write(row)

    satisfaction_col = next((c for c in df.columns if "satisfaction" in c.lower()), None)
    complaint_col    = next((c for c in df.columns if "complaint" in c.lower() or
                              "ticket" in c.lower()), None)

    satisfaction = row[satisfaction_col] if satisfaction_col else 5
    complaints   = row[complaint_col]    if complaint_col    else 0
    is_churned   = row.get("Churn_Flag", 0)

    risk_manual = "High" if is_churned else ("Medium" if satisfaction <= 3 else "Low")

    recs = []
    if risk_manual == "High":
        recs = ["Offer a 20% discount on next 3 months",
                "Assign priority customer support",
                "Offer free 1-month Premium trial"]
    elif risk_manual == "Medium":
        recs = ["Offer a 10% loyalty discount", "Send satisfaction survey"]
    else:
        recs = ["Send thank-you loyalty message", "Inform about new features"]

    st.info(f"Risk Level: **{risk_manual}**")
    for r in recs:
        st.write(f"✅ {r}")

    st.subheader("Recommendation Categories")
    category_rows = []
    for risk_level, strategy_text in {
        "High": "Offer discount, priority support, premium trial, loyalty reward",
        "Medium": "Loyalty discount, satisfaction survey, early-loyalty bonus",
        "Low": "Thank-you message, new features notification",
    }.items():
        for strategy in strategy_text.split(", "):
            category_rows.append({"Risk Level": risk_level, "Recommendation": strategy,
                                 "Category": recommendation_category(strategy)})
    st.dataframe(pd.DataFrame(category_rows), use_container_width=True, hide_index=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 5 — Business Insights
# ══════════════════════════════════════════════════════════════════════════════
with tabs[4]:
    st.title("📈 Business Insights")

    payment_col = next((c for c in df.columns if "payment" in c.lower()), None)

    c1, c2 = st.columns(2)

    with c1:
        if payment_col:
            pay_churn = df.groupby(payment_col)["Churn_Flag"].mean().reset_index()
            pay_churn.columns = ["Payment Method", "Churn Rate"]
            pay_churn["Churn Rate"] = pay_churn["Churn Rate"] * 100
            pay_churn = pay_churn.sort_values("Churn Rate", ascending=False)
            fig = px.bar(
                pay_churn, x="Payment Method", y="Churn Rate", text="Churn Rate",
                title="Churn Rate by Payment Method", color="Churn Rate",
                color_continuous_scale="Reds", template="plotly_white"
            )
            fig.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
            fig.update_layout(showlegend=False, yaxis_title="Churn Rate (%)")
            st.plotly_chart(fig, use_container_width=True)

    with c2:
        if age_col:
            df["Age_Group"] = pd.cut(df[age_col],
                                     bins=[0, 25, 35, 45, 55, 100],
                                     labels=["<25", "25-35", "35-45", "45-55", "55+"])
            age_churn = df.groupby("Age_Group", observed=False).agg(
                Churn_Rate=("Churn_Flag", "mean"), Customers=("Churn_Flag", "count")
            ).reset_index()
            age_churn.columns = ["Age Group", "Churn Rate", "Customers"]
            age_churn["Churn Rate"] = age_churn["Churn Rate"] * 100
            age_churn = age_churn.sort_values("Churn Rate", ascending=False)
            fig2 = px.bar(
                age_churn, x="Age Group", y="Churn Rate", text="Churn Rate",
                title="Churn Rate by Age Group", color="Churn Rate",
                color_continuous_scale="Blues", template="plotly_white"
            )
            fig2.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
            fig2.update_layout(showlegend=False, yaxis_title="Churn Rate (%)")
            st.plotly_chart(fig2, use_container_width=True)

    st.subheader("Churn Drivers by Plan and State")
    c1, c2 = st.columns(2)

    if plan_col:
        plan_insights = df.groupby(plan_col).agg(
            Total_Customers=("Churn_Flag", "count"),
            Churned=("Churn_Flag", "sum")
        ).reset_index()
        plan_insights["Churn Rate %"] = (
            plan_insights["Churned"] / plan_insights["Total_Customers"] * 100
        ).round(2)
        plan_insights = plan_insights.sort_values("Churn Rate %", ascending=False)
        with c1:
            fig_plan = px.bar(
                plan_insights,
                x=plan_col,
                y="Churn Rate %",
                text="Churn Rate %",
                hover_data=["Total_Customers", "Churned"],
                title="Churn Rate by Subscription Plan",
                labels={plan_col: "Subscription Plan", "Churn Rate %": "Churn Rate (%)"},
                color="Churn Rate %",
                color_continuous_scale="Reds",
                template="plotly_white"
            )
            fig_plan.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
            fig_plan.update_layout(showlegend=False, yaxis_title="Churn Rate (%)")
            st.plotly_chart(fig_plan, use_container_width=True)

    if state_col:
        state_chart = df.groupby(state_col).agg(
            Total_Customers=("Churn_Flag", "count"),
            Churned=("Churn_Flag", "sum")
        ).reset_index()
        state_chart["Churn Rate %"] = (
            state_chart["Churned"] / state_chart["Total_Customers"] * 100
        ).round(2)
        state_chart = state_chart.sort_values("Churn Rate %", ascending=False).head(15)
        with c2:
            fig_state = px.bar(
                state_chart,
                x=state_col,
                y="Churn Rate %",
                text="Churn Rate %",
                hover_data=["Total_Customers", "Churned"],
                title="Top 15 States by Churn Rate",
                labels={state_col: "State", "Churn Rate %": "Churn Rate (%)"},
                color="Churn Rate %",
                color_continuous_scale="Oranges",
                template="plotly_white"
            )
            fig_state.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
            fig_state.update_layout(showlegend=False, yaxis_title="Churn Rate (%)",
                                    xaxis_tickangle=-45)
            st.plotly_chart(fig_state, use_container_width=True)

    if plan_col:
        plan_rev = df.groupby(plan_col).agg(
            Total_Customers=("Churn_Flag", "count"),
            Churned=("Churn_Flag", "sum")
        ).reset_index()
        plan_rev["Churn Rate %"] = (plan_rev["Churned"] / plan_rev["Total_Customers"] * 100).round(2)
        st.subheader("Churn by Subscription Plan")
        st.dataframe(plan_rev, use_container_width=True, hide_index=True)

    if state_col:
        state_insights = df.groupby(state_col).agg(
            Total_Customers=("Churn_Flag", "count"),
            Churned=("Churn_Flag", "sum")
        ).reset_index()
        state_insights["Churn Rate %"] = (
            state_insights["Churned"] / state_insights["Total_Customers"] * 100
        ).round(2)
        st.subheader("Churn by State")
        st.dataframe(state_insights.sort_values("Churn Rate %", ascending=False),
                     use_container_width=True, hide_index=True)

