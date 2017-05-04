import csv
import argparse
from book import Book
from generator import ThreadedBookGenerator
from cache import Cache


parser = argparse.ArgumentParser(description='Convert scanned JPGs to PDF for ebook reader')
parser.add_argument('-f', '--force', action='store_true',
                    help='Force process book')
parser.add_argument('-n', '--name', help='Filter book name')
parser.add_argument('-l', '--library', default='library.csv', help='Library CSV file')
args = parser.parse_args()


cache = Cache()
library_file = open(args.library, "r")
library = csv.DictReader(library_file)


for book_csv in library:

    book = Book(**book_csv)

    if args.name and args.name.lower() not in book.name.lower():
        continue

    print("• {}".format(book))

    if args.force or cache.has_book_change(book):
        ThreadedBookGenerator(book).process()
        cache.store_book(book)
    else:
        print('  No changes')
