from flask import Blueprint, render_template, request, abort
from services.book_service import (
    get_all_books,
    search_books,
    get_book_by_id,
)
from models import Category

books_bp = Blueprint("books", __name__, url_prefix="/books")


@books_bp.route("", methods=["GET"])
def view_books():
    category_id = request.args.get("category")
    sort_by = request.args.get("sort", "title")
    order = request.args.get("order", "asc")

    books = get_all_books(category_id, sort_by, order)
    categories = Category.query.all()

    return render_template(
        "books/book_list.html",
        books=books,
        categories=categories,
        selected_category=category_id,
        sort_by=sort_by,
        order=order,
    )


@books_bp.route("/search", methods=["GET"])
def search():
    keyword = request.args.get("keyword", "").strip()
    sort_by = request.args.get("sort", "title")
    order = request.args.get("order", "asc")

    if not keyword:
        return render_template(
            "books/search_results.html",
            books=[],
            keyword=keyword,
        )

    books = search_books(keyword, sort_by, order)

    return render_template(
        "books/search_results.html",
        books=books,
        keyword=keyword,
        sort_by=sort_by,
        order=order,
    )


@books_bp.route("/<string:book_id>", methods=["GET"])
def book_detail(book_id):
    book = get_book_by_id(book_id)

    if not book:
        abort(404)

    return render_template(
        "books/book_detail.html",
        book=book,
    )
