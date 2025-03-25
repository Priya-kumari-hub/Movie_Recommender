import streamlit as st
import pickle
import pandas as pd
import gdown
import os

# Set page config
st.set_page_config(page_title="Movie Recommender", layout="wide")

@st.cache_resource
def load_movie_data():
    return pickle.load(open('movies.pkl', 'rb'))

@st.cache_resource
def load_similarity():
    # Download similarity matrix from Google Drive if not exists
    if not os.path.exists("similarity.pkl"):
        with st.spinner('Downloading similarity data... This may take a while'):
            # Direct download link (replace with your actual file ID)
            file_id = "1rCprEkE55OzISkK6rOuw_Sa5mA1QV19r"
            url = f"https://drive.google.com/uc?export=download&id={file_id}"
            gdown.download(url, "similarity.pkl", quiet=False)
    
    return pickle.load(open('similarity.pkl', 'rb'))

def recommend(movie, movies, similarity):
    try:
        movie_index = movies[movies['original_title'] == movie].index[0]
        distances = similarity[movie_index]
        movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
        return [movies.iloc[i[0]]['original_title'] for i in movies_list]
    except Exception as e:
        st.error(f"Error generating recommendations: {str(e)}")
        return []

# Load data
movies = load_movie_data()
similarity = load_similarity()

# UI Components
st.title("🍿 Movie Recommendation System")
st.markdown("Discover movies similar to your favorites!")

# Movie selection
selected_movie = st.selectbox(
    "Select a movie you like:",
    movies['original_title'].values,
    index=0,
    help="Start typing to search through our movie collection"
)

# Recommendation button
if st.button("Get Recommendations", type="primary"):
    with st.spinner('Finding similar movies...'):
        recommendations = recommend(selected_movie, movies, similarity)
    
    if recommendations:
        st.subheader("Recommended Movies:")
        cols = st.columns(3)
        for i, rec in enumerate(recommendations):
            with cols[i % 3]:
                st.success(f"🎬 {rec}")
    else:
        st.warning("No recommendations found. Try another movie.")