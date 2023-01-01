import streamlit as st
import pymongo
import requetes

st.title('IMDB top film and series')

# Initialize connection.
# Uses st.experimental_singleton to only run once.
@st.experimental_singleton
def init_connection():
    return pymongo.MongoClient("mongodb://localhost:27017")

client = init_connection()
db = client.IMDB
collection = db['IMDB']

st.write([data for data in requetes.data1()])
