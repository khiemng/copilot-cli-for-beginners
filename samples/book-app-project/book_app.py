import sys
from books import BookCollection
from utils import print_books

# Global collection instance
collection: BookCollection = BookCollection()




def handle_list() -> None:
    books = collection.list_books()
    print_books(books)

def handle_unread() -> None:
    books = collection.get_unread_books()
    print_books(books)


def handle_add() -> None:
    print("\nAdd a New Book\n")

    title = input("Title: ").strip()
    author = input("Author: ").strip()
    year_str = input("Year: ").strip()

    try:
        year = int(year_str) if year_str else 0
        collection.add_book(title, author, year)
        print("\nBook added successfully.\n")
    except ValueError as e:
        print(f"\nError: {e}\n")


def handle_remove() -> None:
    print("\nRemove a Book\n")

    title = input("Enter the title of the book to remove: ").strip()
    collection.remove_book(title)

    print("\nBook removed if it existed.\n")


def handle_find() -> None:
    print("\nFind Books by Author\n")

    author = input("Author name: ").strip()
    books = collection.find_by_author(author)

    print_books(books)


def handle_mark() -> None:
    print("\nMark a Book as Read\n")

    title = input("Enter the title of the book to mark as read: ").strip()
    success = collection.mark_as_read(title)

    if success:
        print(f"\n\"{title}\" marked as read.\n")
    else:
        print(f"\nBook \"{title}\" not found.\n")


def show_help() -> None:
    print("""
Book Collection Helper

Commands:
  list     - Show all books
  unread   - Show unread books
  add      - Add a new book
  remove   - Remove a book by title
  find     - Find books by author
  mark     - Mark a book as read
  help     - Show this help message
""")


def main() -> None:
    if len(sys.argv) < 2:
        show_help()
        return

    command = sys.argv[1].lower()

    commands = {
        "list": handle_list,
        "unread": handle_unread,
        "add": handle_add,
        "remove": handle_remove,
        "find": handle_find,
        "mark": handle_mark,
        "help": show_help,
    }

    handler = commands.get(command)
    if handler:
        handler()
    else:
        print("Unknown command.\n")
        show_help()


if __name__ == "__main__":
    main()
