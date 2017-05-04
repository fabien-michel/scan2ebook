import os


class Book:

    ARGS = {
        'name': (str, ''),
        'path': (str, ''),
        'cut_x': (int, 0),
        'cut_y': (int, 0),
        'rotate': (int, 0),
        'flip_alternatively': (int, 0),
        'quality': (int, 40),
        'grayscale': (bool, False),
    }

    def __init__(self, *args, **kwargs):

        for arg_name, arg_attributes in self.ARGS.items():
            value = arg_attributes[1]

            if arg_name in kwargs and kwargs[arg_name]:
                value = kwargs[arg_name]

                if arg_attributes[0] == int:
                    try:
                        value = int(value)
                    except:
                        print('Int convetion failed for {} parameter. Using default : {}'.format(arg_name, value))

                if arg_attributes[0] == bool:
                    value = bool(value)

            setattr(self, arg_name, value)

        if not self.name:
            raise Exception('No name provided for the book')
        if not self.path:
            self.path = 'sources/{}'.format(self.name)
        if not os.path.exists(self.path):
            raise Exception("Path {} not exists".format(self.path))

    @classmethod
    def from_csv(book_csv):
        return Book(**book_csv)

    @property
    def tmp_path(self):
        _tmp_path = self.path.replace('sources', 'temp')
        if not os.path.exists(_tmp_path):
            os.makedirs(_tmp_path)
        return _tmp_path

    def pages_in_dir(self, temp_dir=False):
        pages_path = self.tmp_path if temp_dir else self.path
        return [file for file in os.listdir(pages_path) if file.endswith('.jpg')]

    @property
    def pages(self):
        if not hasattr(self, '_pages'):
            self._pages = self.pages_in_dir()
        return self._pages

    @property
    def temp_pages(self):
        if not hasattr(self, '_temp_pages'):
            self._temp_pages = self.pages_in_dir(temp=True)
        return self._temp_pages

    def __str__(self):
        return self.name

    def __eq__(self, book):
        for arg_name in self.ARGS.keys():
            if getattr(self, arg_name) != getattr(book, arg_name):
                return False
        return True
