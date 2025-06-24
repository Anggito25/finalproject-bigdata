import streamlit as st
import pandas as pd
import altair as alt
import matplotlib.pyplot as plt
from wordcloud import WordCloud

#load dataset
df = pd.read_csv('Top 5 cell phone brands 2022 on Amazon.csv')

#judul
st.title("Analisis Top 5 HP di Amazon (2022)")

#sidebar filter
brands = df['Brand'].unique()
selected_brands = st.sidebar.multiselect(
    "Pilih Brand Handphone:",
    options=brands,
    default=brands
)

#filter data sesuai brand
df_filtered = df[df['Brand'].isin(selected_brands)]

#konversi kolom rating dan sale_price jadi numeric
df_filtered['rating'] = pd.to_numeric(df_filtered['rating'], errors='coerce')
df_filtered['sale_price'] = pd.to_numeric(df_filtered['sale_price'], errors='coerce')
df_filtered['list_price'] = pd.to_numeric(df_filtered['list_price'], errors='coerce')

#hapus data yang tidak valid
df_filtered['times_evaluated'] = pd.to_numeric(df_filtered['times_evaluated'], errors='coerce')

#perhitungan harga rata-rata dan rata-rata rating
avg_list_price = df_filtered['list_price'].mean()
avg_sale_price = df_filtered['sale_price'].mean()
avg_rating = df_filtered['rating'].mean()
total_review = df_filtered['times_evaluated'].sum()

#kolom informasi umum
col1, col2, col3, col4 = st.columns(4)
col1.metric("Rata-rata Harga", f"${avg_list_price:,.2f}")
col2.metric("Rata-rata Harga Diskon", f"${avg_sale_price:,.2f}")
col3.metric("Rata-rata Rating", f"{avg_rating:.2f}")
col4.metric("Total Ulasan", f"{total_review:,}")

#tabel data produk
st.subheader("Data Produk")
st.dataframe(df_filtered[['Brand', 'title', 'list_price', 'sale_price', 'rating']])

#bar chart: total produk per brand
st.subheader("Jumlah Produk per Brand")
brand_counts_all = df['Brand'].value_counts()
st.bar_chart(brand_counts_all)

#bar chart: rata-rata rating per brand
avg_rating_per_brand = df_filtered.groupby('Brand')['rating'].mean()
st.subheader("Rata-rata Rating per Brand (Line Chart)")

#buat brand jadi kolom
avg_rating_df = avg_rating_per_brand.reset_index()

line_chart = alt.Chart(avg_rating_df).mark_line(point=True).encode(
    x=alt.X('Brand', axis=alt.Axis(labelAngle=0)),  # sort=None biar urutan asli
    y=alt.Y('rating', title='Rata-rata Rating'),
    tooltip=['Brand', 'rating']
).properties(
    width=600,
    height=400
)
st.altair_chart(line_chart, use_container_width=True)

#scatter plot: perbandingan harga normal dan diskon menggunakan
st.subheader("Perbandingan Harga Normal dan Harga Diskon")
chart = alt.Chart(df_filtered).mark_circle(size=60).encode(
    x=alt.X('list_price', title='Harga Normal'),
    y=alt.Y('sale_price', title='Harga Diskon'),
    color=alt.Color('Brand', legend=alt.Legend(title="Brand")),
    tooltip=['Brand', 'title', 'list_price', 'sale_price']
).properties(
    width=700,
    height=400
).interactive()
st.altair_chart(chart)

#persiapan wordcloud: gabungkan semua judul jadi satu string
text_titles = ' '.join(df_filtered['title'].dropna().astype(str))

#wordcloud: kata yang sering muncul
wordcloud = WordCloud(
    width=800,
    height=400,
    background_color='white',
    colormap='viridis',
    max_words=100
).generate(text_titles)
st.subheader("WordCloud dari Judul Produk")
fig, ax = plt.subplots(figsize=(10, 5))
ax.imshow(wordcloud, interpolation='bilinear')
ax.axis("off")
st.pyplot(fig)
