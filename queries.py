import pandas as pd
# import psycopg2
import sqlite3
import streamlit as st



@st.cache_data
def load_studio_count():
    connection = sqlite3.connect('Movies.db')

    query_01 = """
        SELECT studio_main, COUNT(*) AS value_count
        FROM MyAnime
        WHERE studio_main != 'Unknown'
        GROUP BY studio_main
        ORDER BY value_count DESC
        LIMIT 10;
    """
    df__1 = pd.read_sql_query(query_01, connection)
    connection.close()
    return df__1
df_1 = load_studio_count()

@st.cache_data
def load_streaming_data():
    connection = sqlite3.connect('Movies.db')

    query_02 = """
        SELECT 
            m.*, 
            COALESCE(m.streaming_platforms, 'Not Specified') AS streaming_not_null,
            COALESCE(a.image_url, 'https://via.placeholder.com/150') AS image_url_not_null
        FROM MyAnime m
        LEFT JOIN anime_dataset_20k a ON m.title_english = a.title_english;
    """
    df__2 = pd.read_sql_query(query_02, connection)
    connection.close()
    return df__2
df_streaming = load_streaming_data()

@st.cache_data
def load_anime_list():
    connection = sqlite3.connect('Movies.db')

    query = """
        SELECT * FROM MyAnime
        WHERE studio_main != 'Unknown'
    """
    df__3 = pd.read_sql_query(query, connection)
    connection.close()
    return df__3
df_list = load_anime_list()

#     COALESCE(m.streaming_platforms, 'Not Specified') AS streaming_not_null,
#     COALESCE(a.image_url, 'https://via.placeholder.com/150') AS image_url_not_null
# FROM MyAnime m
# LEFT JOIN anime_dataset_20k a ON m.title_english = a.title_english;
# """
# df_streaming = pd.read_sql_query(str_query, connection)
