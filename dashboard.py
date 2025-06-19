import streamlit as st
import pandas as pd
import plotly.express as px

# Load data
df = pd.read_csv("cleaned_amazon_data.csv")
top_revenue = pd.read_csv("top_revenue_products.csv")
top_units = pd.read_csv("top_units_products.csv")
daily_df = pd.read_csv("daily_trends.csv", parse_dates=["Date"])
weekly_df = pd.read_csv("weekly_summary.csv", parse_dates=["Week"])

# Metrics
total_revenue = df['Ordered Product Sales'].sum()
total_orders = df['Total Order Items'].sum()
total_units = df['Units Ordered'].sum()
average_order_value = total_revenue / total_orders if total_orders else 0

# Page layout
st.set_page_config(page_title="GO Sleeves Amazon Dashboard", layout="wide")
st.title("📊 GO Sleeves Amazon Sales Dashboard")

# Metric Cards
col1, col2, col3, col4 = st.columns(4)
col1.metric("💵 Total Revenue", f"${total_revenue:,.2f}")
col2.metric("📦 Total Orders", f"{int(total_orders):,}")
col3.metric("📊 Units Sold", f"{int(total_units):,}")
col4.metric("💰 Avg. Order Value", f"${average_order_value:,.2f}")

st.markdown("---")

# Daily Trend Chart
st.subheader("📅 Daily Revenue Trend")
daily_chart = px.line(daily_df.groupby("Date").agg({"Daily Revenue": "sum"}).reset_index(),
                      x="Date", y="Daily Revenue",
                      labels={"Daily Revenue": "Revenue", "Date": "Date"},
                      title="Daily Revenue Over Time")
st.plotly_chart(daily_chart, use_container_width=True)

# Weekly Revenue Chart
st.subheader("📈 Weekly Revenue Summary")
weekly_chart = px.bar(weekly_df, x="Week", y="Weekly Revenue",
                      labels={"Weekly Revenue": "Revenue", "Week": "Week"},
                      text_auto=True, color="Weekly Revenue", color_continuous_scale="Blues")
st.plotly_chart(weekly_chart, use_container_width=True)

# Top Products by Revenue
st.subheader("🔥 Top Performing Products by Revenue")
fig_rev = px.bar(top_revenue, x="Ordered Product Sales", y="Title", orientation='h',
                 labels={"Ordered Product Sales": "Revenue", "Title": "Product"},
                 text="Ordered Product Sales", color="Ordered Product Sales",
                 color_continuous_scale="Blues")
st.plotly_chart(fig_rev, use_container_width=True)

# Top Products by Units Sold
st.subheader("📦 Top Products by Units Sold")
fig_units = px.bar(top_units, x="Units Ordered", y="Title", orientation='h',
                   labels={"Units Ordered": "Units", "Title": "Product"},
                   text="Units Ordered", color="Units Ordered",
                   color_continuous_scale="Greens")
st.plotly_chart(fig_units, use_container_width=True)

# Full Table
st.subheader("🧾 Full Product Breakdown")
st.dataframe(df[['(Child) ASIN', 'Title', 'Ordered Product Sales', 'Units Ordered',
                 'Total Order Items', 'Sessions - Total', 'Unit Session Percentage']]
             .sort_values(by='Ordered Product Sales', ascending=False),
             use_container_width=True)