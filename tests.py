import pytest
from main import BooksCollector


@pytest.fixture(scope='function')
def collector():
    return BooksCollector()


class TestBooksCollector:
    NAME_MAX_LENGTH = 40
    DEFAULT_BOOK_NAME = 'Книга 1'

    @pytest.mark.parametrize('books_names',
                             (('1' * NAME_MAX_LENGTH,),
                              (DEFAULT_BOOK_NAME, DEFAULT_BOOK_NAME + '1'))
                             )
    def test_add_new_book_add_unique_books(self, collector, books_names):
        for name in books_names:
            collector.add_new_book(name)
        assert set(books_names).issubset(list(collector.books_genre.keys()))

    def test_add_new_book_add_duplicate_books(self, collector):
        name = self.DEFAULT_BOOK_NAME
        collector.add_new_book(name)
        collector.books_genre[name] = name
        book_name = collector.books_genre[name]
        collector.add_new_book(name)

        assert len(collector.books_genre) == 1
        assert book_name == collector.books_genre[name]

    @pytest.mark.parametrize('name',
                             ('',
                              '1' * (NAME_MAX_LENGTH + 1))
                             )
    def test_add_new_book_add_book_incorrect_name_length(self, collector, name):
        collector.add_new_book(name)
        assert not collector.books_genre

    @pytest.mark.parametrize('name',
                             (['name'],
                              15,
                              BooksCollector())
                             )
    def test_add_new_book_raises_error(self, collector, name):
        try:
            collector.add_new_book(name)
        except TypeError as e:
            assert isinstance(e, TypeError)

    def test_set_book_genre_set_existing_genre(self, collector):
        name = self.DEFAULT_BOOK_NAME
        collector.add_new_book(name)
        genre = collector.genre[0]
        collector.set_book_genre(name, genre)
        assert collector.books_genre[name] == genre

    def test_set_book_genre_set_not_existing_genre(self, collector):
        name = self.DEFAULT_BOOK_NAME
        collector.add_new_book(name)
        genre_before_set = collector.books_genre[name]
        genre = collector.genre[0] + 'random'
        collector.set_book_genre(name, genre)
        assert collector.books_genre[name] == genre_before_set

    def test_get_book_genre_name_exists(self, collector):
        name = self.DEFAULT_BOOK_NAME
        collector.add_new_book(name)
        genre = collector.books_genre[name]
        assert genre == collector.get_book_genre(name)

    def test_get_book_genre_name_not_exists(self, collector):
        name = self.DEFAULT_BOOK_NAME + 'random'
        assert collector.get_book_genre(name) is None

    @pytest.mark.parametrize('books_names',
                             ((), (DEFAULT_BOOK_NAME, DEFAULT_BOOK_NAME + '1')))
    def test_get_books_with_specific_genre_returns_books_when_genre_is_valid(
            self,
            collector,
            books_names):
        genre = collector.genre[0]
        for name in books_names:
            collector.add_new_book(name)
            collector.set_book_genre(name, genre)
        assert sorted(collector.get_books_with_specific_genre(genre)) == sorted(books_names)

    @pytest.mark.parametrize('books_names',
                             ((), (DEFAULT_BOOK_NAME, DEFAULT_BOOK_NAME + '1')))
    def test_get_books_genre_returns_books_genre(self, collector, books_names):
        for name in books_names:
            collector.add_new_book(name)
        assert collector.books_genre == collector.get_books_genre()

    def test_get_books_for_children_return_book_in_age_rating(self, collector):
        name = self.DEFAULT_BOOK_NAME
        collector.add_new_book(name)
        genre = set(collector.genre)
        genre_age_rating = set(collector.genre_age_rating)
        exists_genre = list(genre.difference(genre_age_rating))[0]
        collector.set_book_genre(name, exists_genre)

        collector.add_new_book(name + '1')
        collector.set_book_genre(name + '1', collector.genre_age_rating[0])
        assert name in collector.get_books_for_children()
        assert name + '1' not in collector.get_books_for_children()

    @pytest.mark.parametrize('names',
                             ((DEFAULT_BOOK_NAME,),
                              (DEFAULT_BOOK_NAME, DEFAULT_BOOK_NAME + '1'))
                             )
    def test_add_book_in_favorites_add_unique_books(self, collector, names):
        for name in names:
            collector.add_new_book(name)
            collector.add_book_in_favorites(name)
        assert set(names).issubset(collector.favorites)

    def test_delete_book_from_favorites_delete_one_book(self, collector):
        name = self.DEFAULT_BOOK_NAME
        collector.add_new_book(name)
        collector.add_book_in_favorites(name)
        collector.delete_book_from_favorites(name)
        assert name not in collector.favorites

    def test_get_list_of_favorites_books_return_favorites_books(self, collector):
        name = self.DEFAULT_BOOK_NAME
        collector.add_new_book(name)
        collector.add_book_in_favorites(name)
        assert collector.favorites == collector.get_list_of_favorites_books()