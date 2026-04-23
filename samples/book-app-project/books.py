import json
from dataclasses import dataclass, asdict
from typing import List, Optional

DATA_FILE = "data.json"


@dataclass
class Book:
    title: str
    author: str
    year: int
    read: bool = False


class BookCollection:
    def __init__(self):
        self.books: List[Book] = []
        self.load_books()

    def load_books(self):
        """Load books from the JSON file if it exists."""
        try:
            with open(DATA_FILE, "r") as f:
                data = json.load(f)
                self.books = [Book(**b) for b in data]
        except FileNotFoundError:
            self.books = []
        except json.JSONDecodeError:
            print("Warning: data.json is corrupted. Starting with empty collection.")
            self.books = []

    def save_books(self):
        """Save the current book collection to JSON."""
        with open(DATA_FILE, "w") as f:
            json.dump([asdict(b) for b in self.books], f, indent=2)

    def add_book(self, title: str, author: str, year: int) -> Book:
        title = title.strip()
        if not title:
            raise ValueError("title cannot be empty")
        book = Book(title=title, author=author, year=year)
        self.books.append(book)
        self.save_books()
        return book

    def list_books(self) -> List[Book]:
        return self.books

    def get_unread_books(self) -> List[Book]:
        """Return all books not marked as read."""
        return [b for b in self.books if not getattr(b, "read", False)]

    def find_book_by_title(self, title: str) -> Optional[Book]:
        for book in self.books:
            if book.title.lower() == title.lower():
                return book
        return None

    def mark_as_read(self, title: str) -> bool:
        book = self.find_book_by_title(title)
        if book:
            book.read = True
            self.save_books()
            return True
        return False

    def remove_book(self, title: str) -> bool:
        """Remove a book by title."""
        book = self.find_book_by_title(title)
        if book:
            self.books.remove(book)
            self.save_books()
            return True
        return False

    def find_by_author(self, author: str) -> List[Book]:
        """Find all books by a given author (supports partial, case-insensitive matches)."""
        if not author:
            return []
        query = author.strip().lower()
        return [b for b in self.books if query in b.author.lower()]

    def list_by_year(self, start: int, end: int) -> List[Book]:
        """Return books published between start and end years (inclusive).

        Raises:
            TypeError: if start or end are not integers.
            ValueError: if start > end.
        """
        if not isinstance(start, int) or not isinstance(end, int):
            raise TypeError("start and end must be integers")
        if start > end:
            raise ValueError("start must be <= end")
        return [b for b in self.books if start <= b.year <= end]
