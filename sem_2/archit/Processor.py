import pytesseract

class Processor():
    """Processes the image and returns the text"""
    def __init__(self, img):
        self.img = img

    def process(self):
        # Process the image
        # Return text
        text = pytesseract.image_to_string(self.img)
        return text
