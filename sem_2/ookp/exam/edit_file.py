"""
This is the main window which contains all objects needed for editing the file
"""
from PySide2 import QtCore, QtGui, QtWidgets, QtWebEngineWidgets

# from PySide2.QtCore import Qt, Slot
# from PySide2.QtWidgets import (QLabel, QPushButton, QVBoxLayout, QWidget)


class EditFile(QtWidgets.QDialog):
    """This is the main widget"""
    text = ''

    def __init__(self, edit: bool):
        QtWidgets.QDialog.__init__(self)

        #################
        #  Add widgets  #
        #################

        self.edit = QtWidgets.QTextEdit("Potato")
        self.edit.setEnabled(True)
        #  TODO: Set based on permission <18-06-19, astadnik> # 
        self.edit.setReadOnly(not edit)

        self.save_b = self.createButton('Save', self.save)
        self.save_b.setEnabled(edit)
        #  TODO: Make disabled if no permissions <18-06-19, astadnik> # 

        ####################
        #  Set the layout  #
        ####################

        self.layout = QtWidgets.QGridLayout()

        self.layout.addWidget(self.edit, 0, 0)
        self.layout.addWidget(self.save_b, 0, 1)
        self.setLayout(self.layout)

        # self.open_proj()

    def save(self):
        """Save the file
        Returns: TODO

        """
        EditFile.text = self.edit.toPlainText()

    def createButton(self, text, member):
        button = QtWidgets.QPushButton(text)
        button.clicked.connect(member)
        return button
