from typing import Any, List, Optional, Tuple
from datetime import datetime


def print_menu() -> None:
    """Display the main menu."""
    print("\n📚 Book Collection App")
    print("1. Add a book")
    print("2. List books")
    print("3. Mark book as read")
    print("4. Remove a book")
    print("5. Exit")


def get_user_choice() -> int:
    """Prompt the user until a valid menu choice (1-5) is entered.

    Returns:
        int: A number between 1 and 5. Returns 5 on interrupt (Exit).
    """
    while True:
        try:
            choice_str = input("Choose an option (1-5): ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            return 5

        if not choice_str:
            print("Please enter a choice (1-5).")
            continue

        # Accept numeric input like +1 or -1, and reject non-numeric entries such as "1.0" or "one"
        try:
            choice = int(choice_str)
        except ValueError:
            print("Invalid input. Enter a number between 1 and 5.")
            continue

        if 1 <= choice <= 5:
            return choice

        print("Choice out of range. Enter a number between 1 and 5.")


def get_book_details() -> Tuple[Optional[str], Optional[str], Optional[int]]:
    """Prompt interactively for a book's title, author, and optional publication year.

    Behavior:
    - Prompts the user for title and author; both must be non-empty strings.
    - Prompts for publication year which is optional: the user may leave it blank to store None.
    - Validates that a provided year is an integer and lies between 1 and (current_year + 1).
    - Catches EOFError and KeyboardInterrupt during any prompt and treats that as a cancellation.

    Returns:
        Tuple[Optional[str], Optional[str], Optional[int]]:
            - (title, author, year) when the user completes all prompts successfully.
              title and author are non-empty strings; year is an int or None if omitted.
            - (None, None, None) when the user cancels (EOF/KeyboardInterrupt) or if validation
              ultimately results in missing required fields. This sentinel signals callers to
              abort saving or further processing of the book record.

    Side effects:
    - Reads from stdin using input() and writes prompts/messages to stdout via print().

    Notes:
    - Calling code should treat any None return as a user cancellation and avoid persisting
      partial/invalid records.
    """
    try:
        while True:
            title = input("Enter book title: ").strip()
            if title:
                break
            print("Title cannot be empty.")
    except (EOFError, KeyboardInterrupt):
        print()
        return None, None, None

    try:
        while True:
            author = input("Enter author: ").strip()
            if author:
                break
            print("Author cannot be empty.")
    except (EOFError, KeyboardInterrupt):
        print()
        return None, None, None

    current_year = datetime.now().year
    try:
        while True:
            year_input = input("Enter publication year (optional): ").strip()
            if year_input == "":
                year = None
                break
            try:
                year = int(year_input)
                if 0 < year <= current_year + 1:
                    break
                print(f"Please enter a realistic year (1-{current_year + 1}) or leave blank.")
            except ValueError:
                print("Invalid year. Enter a number or leave blank.")
    except (EOFError, KeyboardInterrupt):
        print()
        return None, None, None

    # Final guard: ensure title and author are non-empty; if not, treat as cancellation
    if not title or not author:
        return None, None, None

    return title, author, year


def print_books(books: List[Any]) -> None:
    """Print a list of books. Handles missing attributes gracefully."""
    if not books:
        print("No books in your collection.")
        return

    print("\nYour Books:")
    for index, book in enumerate(books, start=1):
        year = getattr(book, "year", None)
        year_str = str(year) if year is not None else "Unknown"
        read_attr = getattr(book, "read", False)
        status = "✅ Read" if read_attr else "📖 Unread"
        title = getattr(book, "title", "<Untitled>")
        author = getattr(book, "author", "<Unknown>")
        print(f"{index}. {title} by {author} ({year_str}) - {status}")
