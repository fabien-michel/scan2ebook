import os
import pickle
import base64

CACHE_DIR = b'.cache'


class Cache:

    def __init__(self):
        if not os.path.exists(CACHE_DIR):
            os.makedirs(CACHE_DIR)

    def has_book_change(self, book):
        path = self._book_cachefile(book)
        try:
            if os.path.exists(path):
                f = open(path, 'rb')
                cached_book = pickle.load(f)
                return cached_book != book
        except Exception:
            pass
        return True

    def store_book(self, book):
        path = self._book_cachefile(book)
        f = open(path, 'wb')
        pickle.dump(book, f)

    def _book_cachefile(self, book):
        if not book.name:
            raise "No book name"
        return os.path.join(CACHE_DIR, base64.b64encode(book.name.encode('ascii')))
