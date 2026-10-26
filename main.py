import requests
import os

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
            limit = int(
                input(
                    "What is the maximum amount of returns you would like? (At most 200) "
                )
            )
            if limit > 200:
                limit = 100
            params = {"limit": limit, "author": author}
            return params, "author"
        case "2":
            subject = input("Which subject would you like to search for? ")
            limit = int(
                input(
                    "What is the maximum amount of returns you would like? (At most 200) "
                )
            )
            if limit > 200:
                limit = 100
            params = {"limit": limit, "q": subject}
            return params, "subject"
        case _:
            print("Please input a valid option.")
            create()


def main():
    optA, term = create()
    data = fetch_data(optA)
    if not data:
        return

    records = process_data(data)
    display_results(records)


if __name__ == "__main__":
    main()
