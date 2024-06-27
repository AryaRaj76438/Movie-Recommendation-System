import pickle
import pandas as pd
import requests
import streamlit as st

st.title('Movie Recommendation System')

#  Define all the function that are required
def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=c919ad2cca17e44672935cc27da8a475&language=en-US'.format(movie_id))
    data = response.json()
    return "https://image.tmdb.org/t/p/w500"+data['poster_path']

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)),reverse=True, key=lambda x:x[1])[1:select_number_movie+1]

    recommend_movies = []
    recommend_movies_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommend_movies.append(movies.iloc[i[0]].title)
        recommend_movies_posters.append(fetch_poster(movie_id))
    return recommend_movies, recommend_movies_posters

movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))

select_number_movie = st.selectbox(
    'Select number to be suggested',
    [5,10,15]
)
selected_movie_name = st.selectbox(
    'Select Movie',
    movies['title'].values
)

if st.button('Recommend'):
    names,posters = recommend(selected_movie_name)
    # col = ['col1', 'col2', 'col3', 'col4', col5]
    [col1, col2, col3, col4, col5] = st.columns(5)
    # for i in range(0,5):
    #     with f"col{i}":
    #         st.text(names[i])
    #         st.image(posters[i])
    #

    num_columns = select_number_movie
    columns = st.columns(num_columns)

    for i in range(num_columns):
        with columns[i]:
            st.text(names[i])
            st.image(posters[i])

    # with col1:
    #     st.text(names[0])
    #     st.image(posters[0])
    # with col2:
    #     st.text(names[1])
    #     st.image(posters[1])
    # with col3:
    #     st.text(names[2])
    #     st.image(posters[2])
    # with col4:
    #     st.text(names[3])
    #     st.image(posters[3])
    # with col5:
    #     st.text(names[4])
    #     st.image(posters[4])