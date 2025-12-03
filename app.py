import os
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

st.title("Personal Finance Tracker")

# CSV path — relative path for deploy & local
file_path = "transactions.csv"

# Step 1 — CSV auto-create if missing
if not os.path.exists(file_path):
    df = pd.DataFrame(columns=["Date","Category","Amount","Description","Payment Method","Notes"])
    # Optional first-time dummy data
    df = pd.DataFrame([
        {"Date":"2025-12-01","Category":"Food","Amount":500,"Description":"Lunch","Payment Method":"UPI","Notes":""},
        {"Date":"2025-12-02","Category":"Transport","Amount":300,"Description":"Cab","Payment Method":"Cash","Notes":""},
    ])
    df.to_csv(file_path, index=False)
else:
    df = pd.read_csv(file_path)

# Step 2 — Add New Expense
st.subheader("Add New Expense")
with st.form("expense_form"):
    date = st.date_input("Date")
    category = st.selectbox("Category", ["Food","Transport","Shopping","Health","Bills","Entertainment","Others"])
    amount = st.number_input("Amount", min_value=0.0, format="%.2f")
    description = st.text_input("Description")
    payment_method = st.selectbox("Payment Method", ["UPI","Cash","Card","Netbanking"])
    notes = st.text_input("Notes")
    submitted = st.form_submit_button("Add Expense")
    
    if submitted:
        new_row = {
            "Date": date.strftime("%Y-%m-%d"),
            "Category": category,
            "Amount": amount,
            "Description": description,
            "Payment Method": payment_method,
            "Notes": notes
        }
        # Append to CSV directly
        pd.DataFrame([new_row]).to_csv(file_path, mode='a', header=not os.path.exists(file_path), index=False)
        # Reload updated CSV to reflect new row
        df = pd.read_csv(file_path)
        st.success("Expense Added!")

# Step 3 — Display All Expenses
st.subheader("All Expenses")
st.dataframe(df)

# Step 4 — Charts
if not df.empty:
    pie_data = df.groupby("Category")["Amount"].sum()
    fig1, ax1 = plt.subplots()
    ax1.pie(pie_data, labels=pie_data.index, autopct='%1.1f%%')
    st.subheader("Expenses by Category (Pie Chart)")
    st.pyplot(fig1)

    bar_data = df.groupby("Category")["Amount"].sum()
    fig2, ax2 = plt.subplots()
    ax2.bar(bar_data.index, bar_data.values)
    st.subheader("Expenses by Category (Bar Chart)")
    st.pyplot(fig2)
else:
    st.info("No expense data available to display charts.")

# Step 5 — Budget Alerts
budget_limit = 10000
total_expense = df["Amount"].sum() if not df.empty else 0
st.subheader("Budget Alerts")
if total_expense > budget_limit:
    st.error(f"Budget exceeded! Total: ₹{total_expense}")
else:
    st.success(f"Within budget. Total: ₹{total_expense}")
