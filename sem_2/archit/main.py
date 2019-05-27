#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Parser import Parser
from Get_image import Get_image
from Processor import Processor
from Output import Output


def main():
    # Initialize the parser
    parser = Parser()

    # Get arguments
    args = parser.parse()

    # Check the arguments

    # Initialize the get_img
    get_img = Get_image(args)

    # Get the input image
    img = get_img.get_img()

    # We have to change the way the constructor is called
    processor = Processor()
    processor.init(img)

    # Process the image and get the resulting text
    text = processor.process()

    # Initialize the output
    output = Output(text)

    # Output the resulting text
    output.output()

    print('The 2nd output:')
    print()

    # Initialize the processor again
    processor = Processor()

    # This time don't process the image

    # Initialize the output with the new object's field
    output = Output(processor.text)

    # Output the resulting text
    output.output()


if __name__ == "__main__":
    main()
