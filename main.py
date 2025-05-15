import streamlit as st

# streamlit is used to convert this into web app , it is used for datasience and machine leerning projects
# it is simple to use for small projects like this 
# no need of html ,css ,js directly convert the python scriipts to website
# command for terminal is = streamlit run main.py 

import pickle
import requests

# api is used to fetch the movie poster and data 

API_KEY = "4899b79d"

def fetch_movie_info(title):
    url = f"http://www.omdbapi.com/?t={title}&apikey={API_KEY}"
    response = requests.get(url).json()
    if response["Response"] == "True":
        return {
            "Poster": response["Poster"],
            "Title": response["Title"],
            "Year": response["Year"],
            "Plot": response["Plot"],
        }
    else:
        return {"Title": title, "Error": response.get("Error")}


st.header("Movies Recommendation System")

movie_list = pickle.load(open('movies_list.pkl' , 'rb'))
similarity = pickle.load(open('similarity.pkl' , 'rb'))

selected_movie = st.selectbox("Select movie from dropdown" , movie_list.Title)

def recommend(movies):
    index = movie_list[movie_list['Title'] == movies].index[0]
    distance = sorted(list(enumerate(similarity[index])) , reverse=True , key=lambda vector:vector[1])
    recommend_movies = []
    for i in distance[0:10]:
       recommend_movies.append(movie_list.iloc[i[0]]) 
    return recommend_movies

if st.button("Show Recommendation"):
    cols = st.columns(3)
    # storing the data in grid layout that has 3 columns 
    result = recommend(selected_movie)
    for index , i in enumerate(result[1:]):  
        info = fetch_movie_info(i.Title)
        col = cols[index % 3]  
        # Show poster image if available
        with col:
            if info.get("Poster") and info["Poster"] != "N/A":
                st.image(info["Poster"], width=250)
            st.write(f"**{info.get('Title', 'Unknown')} ({info.get('Year', '')})**")
            st.write(info.get("Plot", "No plot available"))
            st.write("---")
    # result[1:] it will skip the movie itself and print next 9 movies 