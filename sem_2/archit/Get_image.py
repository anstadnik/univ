from Parse_png import Parse_png

class Get_image(object):
    """This module is capable of the processing the input"""
    def __init__(self, args):
        if args.input is not None:
            self.processor = Parse_png(args.input)
        # else:
        #     self.processor = gui_input()
        
    def get_img(self):
        # Parses the image
        # return image
        img = self.processor.get_img()
        return img
