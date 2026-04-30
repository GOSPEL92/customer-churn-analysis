import pandas as pd
from snowflake.connector import connect
from snowflake.connector.pandas_tools import write_pandas

# Step 1: Connect to Snowflake
conn = connect(
    user=" "your_username_here",
    password="your_password_here",
    account="your account here",
    warehouse="your warehouse name here",
    database="your database name here",
    schema="PUBLIC"
)

# Step 2: Load Kaggle churn dataset
df = pd.read_csv(r"C:\Users\HP\Downloads\Customer Churn data\customer_churn_business_dataset.csv")

# Step 3: Apply feature engineering
df = transform_features(df)

# Step 4: Model scoring using your trained pipeline
X_full = df.drop(columns=['churn'])
y_pred_proba = pipeline.predict_proba(X_full)[:,1]

# Step 5: Risk banding
risk_band = pd.Series(y_pred_proba).apply(
    lambda p: 'Low' if p < 0.3 else 'Medium' if p < 0.6 else 'High'
)

# Step 6: Build summary DataFrame
summary_df = pd.DataFrame({
    'CUSTOMER_ID': df['customer_id'],
    'CHURN_PROBABILITY': y_pred_proba,
    'RISK_BAND': risk_band
})

# Step 7: Load into Snowflake
summary_df.columns = [c.upper() for c in summary_df.columns]
success, nchunks, nrows, _ = write_pandas(conn, summary_df, "CUSTOMER_CHURN_SUMMARY")
print(f"Automation run complete: {nrows} rows loaded.")

