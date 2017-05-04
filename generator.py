import os
import img2pdf
import threading
import time
from wand.image import Image

DEST_PATH = 'books'
MAX_THREAD = 5


class BookGenerator:

    def __init__(self, book):
        self.book = book
        self.page_processor = BookPageProcessor(self.book)
        try:
            os.makedirs(DEST_PATH)
        except:
            pass

    def process(self):

        start = time.time()

        for page_index, page_file in enumerate(self.book.pages):
            # page_index += 1
            print('  {}'.format(page_file))
            self.process_page(page_file, page_index)

        # Combine to PDF
        self.combine_to_pdf()

        end = time.time()
        print('  {}s'.format(end - start))

    def process_page(self, page_file, page_index):
        self.page_processor.process(page_file, page_index)

    def combine_to_pdf(self):
        print('  Building PDF')
        with open(os.path.join(DEST_PATH, '{}.pdf'.format(self.book.name)), "wb") as f:
            f.write(img2pdf.convert(
                [os.path.join(self.book.tmp_path, page_file) for page_file in self.book.pages]
            ))


class BookPageProcessor:
    def __init__(self, book):
        self.book = book

    def process(self, page_file, page_index):
        with Image(filename=os.path.join(self.book.path, page_file)) as source_img:
            with source_img.clone() as page:
                # Crop pages
                page.crop(0, 0, self.book.cut_x or page.width, self.book.cut_y or page.height)
                # Reduce dimensions
                page.transform(resize='758x1024>')
                # Set to B&W
                if self.book.grayscale:
                    page.type = 'grayscalematte'
                # Rotation
                if self.book.rotate:
                    page.rotate(self.book.rotate)
                # Flip one page on two
                if self.book.flip_alternatively:
                    if (page_index >= self.book.flip_alternatively and
                            (page_index - self.book.flip_alternatively) % 2 == 0):
                        page.rotate(180)
                # Change jpg quality
                page.compression_quality = self.book.quality

                # Save image in temp path
                page.save(filename=os.path.join(self.book.tmp_path, page_file))


class BookPageProcessorThread(threading.Thread):
    def __init__(self, book, page_file, page_index):
        threading.Thread.__init__(self)
        self.book = book
        self.page_file = page_file
        self.page_index = page_index

    def run(self):
        BookPageProcessor(self.book).process(self.page_file, self.page_index)


class ThreadedBookGenerator(BookGenerator):

    def process_page(self, page, page_index):
        while threading.active_count() >= MAX_THREAD:
            time.sleep(0.1)
        BookPageProcessorThread(self.book, page, page_index).start()

    def combine_to_pdf(self):
        # Waiting to all pages been processed
        while threading.active_count() > 1:
            time.sleep(0.1)
        return super(ThreadedBookGenerator, self).combine_to_pdf()
