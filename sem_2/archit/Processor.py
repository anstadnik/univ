import pytesseract

class Processor():
    """Processes the image and returns the text"""
    def init(self, img):
        self.img = img

    def process(self):
        # Process the image
        # Return text
        self.text = pytesseract.image_to_string(self.img)
        return self.text
