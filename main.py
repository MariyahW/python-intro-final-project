import requests
import os
import csv

# from dotenv import load_dotenv

API_URL = "https://openlibrary.org/search.json"  # Replace with your chosen API endpoint


def fetch_data(q_params):
    """Fetch data from the API. Returns the raw JSON response, or an empty list on failure."""
    try:
        response = requests.get(API_URL, params=q_params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error: could not fetch data. {e}")
        return []


def process_data(data):
    """Extract and transform the fields you need. Returns a list of dictionaries."""
    books = data.get("docs", [])
    cleanBooks = []
    for book in books:
        authors_list = book.get("author_name", ["Unknown Author"])
        prim_Author = authors_list[0]

        clean_book = {
            "title": book.get("title", "Unknown Title"),
            "author": prim_Author,
            "year": book.get("first_publish_year", "N/A"),
            "pages": book.get("number_of_pages_median", "N/A"),
            "key": book.get("key", ""),
        }
        cleanBooks.append(clean_book)
    return cleanBooks


def display_results(results):
    """Print results to the terminal in a readable format."""
    if not results:
        print("No records found")
        return

    print(f"\n--- Found {len(results)} Results ---")

    for index, book in enumerate(results, start=1):
        title = book.get("title")
        author = book.get("author")
        year = book.get("year")
        pages = book.get("pages")

        print(f"{index}. {title} by {author} (Published: {year}, Pages: {pages})")

    print("-" * 30)


def create():
    print(f"====++++++++++=====")
    print(f"Would you like to search by author? Enter 1")
    print(f"Search by subject? Enter 2")
    # print(f"Exit the program? Enter 3")
    optionA = input(":   ")

    match optionA:
        case "1":
            author = input("Which author would you like to search for? ")
            try:
                limit = int(
                    input(
                        "What is the maximum amount of returns you would like? (At most 200) "
                    )
                )
            except:
                limit = 100
            if limit > 200:
                limit = 100
            params = {"limit": limit, "author": author}
            return params, "author"
        case "2":
            subject = input("Which subject would you like to search for? ")
            try:
                limit = int(
                    input(
                        "What is the maximum amount of returns you would like? (At most 200) "
                    )
                )
            except:
                limit = 100

            if limit > 200:
                limit = 100
            params = {"limit": limit, "q": subject}
            return params, "subject"
        case _:
            print("Please input a valid option.")
            return create()


def export_CSV(records, filename="csv_files/books_export.csv"):
    if not records:
        print("No Records Found")
        return
    fields = records[0].keys()
    try:
        with open(filename, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=fields)
            writer.writeheader()
            writer.writerows(records)
        print(f"\nSuccess! Cleaned data exported to {filename}")
    except IOError as e:
        print(f"\nError saving to CSV: {e}")


def main():
    optA, term = create()
    data = fetch_data(optA)
    if not data:
        return

    records = process_data(data)
    display_results(records)

    # Option B: The CSV Export prompt
    export_choice = input(
        "\nWould you like to export these results to a CSV file? (y/n): "
    )
    if export_choice.lower().strip() == "y":
        export_CSV(records, f"csv_files/{term}_book_export.csv")

    print("\nThanks for using the Open Library Explorer!")


if __name__ == "__main__":
    main()
