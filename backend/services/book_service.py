from sqlalchemy import asc, desc
from models import db, Book, Category


def _apply_sorting(query, sort_by: str, order: str):
    if sort_by == "title":
        return query.order_by(asc(Book.title) if order == "asc" else desc(Book.title))
    if sort_by == "status":
        return query.order_by(asc(Book.status) if order == "asc" else desc(Book.status))
    return query


def get_all_books(category_id: str | None, sort_by: str, order: str):
    query = db.session.query(Book).join(Category)

    if category_id:
        query = query.filter(Book.category_id == category_id)

    query = _apply_sorting(query, sort_by, order)
    return query.all()


def search_books(keyword: str, sort_by: str, order: str):
    query = (
        db.session.query(Book)
        .join(Category)
        .filter(Book.title.ilike(f"%{keyword}%"))
    )

    query = _apply_sorting(query, sort_by, order)
    return query.all()


def get_book_by_id(book_id: str):
    return (
        db.session.query(Book)
        .join(Category)
        .filter(Book.book_id == book_id)
        .first()
    )
