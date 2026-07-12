# Assignment 19 - Word2Vec Text Embeddings

## Dataset

* Dataset Name: SMS Spam Collection Dataset
* Dataset Source: UCI Machine Learning Repository
* Kaggle Link:
  https://www.kaggle.com/datasets/uciml/sms-spam-collection-dataset

---

## Tasks Completed

* Understanding Word Embeddings
* Word2Vec Overview
* CBOW Architecture
* Skip-Gram Architecture
* Neural Network Intuition
* Dataset Preprocessing
* Training CBOW Model
* Training Skip-Gram Model
* Vocabulary Analysis
* Word Similarity Search
* Vector Arithmetic
* PCA Visualization
* Evaluation and Insights

---

## Libraries Used

* Pandas
* NumPy
* NLTK
* Gensim
* Scikit-Learn
* Matplotlib

---

## How To Run

1. Install dependencies:

```bash
pip install pandas numpy nltk gensim scikit-learn matplotlib
```

2. Place `spam.csv` inside the project folder.

3. Open `Assignment_19_Word2Vec.ipynb`.

4. Run all notebook cells sequentially.

---

## Learning Outcomes

* Learned the concept of distributed word representations.
* Understood the limitations of One-Hot Encoding and Bag of Words.
* Implemented Word2Vec using Gensim.
* Trained CBOW and Skip-Gram architectures.
* Retrieved semantically similar words.
* Explored vector arithmetic.
* Visualized embeddings using PCA.

---

## Challenges Faced

* Understanding how Word2Vec learns semantic relationships.
* Comparing CBOW and Skip-Gram architectures.
* Interpreting high-dimensional embedding vectors.
* Visualizing embeddings in two dimensions.

---

## Key Findings

* Word2Vec generated dense vector representations for words in the SMS dataset.
* Similar words were grouped together in embedding space.
* CBOW trained faster than Skip-Gram.
* Skip-Gram captured richer relationships for less frequent words.
* PCA visualization showed clustering of related terms.

---

## Submitted By

Abhishek Thakare
