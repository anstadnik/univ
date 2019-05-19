import pytesseract

class Singleton(object):
    _instance = None
    def __new__(class_, *args, **kwargs):
        if not isinstance(class_._instance, class_):
            class_._instance = object.__new__(class_, *args, **kwargs)
        return class_._instance


class Processor(Singleton):
    """Processes the image and returns the text"""
    def init(self, img):
        self.img = img

    def process(self):
        # Process the image
        # Return text
        text = pytesseract.image_to_string(self.img)
        return text
