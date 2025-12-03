import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

st.title("💰 Personal Finance Tracker")

# --- Load CSV ---
df = pd.read_csv("transactions.csv")

# --- Transactions Table ---
st.subheader("📋 Transactions Data")
st.dataframe(df)

# --- Total Expense ---
total = df['amount'].sum()
st.subheader(f"Total Expense: ₹{total}")

# --- Pie Chart: Expense by Category ---
st.subheader("📊 Expense by Category")
expense_totals = df.groupby("category")["amount"].sum()

fig, ax = plt.subplots()
ax.pie(expense_totals, labels=expense_totals.index, autopct="%1.1f%%", startangle=90)
ax.axis("equal")
st.pyplot(fig)

# --- Bar Chart: Category-wise Expense ---
st.subheader("📈 Expense by Category - Bar Chart")
fig2, ax2 = plt.subplots()
expense_totals.plot(kind='bar', ax=ax2, color='skyblue')
ax2.set_ylabel("Amount")
ax2.set_xlabel("Category")
ax2.set_title("Category-wise Expense")
st.pyplot(fig2)

# --- Budget Alert Setup ---
# Define budget limits per category
budget_limits = {
    "Food": 500,
    "Transport": 200,
    "Shopping": 1000,
    "Bills": 800,
    "Others": 300
}

st.subheader("⚠️ Budget Alerts")
for category, limit in budget_limits.items():
    spent = df[df['category'] == category]['amount'].sum()
    if spent > limit:
        st.warning(f"💡 Alert: You spent ₹{spent} in {category}, which exceeds the budget limit of ₹{limit}!")

# --- Add New Transaction Form ---
st.subheader("➕ Add New Transaction")

name = st.text_input("Description")
amount = st.number_input("Amount", min_value=0.0)
category = st.selectbox("Category", ["Food", "Transport", "Shopping", "Bills", "Others"])

if st.button("Add Transaction"):
    new_row = {"category": category, "amount": amount, "name": name}
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    df.to_csv("transactions.csv", index=False)
    st.success("✅ Transaction Added!")
