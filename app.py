import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

# -------------------------
# Initialize CSV
# -------------------------
CSV_FILE = "expenses.csv"

if not os.path.exists(CSV_FILE):
    df = pd.DataFrame(columns=["Date", "Category", "Amount", "Payment Method", "Description"])
    df.to_csv(CSV_FILE, index=False)

df = pd.read_csv(CSV_FILE)

st.title("💰 Personal Finance Tracker")

# -------------------------
# Add New Expense Form
# -------------------------
st.header("Add New Expense")

date = st.date_input("Date")
category = st.selectbox("Category", ["Food", "Transport", "Shopping", "Health", "Bills", "Entertainment", "Others"])
amount = st.number_input("Amount", min_value=0.0, format="%.2f")
payment = st.selectbox("Payment Method", ["Cash", "Card", "UPI"])
description = st.text_input("Description (Optional)", "")

if st.button("Add Expense"):
    new_row = {
        "Date": str(date),
        "Category": category,
        "Amount": amount,
        "Payment Method": payment,
        "Description": description
    }
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    df.to_csv(CSV_FILE, index=False)
    st.success("Expense added successfully!")

# Reload updated data
df = pd.read_csv(CSV_FILE)

# -------------------------
# Show All Expenses
# -------------------------
st.header("All Expenses")

if not df.empty:
    df_display = df.copy()
    df_display.index = df_display.index + 1     # S.No
    
    df_display = df_display[["Date", "Category", "Amount", "Payment Method", "Description"]]
    
    st.dataframe(df_display)
else:
    st.write("No expenses added yet.")

# -------------------------
# Charts Section
# -------------------------
if not df.empty:

    st.header("Total Expenses")
    st.subheader(f"₹ {df['Amount'].sum():,.2f}")

    # ---------- Pie Chart ----------
    st.subheader("Expenses by Category (Pie Chart)")
    pie_data = df.groupby("Category")["Amount"].sum()

    fig1, ax1 = plt.subplots()
    ax1.pie(pie_data, labels=pie_data.index, autopct="%1.1f%%")
    ax1.axis("equal")
    st.pyplot(fig1)

    # ---------- Bar Chart ----------
    st.subheader("Expenses by Category (Bar Chart)")
    fig2, ax2 = plt.subplots()
    ax2.bar(pie_data.index, pie_data.values)
    plt.xticks(rotation=45)
    st.pyplot(fig2)
