# 🎬 Movie Recommendation System
# Dataset: TMDB 5000 Movies
# Tech: Python + Pandas

import pandas as pd

# ── Load Data ──────────────────────────────────────────────
print("Loading movie dataset...")
df = pd.read_csv("tmdb_5000_movies.csv")
df = df.dropna(subset=['title', 'vote_average', 'genres'])
df['genres'] = df['genres'].fillna('')
print(f"✅ Loaded {len(df)} movies successfully!\n")

# ── Functions ──────────────────────────────────────────────

def show_top_movies(n=10):
    top = df[['title', 'vote_average', 'release_date']] \
        .sort_values(by='vote_average', ascending=False) \
        .head(n)
    print(f"\n🎬 Top {n} Highest Rated Movies:")
    print("-" * 50)
    for _, row in top.iterrows():
        year = str(row['release_date'])[:4]
        print(f"  {row['title']} ({year}) — {row['vote_average']}/10")

def search_by_genre(genre):
    filtered = df[df['genres'].str.contains(genre, case=False, na=False)]
    filtered = filtered.sort_values(by='vote_average', ascending=False).head(10)
    if filtered.empty:
        print(f"\n  ❌ No movies found for genre: {genre}")
    else:
        print(f"\n🎭 Top movies in '{genre}':")
        print("-" * 50)
        for _, row in filtered.iterrows():
            year = str(row['release_date'])[:4]
            print(f"  {row['title']} ({year}) — {row['vote_average']}/10")

def recommend_similar(movie_title):
    movie = df[df['title'].str.contains(movie_title, case=False, na=False)]
    if movie.empty:
        print(f"\n  ❌ Movie '{movie_title}' not found.")
        return
    base        = movie.iloc[0]
    base_title  = base['title']
    base_genres = base['genres']
    # extract genre names from JSON-like string
    import re
    genre_names = re.findall(r'"name":\s*"([^"]+)"', base_genres)
    if not genre_names:
        print(f"\n  ❌ Could not extract genres for '{base_title}'.")
        return
    pattern = '|'.join(genre_names)
    similar = df[df['genres'].str.contains(pattern, case=False, na=False)]
    similar = similar[similar['title'] != base_title]
    similar = similar.sort_values(by='vote_average', ascending=False).head(5)
    print(f"\n✨ Because you liked '{base_title}', try:")
    print("-" * 50)
    for _, row in similar.iterrows():
        year = str(row['release_date'])[:4]
        print(f"  {row['title']} ({year}) — {row['vote_average']}/10")

def search_by_language(lang):
    filtered = df[df['original_language'].str.contains(lang, case=False, na=False)]
    filtered = filtered.sort_values(by='vote_average', ascending=False).head(10)
    if filtered.empty:
        print(f"\n  ❌ No movies found for language: {lang}")
    else:
        print(f"\n🌍 Top '{lang}' movies:")
        print("-" * 50)
        for _, row in filtered.iterrows():
            year = str(row['release_date'])[:4]
            print(f"  {row['title']} ({year}) — {row['vote_average']}/10")

# ── Main Menu ──────────────────────────────────────────────

def main():
    while True:
        print("\n========== 🎬 Movie Recommender ==========")
        print("  1. Show top rated movies")
        print("  2. Search by genre")
        print("  3. Get recommendations for a movie")
        print("  4. Search by language")
        print("  5. Exit")
        print("==========================================")

        choice = input("Enter choice (1/2/3/4/5): ").strip()

        if choice == '1':
            show_top_movies()
        elif choice == '2':
            genre = input("Enter genre (e.g. Action, Comedy, Drama): ").strip()
            search_by_genre(genre)
        elif choice == '3':
            title = input("Enter a movie name: ").strip()
            recommend_similar(title)
        elif choice == '4':
            lang = input("Enter language code (e.g. en, hi, fr): ").strip()
            search_by_language(lang)
        elif choice == '5':
            print("\nGoodbye! 🎬")
            break
        else:
            print("  ⚠️  Invalid choice. Enter 1, 2, 3, 4 or 5.")

if __name__ == "__main__":
    main()
