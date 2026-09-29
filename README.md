# Anime-Scout
Streamlit based application that helps find the Anime of your preference.

A high-performance, mobile-responsive anime analytics and search dashboard built with **Streamlit**, **Pandas**, and **Plotly**, backed by an **SQLite** database.

---

## 🚀 Features

* **📊 Analytics & Insights**: Visualizes studio shares, genre trends, and release counts over time using Plotly charts and native Streamlit progress indicators.
* **🔍 Advanced Filtering**: Multi-select and regex-powered genre/platform filtering (`OR` & `AND` conditions).
* **📱 Mobile-Optimized UI**: Designed with a tight, screen-fitting layout and custom CSS styling to minimize scrolling on laptop screens and mobile viewports.
* **⚡ High Performance**: Optimized with `@st.cache_data` to ensure blazing-fast query speeds and data loads.

---

## 🛠️ Tech Stack

* **Frontend/UI**: [Streamlit](https://streamlit.io/)
* **Data Processing**: [Pandas](https://pandas.pydata.org/)
* **Visualizations**: [Plotly](https://plotly.com/python/)
* **Database**: SQLite

---

## 📂 Project Structure

```text
Dashboard/
│
├── app.py              # Main Streamlit application file
├── queries.py          # Database connection and cached data loader
├── my_anime.db         # SQLite database containing anime records
└── README.md           # Project documentation
