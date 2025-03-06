import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set(style='dark')


def season_total_df(day_df):
    season_sum_df = day_df.groupby(by="season").count_total.sum().sort_values(ascending=False).reset_index()
    
    return season_sum_df

def weekday_total_df(day_df):
    weekday_sum_df = day_df.groupby(by="weekday").count_total.sum().sort_values(ascending=False).reset_index()
    
    return weekday_sum_df

def hour_total_df(hour_df):
    hour_sum_df = hour_df.groupby(by="hour").count_total.sum().sort_values(ascending=False).reset_index()
    
    return hour_sum_df

def month_total_df(day_df):
    yearmonth_sum_df = day_df.sort_values(["year", "month"]).groupby(["year", "month"]).count_total.sum().reset_index()
    
    return yearmonth_sum_df

day_df = pd.read_csv("dashboard/day_cleaned.csv")
hour_df = pd.read_csv("dashboard/hour_cleaned.csv")

day_df.sort_values(by="date", inplace=True)
day_df.reset_index(inplace=True)
day_df["date"] = pd.to_datetime(day_df["date"])

hour_df.sort_values(by="date", inplace=True)
hour_df.reset_index(inplace=True)
hour_df["date"] = pd.to_datetime(hour_df["date"])

min_date = day_df["date"].min()
max_date = day_df["date"].max()

min_date = hour_df["date"].min()
max_date = hour_df["date"].max()
 
with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("https://github.com/dicodingacademy/assets/raw/main/logo.png")
    
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df_day = day_df[(day_df["date"] >= str(start_date)) & 
                (day_df["date"] <= str(end_date))]

main_df_hour = hour_df[(hour_df["date"] >= str(start_date)) & 
                (hour_df["date"] <= str(end_date))]

season_df = season_total_df(main_df_day)
weekday_df = weekday_total_df(main_df_day)
month_df = month_total_df(main_df_day)
hour_sum_df = hour_total_df(main_df_hour)

st.header('Dashboard Data Penyewaan Sepeda Tahun 2011 dan 2012')

st.subheader('Performa penyewaan sepeda setiap bulannya (2011 dan 2012)')
 
col1, col2, col3 = st.columns(3)
 
with col1:
    total_count = day_df.count_total.sum()
    st.metric("Total penyewa", value=total_count)

with col2:
    total_casual = day_df.casual.sum()
    st.metric("Total penyewa casual", value=total_casual)

with col3:
    total_regis = day_df.registered.sum()
    st.metric("Total penyewa registered", value=total_regis)
 
 
fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    day_df["month"],
    day_df["count_total"],
    marker='o', 
    linewidth=2,
    color="#90CAF9"
)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)
 
st.pyplot(fig)

st.subheader("Customer Demographics")
 
col1, col2 = st.columns(2)
 
with col1:
    fig, ax = plt.subplots(figsize=(20, 10))
    colors = ["#99aab5", "#99aab5", "#7289da", "#99aab5"]
    sns.barplot(
        y="count_total", 
        x="season",
        data=season_df.sort_values(by="season", ascending=False),
        palette=colors,
        ax=ax
    )
    ax.set_title("Number of Customer by season", loc="center", fontsize=50)
    ax.set_ylabel(None)
    ax.set_xlabel(None)
    ax.tick_params(axis='x', labelsize=35)
    ax.tick_params(axis='y', labelsize=30)
    st.pyplot(fig)
 
with col2:
    fig, ax = plt.subplots(figsize=(20, 10))
    
    colors = ["#99aab5", "#99aab5", "#99aab5", "#99aab5", "#7289da", "#7289da", "#99aab5"]
 
    sns.barplot(
        y="count_total", 
        x="weekday",
        data=weekday_df.sort_values(by="weekday", ascending=False),
        palette=colors,
        ax=ax
    )
    ax.set_title("Number of Customer by weekday", loc="center", fontsize=50)
    ax.set_ylabel(None)
    ax.set_xlabel(None)
    ax.tick_params(axis='x', labelsize=35)
    ax.tick_params(axis='y', labelsize=30)
    st.pyplot(fig)
 
fig, ax = plt.subplots(figsize=(20, 10))
colors= ["#99aab5", "#99aab5", "#99aab5", "#99aab5", "#99aab5", "#99aab5", "#99aab5", "#99aab5", "#99aab5", "#99aab5", "#99aab5", "#99aab5", "#99aab5", "#99aab5", "#99aab5", "#99aab5","#99aab5" , "#7289da", "#99aab5", "#99aab5", "#99aab5", "#99aab5", "#99aab5"]
sns.barplot(
    x="count_total", 
    y="hour",
    data=hour_sum_df.sort_values(by="hour", ascending=False),
    palette=colors,
    orient="h",
    ax=ax
)
ax.set_title("Number of Customer by hour", loc="center", fontsize=30)
ax.set_ylabel(None)
ax.set_xlabel(None)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)
st.pyplot(fig)
