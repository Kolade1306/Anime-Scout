import streamlit as st
from queries import df_1, df_list, df_streaming
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")

st.markdown("""
<style>
    .block-container {
        padding-top: 0.5rem;
        padding-bottom: 1rem;
        padding-left: 2rem;
        padding-right: 2rem;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<style>
    /* Hides the top Streamlit header bar */
    header {visibility: hidden;}
    /* Hides the footer */
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)



st.set_page_config(layout="wide")


# 1. Define your tab titles
tab1, tab2, tab3 = st.tabs(["📊 Overview", "🔍 Search Engine", "📋 Raw Data"])

df_streaming['year'] = df_streaming['year'].astype('Int64')  # Convert year to integer type for proper sorting and filtering


# 2. Add content inside each tab using 'with'
with tab1:
    # st.subheader("Dashboard Analytics")
    # st.title("Sales Dashboard")

    col1, col2 = st.columns(2)

    with col1:
        # 1. Calculate the percentage
        df_1["percentage"] = (df_1["value_count"] / df_1["value_count"].sum()) * 100

        # st.subheader("📊 Percentage of Total Movies by Studio")

        # 2. Render the table with custom column configurations
        st.dataframe(
            df_1[["studio_main", "percentage"]].head(8),  # Display only the top 8 studios
            hide_index=True,  # Hides the row number index column
            use_container_width=True,
            column_config={
                "studio_main": st.column_config.TextColumn("Studio Name"),
                "value_count": st.column_config.NumberColumn("Movie Count"),
                "percentage": st.column_config.ProgressColumn(
                    " Total Percentage (%)",
                    help="Percentage share of total movies",
                    format="%.1f%%",  # Displays numbers like "12.5%"
                    min_value=0,
                    max_value=100,
                ),
            },
        )


    with col2:
        #  st.header("Top Studios by Genre")
        genre_list = ["All"] + sorted(["Action", "Adventure", "Comedy", "Drama", "Fantasy", "Horror", "Mystery", "Romance", "Sci-Fi",
                    "Sports", "Shouen", "Shoujo", "Sienen", "Psychological", "Ecchi", "Isekai"])

        selected_genre = st.selectbox("Select a Genre", genre_list)

        if selected_genre == "All":
            df_isin = df_list
        elif isinstance(selected_genre, str):
            df_isin = df_list[df_list['genres'].str.contains(selected_genre, case=False, na=False)]
        else:
            df_isin = df_list


        chart_data = (
            df_isin.groupby('studio_main')
            .size()
            .reset_index(name='value_count')
            .sort_values(by='value_count', ascending=False)
            .head(10) # Top 10 studios for that genre
        )

        chart_data = chart_data.set_index('studio_main')
        st.bar_chart(chart_data)

    col3, col4 = st.columns(2)
    with col3:
        df_streaming['year'] = df_streaming['year'].astype('Int64')
        # data_year = {
        #     "Year": sorted(df_streaming['year'].unique()),
        #     "Genre_types": sorted(["Action", "Adventure", "Comedy", "Drama", "Fantasy", "Horror", "Mystery", "Romance", "Sci-Fi",
        #             "Sports", "Shouen", "Shoujo", "Sienen", "Psychological", "Ecchi", "Isekai"]),
        #     "Platform_count": []
        # } 

        YEARS = sorted(df_streaming['year'].dropna().unique())
        GENRES = sorted(["Action", "Adventure", "Comedy", "Drama", "Fantasy", "Horror", "Mystery", "Romance", "Sci-Fi",
                "Sports", "Shouen", "Shoujo", "Sienen", "Psychological", "Ecchi", "Isekai"])
        PLATFORM_COUNT = []
        start_year, end_year = st.slider("Select Year Range", min_value=1990, max_value=2026, value=(1990, 2026))

        for year in YEARS:
            if year >= start_year and year <= end_year:
                for genre in GENRES:
                    count = df_streaming[
                        (df_streaming['year'] == year) & 
                        (df_streaming['genres'].str.contains(genre, case=False, na=False))
                    ].shape[0]
                    PLATFORM_COUNT.append(count)

        data_year = {
            "Year": [year for year in YEARS if year >= start_year and year <= end_year for _ in GENRES],
            "Genre": [genre for _ in YEARS if _ >= start_year and _ <= end_year for genre in GENRES],
            "genre_count": PLATFORM_COUNT
        }
        streaming_year_df = pd.DataFrame(data_year)
        # st.subheader("📈 Yearly Streaming Platform Count by Genre")
        st.dataframe(streaming_year_df, height=300)

    with col4:
        df_trend = streaming_year_df.groupby('Year')['genre_count'].sum().reset_index()
        fig = px.line(df_trend, x='Year', y='genre_count', title='Total Anime Produced Over the Years')
        st.plotly_chart(fig, use_container_width=True)




with tab3:
    st.subheader("Dataset Preview")
    with st.container(border=True):
        st.header("Selection Table")
        col_a, col_b, col_c = st.columns(3)
        ratings = ["All"] + sorted([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
        unique_platforms = ["All"] + sorted(["Hulu", "Netflix", "Crunchyroll", "YouTube", "Amazon Prime Video", "Bilibili", 
                            "Tubi TV", "WeTV", "RetroCrush", "Adult Swim", "HIDIVE",  "Other"])
        # unique_streaming = df_streaming[df_streaming['streaming_not_null'].str.contains(unique_platforms, case=False, na=False)]
        df_streaming_1 = df_streaming.copy()
        with col_a:
            selected_rating = st.selectbox("Select a Rating", ratings)
            if selected_rating == "All":
                pass  # No filtering needed, show all ratings
            elif isinstance(selected_rating, int):
                df_streaming_1 = df_streaming_1[df_streaming_1['mal_score'] >= selected_rating]
            
        with col_b:
            selected_platform = st.selectbox("Select a Streaming Platform", unique_platforms)
            standard_platforms = ["Hulu", "Netflix", "Crunchyroll", "YouTube", "Amazon Prime Video", "Bilibili", 
                                "Tubi TV", "WeTV", "RetroCrush", "Adult Swim", "HIDIVE"]

            if selected_platform == "All":
                # 2. If "All" is selected, do not filter by platform at all
                pass
            elif selected_platform == "Other":
                # 1. If "Other" is selected, filter for rows that DO NOT contain any of the standard platforms
                pattern = '|'.join(standard_platforms)
                df_streaming_1 = df_streaming_1[~df_streaming_1['streaming_not_null'].str.contains(pattern, case=False, na=False)]
                # df_show = df_streaming_1[["title_english", "mal_score", "streaming_not_null", "genres", "type", "age_rating"]]
            else:
                # 2. If a normal platform is selected, filter for that specific platform
                df_streaming_1 = df_streaming_1[df_streaming_1['streaming_not_null'].str.contains(selected_platform, case=False, na=False)]
                # df_show = df_streaming_1[["title_english", "mal_score", "streaming_not_null", "genres", "type", "age_rating"]]


        with col_c:
            selected_genre_table = st.selectbox("Select a Genre for Table", genre_list)
            if selected_genre_table == "All":
                pass  # No filtering needed, show all genres
            elif isinstance(selected_genre_table, str):
                df_streaming_1 = df_streaming_1[df_streaming_1['genres'].str.contains(selected_genre_table, case=False, na=False)]


        df_show = df_streaming_1[["title_english", "mal_score", "type", "age_rating"]]
        st.dataframe(df_show.head(500), use_container_width=True, hide_index=True)


with tab2:
    st.subheader("Show Search Engine")
    with st.container(border=True):
        st.subheader("🔍 Show Search Engine")

        # 1. Create a text input for the search bar
        search_query = st.text_input("Type the name of a show:").strip() 

        # 2. Check if the user has typed something
        if search_query:
            # Perform a case-insensitive search on the title column 
            # (Replace 'title_english' with your actual title column name)
            search_results = df_streaming[df_streaming['title_english'].str.contains(search_query, case=False, na=False)]
            
            if not search_results.empty:
                st.success(f"Found {len(search_results)} match(es)!")
                # st.toast("Settings saved successfully!", icon="🎉")
                
                # If multiple shows match, let the user pick the exact one
                selected_show = st.selectbox(
                    "Select the exact show you want to view:", 
                    search_results['title_english'].unique()
                )
                
                # Pull the specific data row for that chosen show
                show_info = df_streaming[df_streaming['title_english'] == selected_show].iloc[0]
                st.divider()
                col_a1, col_a2 = st.columns([1, 2])
                with col_a1:
                    # Display the image of the show
                    st.image(show_info.get("image_url_not_null", "https://via.placeholder.com/150"), width = 400)
                with col_a2:
                    # 3. Display the details nicely using Markdown and layout columns
                    st.markdown(f"## {show_info['title_english']}")
                    
                    # Description/Synopsis
                    st.write("### Overview")
                    st.write(show_info.get('synopsis', 'No description available for this show.')) # Replace 'synopsis' with your description column name if different
                    
                    # Metrics layout for Episodes, Year, Score, etc.
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.metric("Episodes", show_info.get('episodes', 'N/A'))
                    with col2:
                        st.metric("Year", show_info.get('year', 'N/A'))
                    with col3:
                        st.metric("Score", show_info.get('mal_score', 'N/A'))
                    with col4:
                        st.metric("Type", show_info.get('type', 'N/A'))
                        
                    # Extra details
                    st.text(f"Genres: {show_info.get('genres', 'N/A')}")
                    st.text(f"Age Rating: {show_info.get('age_rating', 'N/A')}")
                    st.text(f"Studio: {show_info.get('studio_main', 'N/A')}")
                    st.text(f"Available on: {show_info.get('streaming_not_null', 'N/A')}")
                    
            else:
                st.warning("No shows found matching your search. Check your spelling or try another keyword!")

    with st.container(border=True):
        st.subheader(" 🎬 Anime Suggestions")
        col3, col4 = st.columns(2)
        with col3:
            df_streaming_2 = df_streaming.copy()
            GENRES_2 = sorted(["Action", "Adventure", "Comedy", "Drama", "Fantasy", "Horror", "Mystery", "Romance", "Sci-Fi",
                "Sports", "Shouen", "Shoujo", "Sienen", "Psychological", "Ecchi", "Isekai"])
            selected_genre_2 = st.multiselect("Select Genres for Suggestions", GENRES_2)
            if selected_genre_2:
                for g in selected_genre_2:    
                    df_streaming_2 = df_streaming_2[df_streaming_2['genres'].str.contains(g, case=False, na=False)]
                # st.dataframe(df_streaming_2[["title_english", "mal_score", "type", "age_rating"]])
                random_suggestions = df_streaming_2.sample(n=min(5, len(df_streaming_2)), random_state=42)
                st.subheader("Random Suggestions:")
                for _, suggestion in random_suggestions.iterrows():
                    st.write(f"- {suggestion['title_english']} ({suggestion['mal_score']})")
