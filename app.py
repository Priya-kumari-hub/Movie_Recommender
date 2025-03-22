import streamlit as st
import pandas as pd
import pickle  # If using a trained model

# Load your movie dataset (modify as needed)
movies = ["Inception", "Interstellar", "The Dark Knight", "Avatar", "Titanic"]

# Function to recommend movies (Replace with your recommendation logic)
def recommend_movies(movie_name):
    recommendations = [m for m in movies if m.lower() != movie_name.lower()]
    return recommendations[:5]

# Streamlit UI
st.title("🎬 Movie Recommendation System")
st.write("Enter a movie name to get similar recommendations!")

movie_name = st.text_input("Enter a movie name:")
if st.button("Recommend"):
    if movie_name:
        recommended_movies = recommend_movies(movie_name)
        st.write("**Recommended Movies:**")
        for movie in recommended_movies:
            st.write(f"- {movie}")
    else:
        st.warning("Please enter a movie name!")

