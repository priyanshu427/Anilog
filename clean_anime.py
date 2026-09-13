import ast

import pandas as pd

# 1. Load raw csv
df = pd.read_csv("animes.csv")

# 2. Keep only the columns we actually care about
columns_to_keep = [
    "title",
    "synopsis",
    "genre",
    "episodes",
    "score",
    "ranked",
    "popularity",
    "img_url"
]
df = df[columns_to_keep]

# 3. Drop rows missing critical frontend/backend data
df = df.dropna(subset=["title", "synopsis", "img_url", "score"])

# 4. Clean genres: convert stringified python lists "['Action', 'Sci-Fi']" into clean CSV text "Action, Sci-Fi"
def format_genres(val):
    try:
        parsed = ast.literal_eval(val)
        if isinstance(parsed, list):
            return ", ".join(parsed)
    except Exception:
        pass
    return str(val).strip("[]'\" ")

df["genre"] = df["genre"].apply(format_genres)

# 5. Clean episodes: fill missing/ongoing with 0, convert float to int
df["episodes"] = df["episodes"].fillna(0).astype(int)

# 6. Filter out explicit genres or junk entries if desired
df = df[~df["genre"].str.contains("Hentai|Erotica", case=False, na=False)]

# 7. Sort by score / popularity and take the top 800 highest-rated entries
df = df.sort_values(by="score", ascending=False).drop_duplicates(subset=["title"])
clean_df = df.head(800)

# 8. Export lean seed file
clean_df.to_csv("anime_seed.csv", index=False)
print(f"Done! Created anime_seed.csv with {len(clean_df)} clean rows.")