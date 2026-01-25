from controllers.search_controller import SearchController

def test_search_book():
    results = SearchController.search_books(keyword="Library")
    assert isinstance(results, list)

def test_sort_books():
    results = SearchController.search_books(sort_by="title")
    assert results == sorted(results, key=lambda x: x["title"])
