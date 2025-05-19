import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans, DBSCAN, AgglomerativeClustering
import numpy as np

# Page config
st.set_page_config(page_title="🎬 Movie Explorer Dashboard", layout="wide")

# Custom title with styling for younger audience
st.markdown("""
    <h1 style='text-align: center; color: #4CAF50;'>🎬 Movie Explorer Dashboard</h1>
    <p style='text-align: center;'>Explore your favorite genres and discover trending clusters of movies 🔍🍿</p>
""", unsafe_allow_html=True)

# Load your cleaned data
@st.cache_data
def load_data():
    df = pd.read_csv("movies_full_cleaned.csv")  # Replace with your final dataset path
    return df

movies_full = load_data()


# Create 'main_genre' if it's missing
if 'main_genre' not in movies_full.columns:
    movies_full['main_genre'] = movies_full['genres'].apply(lambda x: x.split('|')[0] if pd.notnull(x) else 'Unknown')


# Sidebar filters
st.sidebar.header("🔧 Filters")
selected_genre = st.sidebar.selectbox("Choose a genre:", options=sorted(movies_full['main_genre'].unique()))

# Filtered data
filtered_movies = movies_full[movies_full['main_genre'] == selected_genre]

# Display top-rated movies
st.subheader(f"⭐ Top-Rated '{selected_genre}' Movies")
top_n = st.slider("How many top movies to show?", 5, 20, 10)
top_movies = filtered_movies.sort_values(by='avg_rating', ascending=False).head(top_n)
st.dataframe(top_movies[['title', 'avg_rating', 'rating_count']])

# Clustering section
st.markdown("""
### 🔍 Movie Clustering Overview
This section shows how movies are grouped based on their characteristics. Clustering helps identify patterns useful for recommendation engines.
""")

# Clustering setup
features = ['avg_rating', 'rating_count'] + [col for col in movies_full.columns if col.startswith('genre_')]
X = movies_full[features]
X_scaled = StandardScaler().fit_transform(X)

# PCA for plotting
pca = PCA(n_components=2)
X_pca = pca.fit_transform(X_scaled)

# Clustering algorithms
kmeans = KMeans(n_clusters=5, random_state=42).fit(X_scaled)
kmeans_labels = kmeans.labels_

dbscan = DBSCAN(eps=2.5, min_samples=5).fit(X_pca)
dbscan_labels = dbscan.labels_

agglo = AgglomerativeClustering(n_clusters=5).fit(X_scaled)
agglo_labels = agglo.labels_

# Interactive plots
def plot_clusters(X, labels, title):
    fig = px.scatter(
        x=X[:, 0], y=X[:, 1], color=labels.astype(str),
        title=title,
        labels={"x": "PCA Component 1", "y": "PCA Component 2"},
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    st.plotly_chart(fig, use_container_width=True)

plot_clusters(X_pca, kmeans_labels, "K-Means Clustering")
plot_clusters(X_pca, dbscan_labels, "DBSCAN Clustering")
plot_clusters(X_pca, agglo_labels, "Agglomerative Clustering")

# Cluster profile summary
st.markdown("""
### 📊 K-Means Cluster Profiles
Here’s a breakdown of average rating and count per cluster, which helps businesses tailor content by audience segment.
""")
movies_full['Cluster_KMeans'] = kmeans_labels
profile = movies_full.groupby('Cluster_KMeans')[['avg_rating', 'rating_count']].mean().round(2)
st.dataframe(profile)

# Footer
st.markdown("""
---
<p style='text-align: center; font-size: small;'>
Built for the Data Viz CA • Designed with 💡 for younger movie lovers aged 18–35
</p>
""", unsafe_allow_html=True)