import streamlit as st
import pickle
import pandas as pd
import gdown
import os

# Google Drive file link for similarity.pkl
drive_link = "https://drive.google.com/file/d/1rCprEkE55OzISkK6rOuw_Sa5mA1QV19r/view?usp=sharing"
file_id = drive_link.split("/d/")[1].split("/")[0]
file_url = f"https://drive.google.com/uc?export=download&id={file_id}"

# Check if similarity.pkl exists, if not, download it
if not os.path.exists("similarity.pkl"):
    st.write("Downloading similarity.pkl from Google Drive...")
    gdown.download(file_url, "similarity.pkl", quiet=False)
    st.write("Download complete!")

# Load the processed data
new_netflix = pickle.load(open('movies.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

# Define the recommendation function
def recommend(movie):
    if movie not in new_netflix['original_title'].values:
        return ["Movie not found! Please choose a valid movie."]
    
    movie_index = new_netflix[new_netflix['original_title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    
    recommended_movies = [new_netflix.iloc[i[0]]['original_title'] for i in movies_list]
    return recommended_movies

# Streamlit UI
st.title("🎬 Netflix Movie Recommendation System")

# Movie selection dropdown
selected_movie = st.selectbox("Select a Movie", new_netflix['original_title'].values)

if st.button("Recommend"):
    recommendations = recommend(selected_movie)
    st.subheader("Recommended Movies:")
    for rec in recommendations:
        st.write(f"🎥 {rec}")


