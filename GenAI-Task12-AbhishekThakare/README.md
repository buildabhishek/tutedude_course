# GenAI Assignment 12 - Seaborn Visualizations

## Student Information

**Name:** Abhishek Thakare

---

# Assignment Overview

This assignment focuses on Exploratory Data Analysis (EDA) using Seaborn. The objective is to understand different types of visualizations and when they should be used for analyzing relationships, distributions, categories, correlations, and patterns in data.

---

# Dataset Used

**Dataset Name:** Titanic Dataset

**Source:** Kaggle

**Dataset Link:**
https://www.kaggle.com/datasets/yasserh/titanic-dataset

**Dataset Description:**
The Titanic dataset contains information about passengers aboard the Titanic, including demographic details, ticket information, passenger class, fare, age, and survival status.

---

# Libraries Used

- Pandas
- Seaborn
- Matplotlib

---

# Data Exploration Performed

Before creating visualizations, the dataset was explored using:

- `df.head()`
- `df.info()`
- `df.describe()`
- `df.shape`
- `df.columns`
- Missing value analysis using `df.isnull().sum()`

Basic cleaning was performed to handle missing values before plotting.

---

# Tasks Completed

## Task 1: Relational Plots

- Relational Plot (`relplot`)
- Scatter Plot
- Relationship between numerical variables using categorical grouping

## Task 2: Line Plot and Faceting

- Line Plot
- Faceted Line Plot using categorical variables

## Task 3: Distribution Plots

- Histogram
- KDE Plot
- Rug Plot
- Histogram + KDE + Rug Plot

## Task 4: Bivariate Distribution Plots

- Bivariate Histogram
- Bivariate KDE Plot

## Task 5: Matrix Plots

- Pair Plot
- Correlation Heatmap

## Task 6: Categorical Plots

- Bar Plot
- Box Plot
- Violin Plot
- Count Plot

## Task 7: Regression Plots

- Regression Plot (`regplot`)
- Linear Model Plot (`lmplot`)

## Task 8: Multi-Plots and Figure-Level Plots

- FacetGrid
- CatPlot
- DisPlot

---

# Learning Outcomes

Through this assignment, I learned:

- How to visualize relationships between numerical variables.
- How distribution plots help understand data spread and skewness.
- How to identify outliers using boxplots and violin plots.
- How heatmaps help analyze feature correlations.
- How figure-level plots simplify multi-category analysis.
- The difference between axes-level and figure-level Seaborn plots.

---

# Key Observations

- Most passengers were between 20 and 40 years of age.
- Fare distribution was highly right-skewed.
- Several fare outliers were present in the dataset.
- Passenger class had a noticeable impact on fare values.
- Correlation between numerical features was generally weak to moderate.
- Distribution plots helped identify missing value patterns and unusual observations.

---

# Files Included

- `seaborn_assignment.ipynb`
- `Titanic-Dataset.csv`
- `README.md`

---

# How to Run

## Install Required Libraries

```bash
pip install pandas seaborn matplotlib
```

## Run Jupyter Notebook

```bash
jupyter notebook
```

Open:

```text
seaborn_assignment.ipynb
```

and run all cells sequentially.

---

# Submission

Assignment 12 - Seaborn (Relational, Distribution, Categorical & Multi-Plots)
