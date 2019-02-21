import argparse


def parse():
    parser = argparse.ArgumentParser(epilog='If no filename is provided, user\
                                     has to write text himself. If no output\
                                     filename is provided, output will be\
                                     printed into the stdout.')
    parser.add_argument("-i", "--input", type=argparse.FileType('r'),
                        default=None, help="Name of the input image",
                        metavar='FIlENAME')
    parser.add_argument("-o", "--output", type=argparse.FileType('w'),
                        default=None, help="Name of the output file",
                        metavar='FILENAME')
    return parser.parse_args()
