"""
Assignment 20 — Building & Deploying a Recommendation System
Content-Based Movie Recommender using TF-IDF + Cosine Similarity
Deployed via Streamlit on Render.
"""

import os
import re
import ast
import numpy as np
import pandas as pd
import streamlit as st

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.corpus import stopwords
import nltk

# ── NLTK downloads ──────────────────────────────────────────────────────────
for pkg in ["stopwords", "punkt", "punkt_tab"]:
    nltk.download(pkg, quiet=True)

os.makedirs("outputs", exist_ok=True)

# ── Page config ─────────────────────────────────────────────────────────────
st.set_page_config(page_title="Movie Recommender", page_icon="🎬", layout="centered")


# ── Helper: load & preprocess ───────────────────────────────────────────────
@st.cache_data
def load_and_prepare_data():
    """
    Load the TMDB movies CSV, build a combined text feature,
    compute TF-IDF matrix and cosine similarity matrix.
    All heavy work is cached so the app is fast after first load.
    """
    df = pd.read_csv("tmdb_5000_movies.csv")

    # Keep only the columns we need
    keep_cols = [
        "id",
        "title",
        "overview",
        "genres",
        "keywords",
        "vote_average",
        "release_date",
    ]
    df = df[[c for c in keep_cols if c in df.columns]].copy()

    # ── Parse JSON-like string columns ──────────────────────────────────────
    def extract_names(json_str):
        """Convert '[{"id":..., "name": "Action"}, ...]' → 'action adventure'"""
        try:
            items = ast.literal_eval(str(json_str))
            names = [item["name"].lower().replace(" ", "_") for item in items]
            return " ".join(names)
        except Exception:
            return ""

    if "genres" in df.columns:
        df["genres_clean"] = df["genres"].apply(extract_names)
    else:
        df["genres_clean"] = ""

    if "keywords" in df.columns:
        df["keywords_clean"] = df["keywords"].apply(extract_names)
    else:
        df["keywords_clean"] = ""

    # ── Preprocess overview text ─────────────────────────────────────────────
    stop_words = set(stopwords.words("english"))

    def clean_text(text):
        """Lowercase, remove punctuation/numbers, remove stopwords."""
        text = str(text).lower()
        text = re.sub(r"[^a-zA-Z\s]", "", text)
        tokens = text.split()
        tokens = [t for t in tokens if t not in stop_words and len(t) > 2]
        return " ".join(tokens)

    df["overview_clean"] = df["overview"].fillna("").apply(clean_text)

    # Handle missing values — fill with empty string
    df["clean_text"] = (
        df["overview_clean"] + " " + df["genres_clean"] + " " + df["keywords_clean"]
    ).str.strip()

    # Drop rows where we ended up with no text at all
    df = df[df["clean_text"].str.len() > 0].reset_index(drop=True)

    # ── TF-IDF Vectorization ─────────────────────────────────────────────────
    tfidf = TfidfVectorizer(
        max_features=10000,  # cap vocabulary to keep memory manageable
        ngram_range=(1, 2),  # unigrams + bigrams for richer matching
        min_df=2,  # ignore words appearing in fewer than 2 movies
        max_df=0.85,  # ignore words in more than 85% of movies
    )

    tfidf_matrix = tfidf.fit_transform(df["clean_text"])

    # ── Cosine Similarity ────────────────────────────────────────────────────
    cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

    # Build a title → index lookup for fast retrieval
    title_to_idx = pd.Series(df.index, index=df["title"].str.lower())

    return df, tfidf, tfidf_matrix, cosine_sim, title_to_idx


def recommend(movie_name: str, df, cosine_sim, title_to_idx, top_n: int = 5):
    """
    Return top_n most similar movies to movie_name.

    Steps:
    1. Find the index of the selected movie.
    2. Get its cosine similarity scores against all other movies.
    3. Sort by score (descending), skip the movie itself (score=1.0).
    4. Return the top_n results as a DataFrame.
    """
    name_lower = movie_name.lower()

    if name_lower not in title_to_idx.index:
        return None, f"'{movie_name}' not found in the dataset."

    # Some titles map to multiple rows — take the first
    idx = title_to_idx[name_lower]
    if isinstance(idx, pd.Series):
        idx = idx.iloc[0]

    # Similarity scores for this movie against all others
    sim_scores = list(enumerate(cosine_sim[idx]))

    # Sort by score, descending — skip position 0 (the movie itself)
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1 : top_n + 1]

    movie_indices = [i for i, _ in sim_scores]
    scores = [round(s, 4) for _, s in sim_scores]

    result_df = df.iloc[movie_indices][
        ["title", "genres_clean", "vote_average", "release_date"]
    ].copy()
    result_df["similarity_score"] = scores
    result_df = result_df.reset_index(drop=True)
    result_df.index += 1  # 1-based ranking

    return result_df, None


