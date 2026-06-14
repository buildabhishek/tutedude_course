# Assignment 18 — Text Vectorization Techniques

## Dataset

| Field | Detail |
|---|---|
| **Dataset Name** | SMS Spam Collection Dataset |
| **Dataset Source** | UCI Machine Learning Repository |
| **Kaggle Link** | https://www.kaggle.com/datasets/uciml/sms-spam-collection-dataset |

The dataset contains **5,572 SMS messages** labelled as either `ham` (legitimate) or `spam`.  
It has two usable columns — `v1` (label) and `v2` (message text) — plus three unnamed empty columns that are dropped during cleaning.

---

## Tasks Completed

| Part | Task | Description |
|---|---|---|
| PART 1 | Task 1 | Manual One-Hot Encoding using plain Python |
| PART 1 | Task 2 | One-Hot Encoding using `MultiLabelBinarizer` from Scikit-learn |
| PART 2 | Task 3 | Bag of Words representation using `CountVectorizer` |
| PART 2 | Task 4 | Word frequency analysis — top 10 most and least frequent words |
| PART 3 | Task 5 | Unigrams, Bigrams, and Trigrams — comparing vocabulary sizes |
| PART 3 | Task 6 | Combined (1,2)-gram vectorizer — context-aware features |
| PART 4 | Task 7 | TF-IDF vectorization using `TfidfVectorizer` |
| PART 4 | Task 8 | BoW vs TF-IDF comparison on common spam words |
| PART 5 | Task 9 | Vectorizer parameter exploration (`max_features`, `min_df`, `max_df`) |
| PART 5 | Task 10 | Conceptual questions — answered with evidence from the experiments |

---

## Libraries Used

```
pandas       — data loading, manipulation, and DataFrame display
numpy        — matrix operations and array handling
scikit-learn — CountVectorizer, TfidfVectorizer, MultiLabelBinarizer
nltk         — stopword lists, word tokenizer, WordNet lemmatizer
re           — regular expressions for text cleaning
os           — creating the outputs/ directory programmatically
```

---

## How to Run

### Step 1 — Download the dataset
Go to https://www.kaggle.com/datasets/uciml/sms-spam-collection-dataset  
Download `spam.csv` and place it in the same folder as `task18.ipynb`.

### Step 2 — Install dependencies
```bash
pip install pandas numpy scikit-learn nltk
```

### Step 3 — Download NLTK data
Run once in Python (already included in the notebook):
```python
import nltk
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('punkt')
nltk.download('punkt_tab')
```

### Step 4 — Run the notebook
Open `task18.ipynb` in Jupyter Notebook or JupyterLab and run all cells from top to bottom.

```bash
jupyter notebook task18.ipynb
```

The `outputs/` folder is created automatically by the notebook. Output CSVs will appear there after running.

---

## Folder Structure

```
GenAI-Task18-AbhishekThakare/
│
├── task18.ipynb          ← Main notebook with all 10 tasks
├── spam.csv              ← Dataset file (download from Kaggle)
├── README.md             ← This file
│
└── outputs/
    ├── manual_one_hot.csv    ← Task 1 output
    ├── sklearn_one_hot.csv   ← Task 2 output
    ├── bow_vectors.csv       ← Task 3 output
    └── tfidf_vectors.csv     ← Task 7 output
```

---

## Learning Outcomes

1. **One-Hot Encoding** converts text to binary presence/absence vectors. It is simple but ignores word frequency and treats each word as completely independent.

2. **Bag of Words** adds frequency counting, which gives classifiers more signal — a spam message repeating "FREE" five times scores differently from one that says it once.

3. **N-grams** capture local context. The bigram "free entry" is a much stronger spam signal than either word alone. However, bigrams also expand the feature space dramatically.

4. **TF-IDF** automatically down-weights words that appear everywhere (which carry little information) and up-weights rare but distinctive words. This makes it the most useful starting point for spam classification.

5. **Vectorizer parameters** (`max_features`, `min_df`, `max_df`) are powerful tuning levers that let you control vocabulary size, filter noise, and reduce memory usage without changing the algorithm.

---

## Challenges Faced

| Challenge | How It Was Resolved |
|---|---|
| `OSError: Cannot save file into a non-existent directory: 'outputs'` | Added `os.makedirs("outputs", exist_ok=True)` at the top of the notebook so the folder is always created before any CSV is saved. |
| Extra unnamed columns in `spam.csv` | Loaded the full file then immediately kept only `v1` and `v2`, renaming them to `label` and `message` for clarity. |
| `punkt_tab` NLTK resource missing on some machines | Added `nltk.download('punkt_tab', quiet=True)` alongside the other downloads. |
| BoW and TF-IDF matrices are too large to display directly | Used `.iloc[:5, :15]` slicing to show a readable sample without crashing the notebook. |

---

## Key Findings

- The SMS Spam dataset is **imbalanced** — 87% ham, 13% spam. This must be addressed before model training.
- After preprocessing, the full `CountVectorizer` vocabulary had **over 7,000 unique tokens**. With `min_df=5`, this dropped by roughly 30%, removing noise without losing meaningful words.
- **Bigrams tripled the vocabulary size** compared to unigrams (~35,000 vs ~7,000 features), confirming that N-gram models need `max_features` limits for practical use.
- Words with the highest TF-IDF scores (like `prize`, `claim`, `winner`) are almost exclusively spam vocabulary, confirming TF-IDF's usefulness for this task.
- All count-based methods **lose word order**. The sentence "not good" and "good not" produce the same unigram vector — a fundamental limitation that requires sequence models to overcome.

---

## Submitted by

**Abhishek Thakare**  
Assignment 18 — GenAI / NLP Track  
TuteDude
