from PIL import Image

class Parse_png:
    """Parses an image"""
    def __init__(self, path):
        self.path = path
        # self.path = str(ascii(self.path))  # str(self.path, errors='replace')

    def get_img(self):
        print(self.path)
        try:
            img = Image.open(self.path)
        except IOError as e:
            print(e)
            quit(1)
        return img
