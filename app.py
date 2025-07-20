import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Netflix EDA", layout="wide")
st.title("🎬 Netflix Data Explorer")

# Load cleaned dataset
df = pd.read_csv("data/processed/netflix_cleaned.csv")

# Sidebar Filters
st.sidebar.header("Filter Options")
type_filter = st.sidebar.multiselect("Select Content Type:", df['type'].unique(), default=df['type'].unique())
country_filter = st.sidebar.multiselect("Select Country:", df['country'].unique(), default=["United States", "India"])
year_filter = st.sidebar.slider("Select Year Range:", int(df['year_added'].min()), int(df['year_added'].max()), (2015, 2021))

# Apply filters
df_filtered = df[
    (df['type'].isin(type_filter)) &
    (df['country'].isin(country_filter)) &
    (df['year_added'] >= year_filter[0]) &
    (df['year_added'] <= year_filter[1])
]

# Show filtered data summary
st.markdown(f"### Showing {len(df_filtered)} titles")
st.dataframe(df_filtered.head(20))

# Visualization 1: Content Type Count
st.subheader("Content Type Distribution")
fig1, ax1 = plt.subplots()
sns.countplot(data=df_filtered, x='type', ax=ax1, palette='Set2')
st.pyplot(fig1)

# Visualization 2: Year-wise Trend
st.subheader("Year-wise Content Added")
fig2, ax2 = plt.subplots()
sns.countplot(data=df_filtered, x='year_added', hue='type', ax=ax2, palette='Set1')
plt.xticks(rotation=45)
st.pyplot(fig2)

# Visualization 3: Top Genres
st.subheader("Top Genres (Quick View)")
from collections import Counter
genre_series = df_filtered['listed_in'].dropna().apply(lambda x: x.split(', '))
all_genres = [genre for sublist in genre_series for genre in sublist]
top_genres = pd.DataFrame(Counter(all_genres).most_common(10), columns=['Genre', 'Count'])

fig3, ax3 = plt.subplots()
sns.barplot(data=top_genres, y='Genre', x='Count', palette='magma', ax=ax3)
st.pyplot(fig3)
