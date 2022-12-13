

from . import pdf2txt

class PreProcessor:
    def __init__(self, data):
        self.data = data

    def _process(self):
        raise NotImplementedError

    def process(self):
        return self.data

