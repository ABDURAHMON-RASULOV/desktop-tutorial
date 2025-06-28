import pandas as pd

# Load cleaned data
df = pd.read_csv("imdb_clean.csv")

# Convert list columns back to real lists
import ast
df['Genres'] = df['Genres'].apply(ast.literal_eval)
df['Top 3 Cast'] = df['Top 3 Cast'].apply(ast.literal_eval)

# Explode list columns
genres_df = df[['Title', 'Genres']].explode('Genres')
cast_df = df[['Title', 'Top 3 Cast']].explode('Top 3 Cast')

# 🔹 1. Top Genres
top_genres = genres_df['Genres'].value_counts().head(10)
print("🎬 Top Genres:\n", top_genres)

# 🔹 2. Top Actors (most frequent)
top_actors = cast_df['Top 3 Cast'].value_counts().head(10)
print("\n🧑‍🎤 Top Actors:\n", top_actors)

# 🔹 3. Best Directors (by average rating)
top_directors = df.groupby('Director')['Rating'].mean().sort_values(ascending=False).head(10)
print("\n🎥 Top Directors (by Avg Rating):\n", top_directors)

# 🔹 4. Top 10 Box Office Movies
top_box_office = df.sort_values(by='Box Office', ascending=False).head(10)[['Title', 'Box Office']]
print("\n💸 Top Grossing Movies:\n", top_box_office)

# 🔹 5. Average Rating Over Time
avg_rating_by_year = df.groupby('Year')['Rating'].mean().dropna()
print("\n📈 Average IMDb Rating by Year:\n", avg_rating_by_year.tail(10))
