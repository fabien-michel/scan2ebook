import os
import csv
from glob import glob
from cache import Cache
from book import Book
from generator import ThreadedBookGenerator


class Library:

    def __init__(self, csv_path):
        if not os.path.exists(csv_path):
            raise "{} path does not exists".format(csv_path)

        self.csv_path = csv_path
        self.cache = Cache()

    def process(self, name_filter, force):
        library = self.read()
        for book_csv in library:

            book = Book(**book_csv)

            if name_filter and name_filter.lower() not in book.name.lower():
                continue

            print("• {}".format(book))

            if force or self.cache.has_book_change(book):
                ThreadedBookGenerator(book).process()
                self.cache.store_book(book)
            # else:
                print('  No changes')

    def read(self):
        with open(self.csv_path, "r") as library_file:
            return list(csv.DictReader(library_file))

    def complete_missing_books(self):
        referenced_book_names = set(book['name'] for book in self.read())
        sourced_book_names = set(os.path.basename(os.path.normpath(name)) for name in glob('sources/*/'))
        missing_book_names = sourced_book_names - referenced_book_names
        print(missing_book_names)
        with open(self.csv_path, "a") as library_file:
            csv_writer = csv.writer(library_file)
            for new_book_name in missing_book_names:
                csv_writer.writerow((new_book_name,))
