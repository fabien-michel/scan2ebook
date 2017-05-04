# scan2ebook
Process scanned JPGs and output PDF for ebook reader

## Requirements

 * Python 3.5
 * imagemagick 6
 
## Usage

1. Scan a book to a set of JPGs
2. Put images into a subfolder in "sources" Folder. eg: sources/My book/page_###.jpg
3. Fill line in library.csv with name "My book" and set up needed options
4. run scan2book.py

## Book processing options

### name
Required. Name of the book

### path
Optional. Indicate folder containing image. The default is to search for the book name folder intou sources folder
scan2book will fail if no valid path found

### cut_x, cut_y
Optional. Crop the image at indicated pixels (default to no crop)

### rotate
Optional. Rotate image by indicated degrees (default 0)

### flip_alternatively
Optional. Rotate 180° one page on two starting at indicated value. (default to not perform)

### quality
Optional. The image output quality (default 40)

### grayscale
Optional. If true, output in grayscale (default False)
