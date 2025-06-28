import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import ast

# Load cleaned data
df = pd.read_csv("imdb_clean.csv")

# Convert columns from string to lists
df['Genres'] = df['Genres'].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else [])
df['Top 3 Cast'] = df['Top 3 Cast'].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else [])

# Explode genre and cast lists
genres_df = df[['Title', 'Genres']].explode('Genres')
cast_df = df[['Title', 'Top 3 Cast']].explode('Top 3 Cast')

# Set seaborn style
sns.set(style="whitegrid")
plt.figure(figsize=(10, 6))

# 1. Top 10 Genres
top_genres = genres_df['Genres'].value_counts().head(10)
if not top_genres.empty:
    top_genres.plot(kind='bar', color='skyblue')
    plt.title("Top 10 Movie Genres")
    plt.ylabel("Count")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("top_genres.png")
    plt.clf()
else:
    print("⚠️ No genres found to plot.")

# 2. Top 10 Actors
top_actors = cast_df['Top 3 Cast'].value_counts().head(10)
if not top_actors.empty:
    top_actors.plot(kind='barh', color='orange')
    plt.title("Top 10 Most Frequent Actors")
    plt.xlabel("Appearances")
    plt.gca().invert_yaxis()
    plt.tight_layout()
    plt.savefig("top_actors.png")
    plt.clf()
else:
    print("⚠️ No actor data found to plot.")

# 3. Average IMDb Rating by Year
avg_rating = df.groupby('Year')['Rating'].mean().dropna()
if not avg_rating.empty:
    sns.lineplot(x=avg_rating.index, y=avg_rating.values, marker='o', color='green')
    plt.title("Average IMDb Rating by Year")
    plt.xlabel("Year")
    plt.ylabel("Average Rating")
    plt.tight_layout()
    plt.savefig("avg_rating_by_year.png")
    plt.clf()
else:
    print("⚠️ No yearly rating data found.")

# 4. Top 10 Directors by Average Rating
top_directors = df.groupby('Director')['Rating'].mean().sort_values(ascending=False).head(10)
if not top_directors.empty:
    top_directors.plot(kind='bar', color='purple')
    plt.title("Top 10 Directors by Avg IMDb Rating")
    plt.ylabel("Average Rating")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("top_directors.png")
    plt.clf()
else:
    print("⚠️ No director data found.")

# 5. Top 10 Box Office Movies
top_box_office = df.sort_values('Box Office', ascending=False).dropna(subset=['Box Office']).head(10)
if not top_box_office.empty:
    sns.barplot(x='Box Office', y='Title', data=top_box_office, palette='mako')
    plt.title("Top 10 Movies by Worldwide Box Office")
    plt.xlabel("Gross ($)")
    plt.tight_layout()
    plt.savefig("top_box_office.png")
    plt.clf()
else:
    print("⚠️ No box office data found.")

print("✅ All visuals created and saved as PNG files.")
