import streamlit as st
import pandas as pd
import plotly.express as px
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# -----------------------------
# Page configuration
# -----------------------------
st.set_page_config(page_title="🎬 Movie Explorer Dashboard", layout="wide")

# -----------------------------
# Title and Intro
# -----------------------------
st.markdown("""
    <h1 style='text-align: center; color: #4CAF50;'>🎬 Movie Explorer Dashboard</h1>
    <p style='text-align: center;'>Explore your favorite genres and discover top-rated movies 🔍🍿</p>
""", unsafe_allow_html=True)

# -----------------------------
# Data Loading
# -----------------------------
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/melnikacg/DV_test_del/main/movies_full_cleaned.csv"
    df = pd.read_csv(url)
    
    if 'main_genre' not in df.columns:
        df['main_genre'] = df['genres'].apply(lambda x: x.split('|')[0] if pd.notnull(x) else 'Unknown')
    
    return df

movies_full = load_data()

# -----------------------------
# Sidebar Filters
# -----------------------------
st.sidebar.header("🔧 Filters")
selected_genre = st.sidebar.selectbox(
    "Choose a genre:",
    options=sorted(movies_full['main_genre'].unique())
)

# -----------------------------
# Top-Rated Movies by Genre
# -----------------------------
st.subheader(f"⭐ Top-Rated '{selected_genre}' Movies")
top_n = st.slider("How many top movies to show?", 5, 20, 10)

filtered_movies = movies_full[movies_full['main_genre'] == selected_genre]
top_movies = filtered_movies.sort_values(by='avg_rating', ascending=False).head(top_n)

st.dataframe(top_movies[['title', 'avg_rating', 'rating_count']])

# -----------------------------
# --- Dual Column Layout
# -----------------------------
col1, col2 = st.columns(2)

# --- Histogram of Ratings
with col1:
    st.markdown("### 🎯 Rating Distribution")
    fig = px.histogram(
        filtered_movies,
        x="avg_rating",
        nbins=20,
        title=f"Distribution of Ratings in '{selected_genre}' Movies",
        labels={"avg_rating": "Average Rating"},
        color_discrete_sequence=["#4CAF50"]
    )
    # Set height and margins to match visual proportions
    fig.update_layout(
        height=500,
        margin=dict(t=50, b=50)
    )
    st.plotly_chart(fig, use_container_width=True)

# --- Word Cloud of Tags
with col2:
    st.markdown("### ☁️ Common Tags in This Genre")
    
    tags_text = ' '.join(filtered_movies['all_tags'].dropna().astype(str).tolist())

    wordcloud = WordCloud(
        width=800,      # Wider to match column width
        height=500,     # Match height with Plotly chart
        background_color='white',
        colormap='Greens',
        max_words=100
    ).generate(tags_text)

    fig_wc, ax = plt.subplots(figsize=(8, 5))  # Match ~800x500 pixels
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis('off')
    plt.tight_layout(pad=0)  # Remove padding
    st.pyplot(fig_wc)

# -----------------------------
# Footer
# -----------------------------
st.markdown("""
---
<p style='text-align: center; font-size: small;'>
Built for the Data Viz CA • Designed with 💡 for younger movie lovers aged 18–35
</p>
""", unsafe_allow_html=True)