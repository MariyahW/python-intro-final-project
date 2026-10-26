# Open Library Explorer CLI

A Python command-line tool that interacts with the Open Library API to search for books by author or subject, format the results, and export cleaned datasets to a CSV file.

## API

This project uses the [Open Library Search API](https://openlibrary.org/developers/api) (`/search.json`).

## Installation

1. Clone this repository:
```bash
git clone https://github.com/MariyahW/python-intro-final-project.git
cd python-intro-final-project

```


2. Create and activate a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate      # macOS/Linux
# .venv\Scripts\activate       # Windows

```


3. Install dependencies:
```bash
pip install -r requirements.txt

```



## Usage

Start the program by running the main script in your terminal:

```bash
python main.py

```

When the program runs, you will be greeted with a menu asking if you want to search by author or subject. After making a selection, you will be prompted to enter your search term and the maximum number of results you want returned. The CLI will fetch the data, print a cleanly formatted and numbered list of books to your terminal, and finally ask if you would like to export the results to a CSV file.

## CLI Interactions

* **Search by Author** — Enter `1` to search the database for all books written by a specific author (e.g., "Tolkien").
* **Search by Subject** — Enter `2` to search for books falling under a specific genre or topic (e.g., "science fiction").
* **Result Limiter** — Controls the size of the API response by asking for a maximum number of returns (capped at 100 to prevent terminal overload).
* **CSV Data Export** — After viewing results, type `y` to instantly generate a `books_export.csv` file containing the structured data.

## Extension Track: Option B (Data Pipeline)

This project implements the Data Pipeline extension. Because the Open Library API contains decades of crowdsourced data, the raw JSON response is often messy or incomplete.

**Data Cleaning Decisions:**

* **Author Names:** The API returns `author_name` as a list of strings (since books can have multiple authors). The cleaning function extracts only the first author (`authors_list[0]`) to ensure the CSV column remains a clean, single-string value rather than a Python list structure.
* **Missing Values:** Many older or obscure books lack page counts or publication years. The `process_data` function uses Python's `.get()` method with fallback default values (like `"N/A"` or `"Unknown Title"`) so that missing data doesn't crash the program and empty CSV cells are clearly labeled.
* **Field Normalization:** Extracted only the core fields (`title`, `author`, `year`, `pages`) to create a structured, predictable format for the `csv.DictWriter` to process.