"""This module handles opening the project"""

from PySide2 import QtCore
import re

class Project:
    """This class represents the project"""
    def __init__(self, path):
        self.path = path
        self.files_p = self.find_java_files(path)
        self.files = self.parse_files()
        if not self.files:
            raise RuntimeError("No .java files were found")

    def find_java_files(self, path):
        """This function recursively finds java files in the path"""
        d = QtCore.QDir(path)
        ret = []
        if path:
            ret.extend(list(map(lambda p: [d.absolutePath() + '/', p],
                                d.entryList(["*.java"],
                                            QtCore.QDir.Files |
                                            QtCore.QDir.NoDotAndDotDot |
                                            QtCore.QDir.NoSymLinks))))
            for directory in d.entryList(QtCore.QDir.AllDirs | QtCore.QDir.NoDotAndDotDot | QtCore.QDir.NoSymLinks):
                ret.extend(self.find_java_files(d.absolutePath() + '/' + directory))
        return ret

    def parse_files(self):
        files = []
        for fp in self.files_p:
            try:
                with open(fp[0] + fp[1], 'r') as f:
                    files.append(f.readlines())
            except IOError as e:
                print("File {} was not found".format(fp[0] + fp[1]))
        return files

    def compute_metrics(self):
        self.metrics = {}
        self.calc_LOC()
        self.calc_NOC()
        self.calc_NDD()
        self.calc_CALL()
        self.calc_NOM()

    def calc_LOC(self):
        self.metrics['LOC'] = {name[1]:len(content) for
                               name, content in zip(self.files_p, self.files)}

    def calc_NOC(self):
        self.metrics['NOC'] = {name[1]:[s.strip().split('//')[0] for s in content
                                        if (not s.strip().startswith(('//', '*')) and
                                            re.match('.* class .*', s.strip().split('//')[0]) and
                                            not re.match('.*[";].*', s.split('//')[0]))]
                               for name, content in zip(self.files_p, self.files)}

    def calc_NDD(self):
        self.metrics['NDD'] = {name[1]:len([rez
                                            for s in self.metrics['NOC'][name[1]]
                                            for rez in re.findall('implements|extends', s)])
                               for name in self.files_p}

    def calc_CALL(self):
        self.metrics['CALL'] = {name[1]:[rez
                                         for s in content
                                         for rez in re.findall('[\w+\|\)]\.\w+\(',
                                                               s.strip().split('//')[0])]
                                for name, content in zip(self.files_p, self.files)}

    def calc_NOM(self):
        self.metrics['NOM'] = {name[1]:[s.strip().split('//')[0] for s in content
                                        if (not s.strip().startswith(('//', '*')) and
                                            re.match('.* {.*', s.strip().split('//')[0]) and
                                            not re.match('.*class.*', s.split('//')[0]))]
                               for name, content in zip(self.files_p, self.files)}

