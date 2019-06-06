"""
This is the main window which contains all objects needed for interacting with
the program
"""
from PySide2 import QtCore, QtGui, QtWidgets, QtWebEngineWidgets
from project import Project
import desc

# from PySide2.QtCore import Qt, Slot
# from PySide2.QtWidgets import (QLabel, QPushButton, QVBoxLayout, QWidget)

class MyWidget(QtWidgets.QDialog):
    """This is the main widget"""
    def __init__(self):
        QtWidgets.QDialog.__init__(self)

        #################
        #  Add widgets  #
        #################

        self.path = QtWidgets.QLabel('Project')
        self.path.setEnabled(False)
        
        self.text = QtWidgets.QTextEdit("Potato")
        self.text.setEnabled(False)
        self.text.setReadOnly(True)

        self.desc = QtWidgets.QTextEdit("Please open the project")
        self.desc.setReadOnly(True)

        self.total = QtWidgets.QLabel('Total')
        self.total.setEnabled(False)

        self.list_metric = QtWidgets.QComboBox()
        self.list_metric.setEnabled(False)
        self.list_metric.currentTextChanged.connect(self.change_metrics)

        self.proj = self.createButton('Open project', self.open_proj)

        ####################
        #  Set the layout  #
        ####################
        self.web = QtWebEngineWidgets.QWebEngineView()
        self.web.setEnabled = False
        self.web.load(None)
        # self.web.load(QtCore.QUrl.fromLocalFile('/home/amyznikov/astadnik/univ/univ_oop/sem_2/EMPI/LOC.html'))

        self.layout = QtWidgets.QGridLayout()

        self.buttons = QtWidgets.QVBoxLayout()
        self.buttons.addStretch()
        self.buttons.addWidget(self.path)
        self.buttons.addWidget(self.text)
        self.buttons.addWidget(self.desc)
        self.buttons.addWidget(self.total)
        self.buttons.addWidget(self.proj)
        self.buttons.addWidget(self.list_metric)

        self.layout.addWidget(self.web, 0, 0)
        self.layout.addLayout(self.buttons, 0, 1)
        self.setLayout(self.layout)

        # self.open_proj()

    def change_metrics(self):
        if not self.list_metric.currentText():
            return
        path = '/home/amyznikov/projects/univ'
        self.web.load(QtCore.QUrl.fromLocalFile('/home/astadnik/projects/univ/my_works/sem_2/EMPI/{}.html'.format(self.list_metric.currentText())))
        self.desc.setText(desc.metrics[self.list_metric.currentText()])
        self.total.setText('Total: {}'.format(self.project.metrics['total'][self.list_metric.currentText()]))
        self.text.setText('\n'.join(['{}: {}'.format(name, loc)
                                     for name, loc in self.project.metrics[
                                         self.list_metric.currentText()].items()]))

    def open_proj(self):
        path = QtWidgets.QFileDialog.getExistingDirectory(self, "Find Files",
                # "/home/amyznikov/astadnik/univ/Simple-Java-Text-Editor/")
                QtCore.QDir.currentPath())
        # path = "/home/amyznikov/astadnik/univ/Simple-Java-Text-Editor/"
        # path = "/home/amyznikov/astadnik/univ/Simple-Java-Text-Editor"
        try:
            self.project = Project(path)
        except RuntimeError as e:
            print(e)
            self.desc = QtWidgets.QTextEdit("Please open the project")
            self.web.setEnabled(False)
            self.text.setEnabled(False)
            self.list_metric.setEnabled(False)
            self.path.setEnabled(False)
            self.total.setEnabled(False)
            self.list_metric.clear()
        self.path.setText(path.split('/')[-1])
        self.project.compute_metrics()
        self.list_metric.setEnabled(True)
        self.path.setEnabled(True)
        self.web.setEnabled = True
        self.total.setEnabled(True)
        self.text.setEnabled(True)
        self.list_metric.clear()
        metrics = list(self.project.metrics.keys())
        metrics.remove('total')
        self.list_metric.addItems(metrics)
        self.list_metric.setCurrentText('LOC')
        self.change_metrics()


    def createButton(self, text, member):
        button = QtWidgets.QPushButton(text)
        button.clicked.connect(member)
        return button
