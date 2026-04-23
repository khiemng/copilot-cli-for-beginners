import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
import books
import book_app
from books import BookCollection


@pytest.fixture(autouse=True)
def use_temp_data_file(tmp_path, monkeypatch):
    """Use a temporary data file for each test."""
    temp_file = tmp_path / "data.json"
    temp_file.write_text("[]")
    monkeypatch.setattr(books, "DATA_FILE", str(temp_file))
    # Reset the global collection so it uses the temp file
    monkeypatch.setattr(book_app, "collection", BookCollection())


def test_add_book():
    collection = BookCollection()
    initial_count = len(collection.books)
    collection.add_book("1984", "George Orwell", 1949)
    assert len(collection.books) == initial_count + 1
    book = collection.find_book_by_title("1984")
    assert book is not None
    assert book.author == "George Orwell"
    assert book.year == 1949
    assert book.read is False

def test_mark_book_as_read():
    collection = BookCollection()
    collection.add_book("Dune", "Frank Herbert", 1965)
    result = collection.mark_as_read("Dune")
    assert result is True
    book = collection.find_book_by_title("Dune")
    assert book.read is True

def test_mark_book_as_read_invalid():
    collection = BookCollection()
    result = collection.mark_as_read("Nonexistent Book")
    assert result is False

def test_remove_book():
    collection = BookCollection()
    collection.add_book("The Hobbit", "J.R.R. Tolkien", 1937)
    result = collection.remove_book("The Hobbit")
    assert result is True
    book = collection.find_book_by_title("The Hobbit")
    assert book is None

def test_remove_book_invalid():
    collection = BookCollection()
    result = collection.remove_book("Nonexistent Book")
    assert result is False


def test_handle_mark_success(monkeypatch, capsys):
    book_app.collection.add_book("Dune", "Frank Herbert", 1965)
    monkeypatch.setattr("builtins.input", lambda _: "Dune")
    book_app.handle_mark()
    captured = capsys.readouterr()
    assert "marked as read" in captured.out
    book = book_app.collection.find_book_by_title("Dune")
    assert book.read is True


def test_handle_mark_not_found(monkeypatch, capsys):
    monkeypatch.setattr("builtins.input", lambda _: "Unknown Title")
    book_app.handle_mark()
    captured = capsys.readouterr()
    assert "not found" in captured.out


# Tests for unread filtering feature
def test_get_unread_books_returns_only_unread():
    c = BookCollection()
    c.add_book("A", "Author A", 2000)
    c.add_book("B", "Author B", 2001)
    c.mark_as_read("A")
    unread = c.get_unread_books()
    assert [b.title for b in unread] == ["B"]

def test_get_unread_books_all_read_returns_empty():
    c = BookCollection()
    c.add_book("A", "Author A", 2000)
    c.mark_as_read("A")
    assert c.get_unread_books() == []

def test_get_unread_books_no_books_returns_empty():
    c = BookCollection()
    assert c.get_unread_books() == []

def test_get_unread_books_preserves_collection():
    c = BookCollection()
    c.add_book("A", "Author A", 2000)
    before = list(c.books)
    _ = c.get_unread_books()
    assert c.books == before

def test_get_unread_books_handles_missing_read_attribute():
    c = BookCollection()
    class Minimal:
        def __init__(self, title, author, year):
            self.title = title
            self.author = author
            self.year = year
    c.books.append(Minimal("X", "Y", 1999))
    unread = c.get_unread_books()
    assert any(getattr(b, "title", None) == "X" for b in unread)

def test_handle_unread_prints_unread_books(capsys):
    book_app.collection.add_book("One", "Author 1", 2010)
    book_app.collection.add_book("Two", "Author 2", 2011)
    book_app.collection.mark_as_read("Two")
    book_app.handle_unread()
    captured = capsys.readouterr()
    # Ensure the unread title is shown and the status contains 'Unread'
    assert "One" in captured.out
    assert "Unread" in captured.out

def test_handle_unread_no_unread_prints_message(capsys):
    # No books in the collection -> should print the empty message
    book_app.handle_unread()
    captured = capsys.readouterr()
    assert "No books in your collection." in captured.out
