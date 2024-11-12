# Melakukan import library yang dibutuhkan
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import datetime
from babel.numbers import format_currency
sns.set(style='dark')

# Membuat tampilan Header Dashboard
st.title('Bike Rental Sharing Dashboard :sparkles:')

# Melakukan load berkas main_data.csv 
main_df = pd.read_csv("main_data.csv")

# Mengubah dteday menjadi tipe data Datetime
datetime_columns = ["dteday"]
main_df.sort_values(by="dteday", inplace=True)
main_df.reset_index(inplace=True)
 
for column in datetime_columns:
    main_df[column] = pd.to_datetime(main_df[column])

# membuat helper function untuk rentals
def create_daily_rentals_df(df):
    daily_rentals_df = df.resample(rule='D', on='dteday').agg({
        "instant": "nunique",
        "cnt": "sum"
    })
    daily_rentals_df = daily_rentals_df.reset_index()
    daily_rentals_df.rename(columns={
        "instant": "rental_count",
        "cnt": "count"
    }, inplace=True)
    
    return daily_rentals_df

# Membuat helper function rentals berdasarkan musim
def create_byseason_df(df):
    byseason_df = df.groupby(by="season").instant.nunique().reset_index()
    byseason_df.rename(columns={
        "instant": "customer_count"
    }, inplace=True)
    
    return byseason_df

# Membuat helper function rentals berdasarkan cuaca
def create_byweather_df(df):
    byweather_df = df.groupby(by="weathersit").instant.nunique().reset_index()
    byweather_df.rename(columns={
        "instant": "customer_count"
    }, inplace=True)
    
    return byweather_df

# Menghubungkan helper function ke berkas main_df
daily_rentals_df = create_daily_rentals_df(main_df)
byseason_df = create_byseason_df(main_df)
byweather_df = create_byweather_df(main_df)

# Membuat komponen filter
min_date = main_df["dteday"].min()
max_date = main_df["dteday"].max()
 
with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("C:/Users/USER/proyek_akhir_analisis_data/bicycle_14190753.png", caption="Bike Sharing Rental")
    
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

### VISUALISASI DATA ###
  
# Membuat kategori label untuk Cuaca dan Musim
weather_category = {
    1: 'Cerah',
    2: 'Berkabut',
    3: 'Hujan Ringan',
    4: 'Hujan Lebat'
}
season_category = {
    1: 'Musim Semi',
    2: 'Musim Panas',
    3: 'Musim Gugur',
    4: 'Musim Dingin'
}

# Terapkan label ke kolom 'weathersit' dan 'season'
main_df['weathersit'] = main_df['weathersit'].map(weather_category)
main_df['season'] = main_df['season'].map(season_category)

# Membuat filter interaktif untuk Kondisi Cuaca
weather_filter = st.sidebar.multiselect(
    "Kondisi Cuaca",
    options=main_df['weathersit'].unique(),
    default=main_df['weathersit'].unique()
)
# Membuat filter interaktif untuk kondisi musim
season_filter = st.sidebar.multiselect(
    "Kondisi Musim",
    options=main_df['season'].unique(),
    default=main_df['season'].unique()
)

# Terapkan filter cuaca dan musim pada data
filtered_df = main_df[main_df['weathersit'].isin(weather_filter)]
filtered_df = main_df[main_df['season'].isin(season_filter)]

# Membuat Tab untuk masing-masing Visualisasi Data
tab1, tab2, tab3 = st.tabs(["Distribusi Penyewaan Sepeda", "Perbandingan Penyewaan Sepeda", "Rekap Data"])
 
with tab1:
    st.header("Jumlah Penyewaan Sepeda per Hari")
    st.line_chart(filtered_df.set_index('dteday')['cnt'])
 
with tab2:
# Membuat Bar chart Rerata Penyewaan sepeda berdasarkan cuaca
    st.header("Rerata Penyewaan Sepeda Berdasarkan Cuaca")
    weather_count = filtered_df.groupby('weathersit')['cnt'].mean()
    st.bar_chart(weather_count)
    st.header("Rerata Penyewaan Sepeda Berdasarkan Musim")
    season_count = filtered_df.groupby('season')['cnt'].mean()
    st.bar_chart(season_count)
    
with tab3:
    st.write(f"Rekap Data Penyewaan Sepeda dari {start_date} hingga {end_date}")
    st.write(filtered_df)
