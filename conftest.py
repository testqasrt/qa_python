import pytest
from main import BooksCollector


@pytest.fixture(scope='function')
def collector():
    return BooksCollector()
