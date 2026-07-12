# Assignment 20 — Building & Deploying a Recommendation System

## Dataset

| Field | Detail |
|---|---|
| **Dataset Name** | TMDB 5000 Movies Dataset |
| **Dataset Source** | The Movie Database (TMDB) via Kaggle |
| **Kaggle Link** | https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata |

The dataset contains metadata for **4,803 movies** including title, overview (plot description),  
genres, keywords, vote average, and release date.

**Key columns used for recommendations:**
- `overview` — plot description text
- `genres` — JSON list of genre objects
- `keywords` — JSON list of keyword objects

---

## Tasks Completed

| Part | Task | Description |
|---|---|---|
| PART 1 | Task 1 | Load & understand the TMDB dataset — shape, columns, sample rows |
| PART 1 | Task 2 | Text preprocessing — parse JSON genres/keywords, clean overview text, build `clean_text` |
| PART 2 | Task 3 | TF-IDF vectorization — max_features=10,000, ngram_range=(1,2), min_df=2 |
| PART 2 | Task 4 | Cosine similarity matrix — computed for all movie pairs, explained and visualized |
| PART 3 | Task 5 | `recommend()` function — finds top N similar movies for any title |
| PART 3 | Task 5 | Tested on 3 different movies: The Dark Knight, Toy Story, Titanic |
| PART 4 | Task 6 | Streamlit UI — dropdown selector, sidebar controls, similarity scores displayed |
| PART 5 | Task 7 | Git & GitHub setup instructions |
| PART 5 | Task 8 | Render deployment — build command, start command, live URL |
| PART 5 | Task 9 | Final validation of deployed app |

---

## Libraries Used

```
pandas       — dataset loading and manipulation
numpy        — numerical operations on similarity matrices
scikit-learn — TfidfVectorizer, cosine_similarity
nltk         — stopword list for text cleaning
streamlit    — web application UI and deployment
matplotlib   — similarity score distribution chart
ast          — parsing JSON-like genre/keyword strings
re           — regex-based text cleaning
```

---

## Folder Structure

```
GenAI-Task20-AbhishekThakare/
│
├── app.py                   ← Streamlit web application (main entry point)
├── task20.ipynb             ← Analysis notebook — all tasks with explanations
├── requirements.txt         ← Python dependencies for Render deployment
├── README.md                ← This file
├── tmdb_5000_movies.csv     ← Dataset (download from Kaggle — not in zip)
│
└── outputs/
    ├── similarity_distribution.png   ← Cosine similarity histogram chart
    ├── recs_dark_knight.csv          ← Recommendations for The Dark Knight
    ├── recs_toy_story.csv            ← Recommendations for Toy Story
    └── recs_titanic.csv              ← Recommendations for Titanic
```

---

## How to Run

### Step 1 — Download the dataset
Go to https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata  
Download `tmdb_5000_movies.csv` and place it in the project folder.

### Step 2 — Install dependencies
```bash
pip install pandas numpy scikit-learn nltk streamlit matplotlib
```

### Step 3 — Run the Streamlit app locally
```bash
streamlit run app.py
```
Open http://localhost:8501 in your browser.

### Step 4 — Run the analysis notebook (optional)
```bash
jupyter notebook task20.ipynb
```

---

## Deploying to Render

1. Push this folder to a GitHub repository.
2. Go to https://render.com → **New → Web Service**.
3. Connect your GitHub repo.
4. Set the following:
   - **Build command:** `pip install -r requirements.txt`
   - **Start command:** `streamlit run app.py --server.port $PORT --server.address 0.0.0.0`
5. Click **Create Web Service**.
6. Render will build and deploy automatically. Copy the live URL.

> **Important:** Commit `tmdb_5000_movies.csv` to the repo, or mount it as a Render persistent disk.  
> The free Render tier sleeps after inactivity — the first request after sleep may take ~30 seconds.

---

## Learning Outcomes

1. Learned how to build a **content-based recommendation system** from scratch using TF-IDF and cosine similarity.
2. Understood how to parse and use structured metadata (JSON genre/keyword strings) as text features.
3. Practiced combining multiple text sources (overview + genres + keywords) into a single feature column.
4. Learned how TF-IDF parameters (`max_features`, `min_df`, `max_df`, `ngram_range`) affect the vocabulary and recommendation quality.
5. Understood **cosine similarity** — why it works for text, and how score distribution reveals dataset sparsity.
6. Built and deployed a working **Streamlit web app** with caching, sidebar controls, and structured result display.
7. Learned the end-to-end workflow: local development → GitHub → Render deployment.

---

## Challenges Faced

| Challenge | How It Was Resolved |
|---|---|
| Genres and keywords stored as JSON strings, not lists | Used `ast.literal_eval()` to parse them into Python objects, then extracted the `name` field |
| Multi-word genres like "Science Fiction" becoming two separate tokens | Replaced spaces with underscores (`science_fiction`) so the genre stays as one token |
| Missing overviews causing errors | Used `.fillna("")` before applying the clean function — missing overviews become empty strings |
| Slow cosine similarity computation on first load | Used Streamlit's `@st.cache_data` decorator — the matrix is computed once and cached for the session |
| Render free tier cold-start delay | Documented in README; users are informed that the first request after inactivity may be slow |

---

## Key Findings

1. Combining overview + genres + keywords produced significantly better genre-consistent recommendations than overview text alone.
2. Most movie pairs have near-zero cosine similarity — the distribution is heavily right-skewed. Only the top 1–2% of movies are meaningfully similar to any given film.
3. TMDB bigrams like `based true` (based on a true story) and `new york` became useful discriminating features that unigrams would have missed.
4. The system correctly differentiates across genres: Dark Knight recommendations were crime/action films; Toy Story recommendations were animated family films; Titanic recommendations were romance/drama films.
5. Content-based filtering works without any user history — a key advantage over collaborative filtering for new or sparse systems.

---

## Deployed App

**Live URL:** *(Add your Render URL here after deployment)*

---

## Submitted By

**Abhishek Thakare**  
Assignment 20 — GenAI / NLP Track  
TuteDude
