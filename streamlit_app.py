import streamlit as st
import pandas as pd
import plotly.express as px
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# Page configuration
st.set_page_config(page_title="🎬 Movie Explorer Dashboard", layout="wide")

# Load the cleaned movie data
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/melnikacg/DV_test_del/main/movies_full_cleaned.csv"
    df = pd.read_csv(url)

    # Explode genres into individual rows for filtering
    df['genres'] = df['genres'].fillna('')
    df['genre_list'] = df['genres'].apply(lambda x: x.split('|') if x else [])
    return df

movies = load_data()

# Unique genres for dropdown
all_genres = sorted({genre for sublist in movies['genre_list'] for genre in sublist if genre})
selected_genre = st.sidebar.selectbox("🎞️ Select a genre", options=all_genres)

# Filter movies by selected genre
filtered_movies = movies[movies['genre_list'].apply(lambda genres: selected_genre in genres)]

top_n = st.sidebar.slider("🎬 How many top movies to show?", 5, 20, 5)
top_movies = filtered_movies.sort_values(by='avg_rating', ascending=False).head(top_n)

# Display Top-Rated Table
st.subheader(f"⭐ Top-Rated Movies in Genre: {selected_genre}")
table = top_movies[['title', 'avg_rating', 'rating_count']].copy()
table.columns = ['Movie Title', 'Average Rating', 'Number of Ratings']
st.dataframe(table.reset_index(drop=True), use_container_width=True)

# Dual Column Layout
col1, col2 = st.columns(2)

# Rating Histogram
with col1:
    st.markdown("### 🎯 Rating Distribution")
    fig = px.histogram(
        filtered_movies,
        x="avg_rating",
        nbins=20,
        labels={"avg_rating": "Average Rating"},
        color_discrete_sequence=["#4CAF50"]
    )
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)

# Word Cloud of Tags
with col2:
    st.markdown("### ☁️ Common Tags")
    tags_text = ' '.join(filtered_movies['all_tags'].dropna().astype(str).tolist())
    wordcloud = WordCloud(
        width=600,
        height=400,
        background_color='white',
        colormap='Greens',
        max_words=100
    ).generate(tags_text)
    fig_wc, ax = plt.subplots(figsize=(6, 4))
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis('off')
    st.pyplot(fig_wc)

# Footer
st.markdown("""
---
<p style='text-align: center; font-size: small;'>
Built for the Data Viz CA • Designed with 💡 for younger movie lovers aged 18–35
</p>
""", unsafe_allow_html=True)