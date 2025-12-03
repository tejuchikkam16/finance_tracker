import os
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

st.set_page_config(page_title="Personal Finance Tracker", layout="wide")
st.title("💰 Personal Finance Tracker")

# CSV path
file_path = "transactions.csv"

# -----------------------------
# Step 1 — CSV auto-create if missing
# -----------------------------
expected_cols = ["Date","Category","Amount","Payment Method","Description"]

if not os.path.exists(file_path):
    df = pd.DataFrame([
        {"Date":"2025-12-01","Category":"Food","Amount":500,"Payment Method":"UPI","Description":"Lunch"},
        {"Date":"2025-12-02","Category":"Transport","Amount":300,"Payment Method":"Cash","Description":"Cab"}
    ])
    df.to_csv(file_path, index=False)
else:
    df = pd.read_csv(file_path)

# Ensure all expected columns exist & correct order
for col in expected_cols:
    if col not in df.columns:
        df[col] = ""
df = df[expected_cols]

# -----------------------------
# Step 2 — Add New Expense Form
# -----------------------------
st.subheader("Add New Expense")
with st.form("expense_form"):
    date = st.date_input("Date")
    category = st.selectbox("Category", ["Food","Transport","Shopping","Health","Bills","Entertainment","Others"])
    amount = st.number_input("Amount", min_value=0.0, format="%.2f")
    payment_method = st.selectbox("Payment Method", ["UPI","Cash","Card","Netbanking"])
    description = st.text_input("Description")

    description = description if description else ""

    submitted = st.form_submit_button("Add Expense")
    if submitted:
        new_row = {
            "Date": date.strftime("%Y-%m-%d"),
            "Category": category,
            "Amount": amount,
            "Payment Method": payment_method,
            "Description": description
        }
        # Append safely
        if not os.path.exists(file_path):
            pd.DataFrame([new_row])[expected_cols].to_csv(file_path, index=False)
        else:
            pd.DataFrame([new_row])[expected_cols].to_csv(file_path, mode='a', header=False, index=False)

        # Reload CSV
        df = pd.read_csv(file_path)
        for col in expected_cols:
            if col not in df.columns:
                df[col] = ""
        df = df[expected_cols]
        st.success("✅ Expense Added!")

# -----------------------------
# Step 3 — Display All Expenses
# -----------------------------
st.subheader("All Expenses")
st.dataframe(df)

# -----------------------------
# Step 4 — Charts (Safe)
# -----------------------------
if not df.empty:
    df["Amount"] = pd.to_numeric(df["Amount"], errors="coerce").fillna(0)

    pie_data = df.groupby("Category")["Amount"].sum()
    if pie_data.sum() > 0:
        fig1, ax1 = plt.subplots()
        ax1.pie(pie_data, labels=pie_data.index, autopct='%1.1f%%')
        st.subheader("Expenses by Category (Pie Chart)")
        st.pyplot(fig1)
    else:
        st.info("No expense amounts to display Pie Chart.")

    bar_data = df.groupby("Category")["Amount"].sum()
    if bar_data.sum() > 0:
        fig2, ax2 = plt.subplots()
        ax2.bar(bar_data.index, bar_data.values)
        st.subheader("Expenses by Category (Bar Chart)")
        st.pyplot(fig2)
    else:
        st.info("No expense amounts to display Bar Chart.")
else:
    st.info("No expense data available to display charts.")

# -----------------------------
# Step 5 — Budget Alerts
# -----------------------------
budget_limit = 10000
total_expense = df["Amount"].sum() if not df.empty else 0
st.subheader("Budget Alerts")
if total_expense > budget_limit:
    st.error(f"⚠️ Budget exceeded! Total: ₹{total_expense}")
else:
    st.success(f"✅ Within budget. Total: ₹{total_expense}")
