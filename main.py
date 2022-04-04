import pickle
import streamlit as st
import requests
import os
from dotenv import load_dotenv
import ast

load_dotenv()
api_key = os.getenv('API_key')


def get_movie_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}"
    data = requests.get(url)
    data = data.json() 
    print(data)
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

def recommend(movie_title):
    index = movies_db[movies_db['title'] == movie_title].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters= []

    for i in distances[1:6]:
        ## retreiving the movie posters
        movie_id = movies_db.iloc[i[0]].movie_id
        recommended_movie_posters.append(get_movie_poster(movie_id))
        recommended_movie_names.append(movies_db.iloc[i[0]].title)

    return recommended_movie_names, recommended_movie_posters

st.header("Movie recommendation system")
movies_db = pickle.load(open('notebook/artifacts/movie_list.pkl','rb'))
similarity = pickle.load(open('notebook/artifacts/similarity.pkl','rb'))


movie_list = movies_db['title'].values
selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_list
)

if st.button('Show Recommendation'):
    recommended_movie_names,recommended_movie_posters = recommend(selected_movie)
    # col1, col2, col3, col4, col5 = st.columns(5)
    # col=[]
    col = st.columns(5)
    for i in range(5):
        with col[i]:
            st.text(recommended_movie_names[i])
            st.image(recommended_movie_posters[i])
    # with col1:
    #     st.text(recommended_movie_names[0])
    #     st.image(recommended_movie_posters[0])
    # with col2:
    #     st.text(recommended_movie_names[1])
    #     st.image(recommended_movie_posters[1])

    # with col3:
    #     st.text(recommended_movie_names[2])
    #     st.image(recommended_movie_posters[2])
    # with col4:
    #     st.text(recommended_movie_names[3])
    #     st.image(recommended_movie_posters[3])
    # with col5:
    #     st.text(recommended_movie_names[4])
    #     st.image(recommended_movie_posters[4])