# ── Streamlit UI ─────────────────────────────────────────────────────────────
def main():
    st.title("🎬 Movie Recommendation System")
    st.markdown(
        "Content-based recommendations using **TF-IDF + Cosine Similarity**  \n"
        "on the TMDB 5000 Movies dataset."
    )
    st.markdown("---")

    # Load data with a spinner so the user knows it's working
    with st.spinner("Loading dataset and computing similarity matrix..."):
        df, tfidf, tfidf_matrix, cosine_sim, title_to_idx = load_and_prepare_data()

    st.success(f"✅ Dataset loaded — {len(df):,} movies ready.")

    # ── Sidebar controls ─────────────────────────────────────────────────────
    st.sidebar.header("⚙️ Settings")
    top_n = st.sidebar.slider(
        "Number of recommendations", min_value=3, max_value=15, value=5, step=1
    )
    st.sidebar.markdown("---")
    st.sidebar.markdown(
        "**About**  \n"
        "This app uses TF-IDF to convert movie overviews, genres, and keywords "
        "into vectors, then ranks all other movies by cosine similarity to your selection."
    )

    # ── Movie selector ───────────────────────────────────────────────────────
    all_titles = sorted(df["title"].dropna().unique().tolist())
    selected_movie = st.selectbox(
        "🔍 Select a movie to get recommendations:",
        options=all_titles,
        index=(
            all_titles.index("The Dark Knight")
            if "The Dark Knight" in all_titles
            else 0
        ),
    )

    # ── Generate button ──────────────────────────────────────────────────────
    if st.button("🎯 Get Recommendations", use_container_width=True):

        result_df, error = recommend(
            selected_movie, df, cosine_sim, title_to_idx, top_n=top_n
        )

        if error:
            st.error(error)
        else:
            st.markdown(f"### 🍿 Top {top_n} recommendations for **{selected_movie}**")
            st.markdown("---")

            for rank, row in result_df.iterrows():
                # Format genres for display
                genres_display = (
                    row["genres_clean"].replace("_", " ").title()
                    if row["genres_clean"]
                    else "—"
                )
                year = (
                    str(row["release_date"])[:4]
                    if pd.notna(row["release_date"])
                    and str(row["release_date"]) != "nan"
                    else "—"
                )
                vote = (
                    f"{row['vote_average']:.1f}/10"
                    if pd.notna(row["vote_average"])
                    else "—"
                )

                with st.container():
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.markdown(f"**{rank}. {row['title']}** ({year})")
                        st.caption(f"Genres: {genres_display}  |  Rating: {vote}")
                    with col2:
                        st.metric(
                            label="Similarity", value=f"{row['similarity_score']:.3f}"
                        )
                    st.markdown("---")

            # Save this recommendation run to outputs/
            result_df.to_csv(
                f"outputs/recommendations_{selected_movie.replace(' ', '_')[:40]}.csv",
                index=True,
            )
            st.caption("💾 Results saved to outputs/ folder.")

    # ── Dataset explorer ─────────────────────────────────────────────────────
    with st.expander("📊 Explore the Dataset"):
        st.write(f"**Shape:** {df.shape[0]:,} rows × {df.shape[1]} columns")
        st.write(f"**Columns:** {list(df.columns)}")
        st.dataframe(
            df[["title", "genres_clean", "vote_average", "release_date"]].head(10)
        )

    # ── TF-IDF info ──────────────────────────────────────────────────────────
    with st.expander("🔢 TF-IDF Matrix Info"):
        st.write(
            f"**Matrix shape:** {tfidf_matrix.shape[0]:,} movies × {tfidf_matrix.shape[1]:,} features"
        )
        st.write(f"**Vocabulary size:** {len(tfidf.vocabulary_):,} terms")
        st.write(f"**N-gram range:** (1, 2) — unigrams + bigrams")
        st.write("**Sample vocabulary (first 30 terms):**")
        sample_vocab = sorted(tfidf.vocabulary_.keys())[:30]
        st.write(sample_vocab)


def _is_running_with_streamlit() -> bool:
    try:
        from streamlit.runtime.scriptrunner import get_script_run_ctx

        return get_script_run_ctx() is not None
    except Exception:
        return False


if __name__ == "__main__":
    if _is_running_with_streamlit():
        main()
    else:
        print("This app must be launched with Streamlit.")
        print("Run it using: python -m streamlit run app.py")
