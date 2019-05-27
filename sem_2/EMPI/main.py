"""This is the program for measuring some code metrics"""
import sys

from PySide2.QtWidgets import QApplication

from main_window import MyWidget

def main():
    """This is the main function"""
    app = QApplication(sys.argv)

    widget = MyWidget()
    widget.resize(800, 600)
    widget.show()

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
