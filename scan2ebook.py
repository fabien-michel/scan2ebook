import argparse
from library import Library


parser = argparse.ArgumentParser(description='Convert scanned JPGs to PDF for ebook reader')
parser.add_argument('-f', '--force', action='store_true',
                    help='Force process book')
parser.add_argument('-n', '--name', help='Filter book name')
parser.add_argument('-l', '--library', default='library.csv', help='Library CSV file')
parser.add_argument('-c', '--complete-new', action='store_true', help='Auto-add missing books in library CSV file')
args = parser.parse_args()


library = Library(args.library)
if args.complete_new:
    library.complete_missing_books()
else:
    library.process(args.name, args.force)
