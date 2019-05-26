"""
This is the main window which contains all objects needed for interacting with
the program
"""
from PySide2 import QtCore, QtGui, QtWidgets
from project import Project

# from PySide2.QtCore import Qt, Slot
# from PySide2.QtWidgets import (QLabel, QPushButton, QVBoxLayout, QWidget)

class MyWidget(QtWidgets.QWidget):
    """This is the main widget"""
    def __init__(self):
        QtWidgets.QWidget.__init__(self)

        # self.process = self.createButton("Process", self.open_proj)
        self.text = QtWidgets.QTextEdit("Hello World")
        self.text.setAlignment(QtCore.Qt.AlignCenter)
        self.list_metric = QtWidgets.QComboBox()
        self.list_metric.setEnabled(False)
        self.list_metric.currentTextChanged.connect(self.change_metrics)

        self.menu_bar = QtWidgets.QMenuBar(self)
        self.file_menu = self.menu_bar.addMenu("&File")
        self.file_menu.addAction("&Open project", self.open_proj)

        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addWidget(self.text)
        # self.layout.addWidget(self.process)
        self.layout.addWidget(self.list_metric)
        self.setLayout(self.layout)

        self.open_proj()

    def change_metrics(self):
        self.text.setText('\n'.join(['{}: {}'.format(name, loc)
                                     for name, loc in self.project.metrics[
                                         self.list_metric.currentText()].items()]))
        

    def open_proj(self):
        # path = QtWidgets.QFileDialog.getExistingDirectory(self, "Find Files",
        #         "/home/amyznikov/astadnik/univ/Simple-Java-Text-Editor/")
                # QtCore.QDir.currentPath())
        path = "/home/amyznikov/astadnik/univ/jadx/"
        try:
            self.project = Project(path)
        except RuntimeError as e:
            print(e)
            self.list_metric.setEnabled(False)
            self.list_metric.clear()
        self.project.compute_metrics()
        self.list_metric.setEnabled(True)
        self.list_metric.addItems(list(self.project.metrics.keys()))


    def createButton(self, text, member):
        button = QtWidgets.QPushButton(text)
        button.clicked.connect(member)
        return button
