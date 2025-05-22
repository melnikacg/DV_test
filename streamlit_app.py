import streamlit as st
import pandas as pd
import plotly.express as px

# Page configuration
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
    
    # Ensure main_genre is defined
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

# Filter and sort movies
filtered_movies = movies_full[movies_full['main_genre'] == selected_genre]
top_movies = filtered_movies.sort_values(by='avg_rating', ascending=False).head(top_n)

st.dataframe(top_movies[['title', 'avg_rating', 'rating_count']])

# -----------------------------
# Two Side-by-Side Graphs
# -----------------------------
st.markdown("### 📊 Genre-Based Insights")

col1, col2 = st.columns(2)

with col1:
    fig_hist = px.histogram(
        filtered_movies,
        x="avg_rating",
        nbins=20,
        title=f"Distribution of Ratings in '{selected_genre}' Movies",
        labels={"avg_rating": "Average Rating"},
        color_discrete_sequence=["#4CAF50"]
    )
    st.plotly_chart(fig_hist, use_container_width=True)

with col2:
    fig_scatter = px.scatter(
        filtered_movies,
        x="rating_count",
        y="avg_rating",
        title=f"Rating Count vs Avg Rating in '{selected_genre}'",
        labels={"rating_count": "Number of Ratings", "avg_rating": "Average Rating"},
        color_discrete_sequence=["#2196F3"],
        size_max=60
    )
    st.plotly_chart(fig_scatter, use_container_width=True)

# -----------------------------
# Footer
# -----------------------------
st.markdown("""
---
<p style='text-align: center; font-size: small;'>
Built for the Data Viz CA • Designed with 💡 for younger movie lovers aged 18–35
</p>
""", unsafe_allow_html=True)