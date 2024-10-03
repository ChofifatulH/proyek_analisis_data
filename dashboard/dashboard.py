import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def load_data():
    df = pd.concat([
        pd.read_csv("air_quality_dataset/PRSA_Data_Aotizhongxin_20130301-20170228.csv"),
        pd.read_csv("air_quality_dataset/PRSA_Data_Changping_20130301-20170228.csv"),
        pd.read_csv("air_quality_dataset/PRSA_Data_Dingling_20130301-20170228.csv"),
        pd.read_csv("air_quality_dataset/PRSA_Data_Dongsi_20130301-20170228.csv"),
        pd.read_csv("air_quality_dataset/PRSA_Data_Guanyuan_20130301-20170228.csv"),
        pd.read_csv("air_quality_dataset/PRSA_Data_Gucheng_20130301-20170228.csv"),
        pd.read_csv("air_quality_dataset/PRSA_Data_Huairou_20130301-20170228.csv"),
        pd.read_csv("air_quality_dataset/PRSA_Data_Nongzhanguan_20130301-20170228.csv"),
        pd.read_csv("air_quality_dataset/PRSA_Data_Shunyi_20130301-20170228.csv"),
        pd.read_csv("air_quality_dataset/PRSA_Data_Tiantan_20130301-20170228.csv"),
        pd.read_csv("air_quality_dataset/PRSA_Data_Wanliu_20130301-20170228.csv"),
        pd.read_csv("air_quality_dataset/PRSA_Data_Wanshouxigong_20130301-20170228.csv")
    ])
    return df

def analyze_august(df):
    df['month'] = pd.to_datetime(df[['year', 'month', 'day']]).dt.month
    df_august = df[df['month'] == 8]

    pollutants = ['PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3']
    august_pollution = df_august.groupby('station')[pollutants].mean().reset_index()

    return august_pollution

def analyze_wind_pollution(df):
    correlation_wind_pm25 = df.groupby('station')['WSPM'].corr(df['PM2.5'])
    correlation_wind_pm10 = df.groupby('station')['WSPM'].corr(df['PM10'])

    return correlation_wind_pm25, correlation_wind_pm10

st.title("Dashboard Polusi Udara dan Kecepatan Angin")

data = load_data()

st.subheader("1. Bagaimana perbandingan polusi udara (PM2.5, PM10, SO2, NO2, CO, O3) di antara 12 stasiun selama bulan Agustus?")
august_pollution = analyze_august(data)
st.write(august_pollution)

st.subheader("Visualisasi Rata-Rata Polusi Udara")
fig, ax = plt.subplots(figsize=(10, 6))
august_pollution.set_index('station').plot(kind='bar', ax=ax)
plt.title("Rata-Rata Polusi Udara di Setiap Stasiun (Agustus)")
plt.ylabel("Kadar Polusi")
plt.xlabel("Stasiun")
st.pyplot(fig)

st.subheader("2. Bagaimana kecepatan angin (WSPM) mempengaruhi tingkat polusi udara (PM2.5, PM10) di setiap stasiun?")
correlation_wind_pm25, correlation_wind_pm10 = analyze_wind_pollution(data)
st.write("Korelasi antara kecepatan angin (WSPM) dan PM2.5 di setiap stasiun:")
st.write(correlation_wind_pm25)
st.write("Korelasi antara kecepatan angin (WSPM) dan PM10 di setiap stasiun:")
st.write(correlation_wind_pm10)

# st.subheader("Visualisasi Hubungan WSPM dan PM2.5 / PM10")
# fig, axes = plt.subplots(1, 2, figsize=(12, 6))
# sns.scatterplot(data=data, x='WSPM', y='PM2.5', ax=axes[0])
# axes[0].set_title('Hubungan WSPM dan PM2.5')
# sns.scatterplot(data=data, x='WSPM', y='PM10', ax=axes[1])
# axes[1].set_title('Hubungan WSPM dan PM10')
# st.pyplot(fig)
