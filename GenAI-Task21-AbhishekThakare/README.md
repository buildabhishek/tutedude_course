# Assignment 21: LangChain Document Loaders & Text Splitters

## Objective

This assignment demonstrates document loading and text splitting using LangChain. It covers TXT, CSV, PDF, directory, and public web content, followed by length-based, recursive, and structure-based splitting.

No vector database or LLM call is used.

## Project Structure

```text
Assignment-21/
├── assignment21.ipynb
├── README.md
├── requirements.txt
└── data/
    ├── notes.txt
    ├── data.csv
    └── company_overview.pdf
```

## Input Files

- `notes.txt` - sample notes used for text loading and splitting.
- `data.csv` - sample employee data used with CSVLoader.
- `company_overview.pdf` - a small two-page PDF used with PyPDFLoader.

## Tasks Completed

1. TextLoader
2. CSVLoader
3. PyPDFLoader
4. DirectoryLoader
5. WebBaseLoader
6. Why text splitting is required
7. CharacterTextSplitter
8. RecursiveCharacterTextSplitter and comparison
9. Document structure-based splitting
10. Semantic chunking concepts
11. Unified preprocessing pipeline
12. Observations and insights

## Libraries Used

- LangChain
- langchain-community
- langchain-text-splitters
- PyPDF
- Beautiful Soup

## How to Run

Create and activate a Python virtual environment if required.

Install dependencies:

```bash
pip install -r requirements.txt
```

Open Jupyter Notebook or VS Code and run:

```text
assignment21.ipynb
```

Run all cells from top to bottom.

Task 5 and the web URL test in Task 11 require an active internet connection.

## Experiments Performed

- Loaded TXT, CSV, PDF, directory, and web content.
- Inspected LangChain Document content and metadata.
- Compared CharacterTextSplitter with RecursiveCharacterTextSplitter on the same text.
- Inspected chunk counts and chunk lengths.
- Preserved Markdown heading information using MarkdownHeaderTextSplitter.
- Combined document loading and recursive splitting in one function.

## Key Observations

Different source formats need suitable loaders, but LangChain returns Document objects with page_content and metadata. Loading and splitting are separate preprocessing steps. Recursive splitting is useful when text contains sections larger than one configured separator can handle.

## Challenges Faced

No generic challenge has been added. Actual installation, file path, or network issues should be documented only if they occur during execution.

## Learning Outcomes

I learned how LangChain loads different document formats and how text splitters prepare loaded content as smaller chunks. I also learned the difference between fixed-separator splitting, recursive splitting, and structure-aware splitting.

## Submitted By

Abhishek Thakare
