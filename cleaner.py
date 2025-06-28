import pandas as pd
import ast

# Load raw scraped data
df = pd.read_csv("imdb_top250_raw.csv")

# Safe string-to-list conversion
def safe_eval(val):
    try:
        return ast.literal_eval(val) if isinstance(val, str) and val.startswith("[") else []
    except:
        return []

df['Genres'] = df['Genres'].apply(safe_eval)
df['Top 3 Cast'] = df['Top 3 Cast'].apply(safe_eval)

# Fix numbers
df['Year'] = pd.to_numeric(df['Year'], errors='coerce')
df['Rating'] = pd.to_numeric(df['Rating'], errors='coerce')
df['Votes'] = pd.to_numeric(df['Votes'], errors='coerce')

# Clean Box Office
df['Box Office'] = df['Box Office'].replace(r'[\$,]', '', regex=True).replace('N/A', None)
df['Box Office'] = pd.to_numeric(df['Box Office'], errors='coerce')

# Save cleaned version
df.to_csv("imdb_clean.csv", index=False)
print("✅ Cleaned data saved to imdb_clean.csv")
