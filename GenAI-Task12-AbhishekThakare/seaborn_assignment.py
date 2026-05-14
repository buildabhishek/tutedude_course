# This program demonstrates Seaborn visualizations

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


# Sample Dataset

data = {
    "Student": ["Amit", "Neha", "Rahul", "Sneha", "Pooja", "Karan"],
    "Marks": [78, 85, 90, 66, 72, 88],
    "StudyHours": [2, 3, 5, 1, 2, 4],
    "Gender": ["Male", "Female", "Male", "Female", "Female", "Male"],
    "Subject": ["Math", "Science", "Math", "Science", "Math", "Science"]
}

df = pd.DataFrame(data)


# Task 1: Relational Plot

sns.relplot(
    data=df,
    x="StudyHours",
    y="Marks",
    hue="Gender"
)

plt.title("Relational Plot")

plt.show()


sns.scatterplot(
    data=df,
    x="StudyHours",
    y="Marks",
    hue="Gender"
)

plt.title("Scatter Plot")

plt.show()


# Task 2: Line Plot as Scatter & Facet

sns.lineplot(
    data=df,
    x="StudyHours",
    y="Marks"
)

plt.title("Line Plot")

plt.show()


sns.relplot(
    data=df,
    x="StudyHours",
    y="Marks",
    col="Subject"
)

plt.show()


# Task 3: Distribution Plots

sns.histplot(
    data=df,
    x="Marks"
)

plt.title("Histogram")

plt.show()


sns.kdeplot(
    data=df,
    x="Marks",
    fill=True
)

plt.title("KDE Plot")

plt.show()


sns.histplot(
    data=df,
    x="Marks",
    kde=True
)

plt.title("Histogram with KDE")

plt.show()


# Task 4: Bivariate Distribution Plots

sns.kdeplot(
    data=df,
    x="StudyHours",
    y="Marks",
    fill=True
)

plt.title("Bivariate KDE Plot")

plt.show()


sns.histplot(
    data=df,
    x="StudyHours",
    y="Marks"
)

plt.title("Bivariate Histogram")

plt.show()


# Task 5: Matrix Plots

sns.pairplot(df)

plt.show()


correlation = df[["Marks", "StudyHours"]].corr()

sns.heatmap(
    correlation,
    annot=True
)

plt.title("Correlation Heatmap")

plt.show()


# Task 6: Categorical Plots

sns.barplot(
    data=df,
    x="Subject",
    y="Marks"
)

plt.title("Bar Plot")

plt.show()


sns.boxplot(
    data=df,
    x="Subject",
    y="Marks"
)

plt.title("Box Plot")

plt.show()


sns.violinplot(
    data=df,
    x="Subject",
    y="Marks"
)

plt.title("Violin Plot")

plt.show()


sns.countplot(
    data=df,
    x="Gender"
)

plt.title("Count Plot")

plt.show()


# Task 7: Regression Plots

sns.regplot(
    data=df,
    x="StudyHours",
    y="Marks"
)

plt.title("Regression Plot")

plt.show()


sns.lmplot(
    data=df,
    x="StudyHours",
    y="Marks",
    hue="Gender"
)

plt.show()


# Task 8: Multi-Plots & Figure-Level Plots

g = sns.FacetGrid(
    df,
    col="Gender"
)

g.map(
    plt.scatter,
    "StudyHours",
    "Marks"
)

plt.show()


sns.relplot(
    data=df,
    x="StudyHours",
    y="Marks",
    hue="Gender"
)

plt.show()


sns.catplot(
    data=df,
    x="Subject",
    y="Marks",
    kind="bar"
)

plt.show()


sns.displot(
    data=df,
    x="Marks",
    kde=True
)

plt.show()
