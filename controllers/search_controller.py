"""
Search Controller - provides search and sort utilities for books
Returns lists of dicts compatible with views (keys: book_id, title, author, category,
status, available_copies, total_copies, description, detailed_info)
"""
from models.book import Book

class SearchController:
    @staticmethod
    def _book_to_dict(b):
        return {
            "book_id": b.book_id,
            "title": b.title,
            "author": b.author,
            "category": b.category_name or "",
            "status": b.status,
            "available_copies": b.available_quantity,
            "total_copies": b.total_quantity,
            "description": b.description,
            "detailed_info": b.detailed_info
        }

    @staticmethod
    def search_books(keyword=None, search_by="title"):
        """
        Search books by keyword and field.
        - keyword: search term (substring match, case-insensitive)
        - search_by: one of "title", "author", "category"
        Returns list of dicts.
        """
        kw = (keyword or "").strip().lower()
        books = Book.get_all_books()
        results = []

        for b in books:
            title = (b.title or "").lower()
            author = (b.author or "").lower()
            category = (b.category_name or "").lower() if b.category_name else ""

            if not kw:
                match = True
            elif search_by == "title":
                match = kw in title
            elif search_by == "author":
                match = kw in author
            elif search_by == "category":
                match = kw in category
            else:
                # fallback: check title and author
                match = kw in title or kw in author

            if match:
                results.append(SearchController._book_to_dict(b))

        return results

    @staticmethod
    def sort_books(books, sort_by='title_asc'):
        """
        Sort a list of book-dicts produced by search_books/display.
        - sort_by options: 'title_asc', 'title_desc', 'author_asc', 'author_desc', 'status'
        """
        reverse = False
        key = lambda x: (x.get('title') or "").lower()

        if sort_by == 'title_desc':
            reverse = True
            key = lambda x: (x.get('title') or "").lower()
        elif sort_by == 'author_asc':
            key = lambda x: (x.get('author') or "").lower()
        elif sort_by == 'author_desc':
            reverse = True
            key = lambda x: (x.get('author') or "").lower()
        elif sort_by == 'status':
            # Put Available first
            key = lambda x: (0 if (x.get('status') == 'Available') else 1, (x.get('title') or "").lower())

        try:
            return sorted(books, key=key, reverse=reverse)
        except Exception:
            return books

