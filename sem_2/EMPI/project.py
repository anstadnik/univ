"""This module handles opening the project"""

from PySide2 import QtCore
import plotly.graph_objs as go
from plotly.offline import plot
from itertools import permutations
import re

class Project:
    """This class represents the project"""
    def __init__(self, path):
        self.path = path
        self.files_p = self.find_java_files(path)
        self.files = self.parse_files()
        if not self.files:
            raise RuntimeError("No .java files were found")
        self.compute_metrics()
        self.make_plots()

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
        self.metrics['total'] = {}
        self.calc_LOC()
        self.calc_NOC()
        self.calc_NDD()
        self.calc_CALL()
        self.calc_NOM()
        self.calc_WMC()
        self.calc_TCC()
        self.calc_PNAS()

    def calc_LOC(self):
        self.metrics['LOC'] = {name[1]:len(content) for
                               name, content in zip(self.files_p, self.files)}
        self.metrics['total']['LOC'] = sum(self.metrics['LOC'].values())

    def calc_NOC(self):
        self.metrics['NOC'] = {name[1]:[s.strip().split('//')[0] for s in content
                                        if (not s.strip().startswith(('//', '*')) and
                                            re.match('.* class .*', s.strip().split('//')[0]) and
                                            not re.match('.*[";].*', s.split('//')[0]))]
                               for name, content in zip(self.files_p, self.files)}
        self.metrics['total']['NOC'] = sum(map(len, self.metrics['NOC'].values()))

    def calc_NDD(self):
        self.metrics['NDD'] = {name[1]:len([rez
                                            for s in self.metrics['NOC'][name[1]]
                                            for rez in re.findall('implements|extends', s)])
                               for name in self.files_p}
        self.metrics['total']['NDD'] = sum(self.metrics['NDD'].values())

    def calc_CALL(self):
        self.metrics['CALL'] = {name[1]:[rez
                                         for s in content
                                         for rez in re.findall('[\w+\|\)]\.\w+\(',
                                                               s.strip().split('//')[0])]
                                for name, content in zip(self.files_p, self.files)}
        self.metrics['total']['CALL'] = sum(map(len, self.metrics['CALL'].values()))

    def calc_NOM(self):
        self.metrics['NOM'] = {name[1]:[s.strip().split('//')[0] for s in content
                                        if (not s.strip().startswith(('//', '*')) and
                                            re.match('.* {.*', s.strip().split('//')[0]) and
                                            not re.match('.*class.*', s.split('//')[0]))]
                               for name, content in zip(self.files_p, self.files)}
        self.metrics['total']['NOM'] = sum(map(len, self.metrics['NOM'].values()))

    def calc_WMC(self):
        self.metrics['WMC'] = {name[1]:len([len(re.findall('if|while|for|case|else', s)) + 1
                                            for s in content
                                            if not s.strip().startswith(('//', '*'))])
                               for name, content in zip(self.files_p, self.files)}
        self.metrics['total']['WMC'] = sum(self.metrics['WMC'].values())

    def calc_TCC(self):
        for f, cont in zip(self.files_p, self.files):
            f = f[1]
            classes = {cl: {} for cl in self.metrics['NOC'][f]}
            rez = 0
            for cl, cl_meths in classes.items():
                for meth in self.metrics['NOM'][f]:
                    indent = None
                    for line in cont:
                        if indent:
                            if len(line) - len(line.lstrip()) <= indent:
                                break
                            cl_meths[f] |= set(re.findall('self.\w\+', line))
                        if meth in line:
                            indent = len(line) - len(line.lstrip())
                            cl_meths[f] = set()
                    else:
                        continue
                    break
                con_cl = 0
                print(cl)
                for perm in permutations(cl_meths, 2):
                    if perm[0][1] & perm[1][1]:
                        con_cl += 1
                rez = (rez + (con_cl / (len(cl[1]) * (len(cl[1]) - 1)))) / 2
            self.metrics['TCC'][f] = rez

    def calc_PNAS(self):
        pass

    def make_plots(self):
        layout = go.Layout(showlegend=False)
        plot(go.Figure(data=[go.Pie(labels=list(self.metrics['LOC'].keys()), 
                                    values=list(self.metrics['LOC'].values()), textinfo='none')],
                       layout=layout), auto_open=False, filename='LOC.html')
        plot(go.Figure(data=[go.Pie(labels=list(self.metrics['NOC'].keys()), 
                                    values=list(map(len, self.metrics['NOC'].values())),
                                    textinfo='none')],
                       layout=layout), auto_open=False, filename='NOC.html')
        plot(go.Figure(data=[go.Pie(labels=list(self.metrics['NOM'].keys()), 
                                    values=list(self.metrics['NOM'].values()), textinfo='none')],
                       layout=layout), auto_open=False, filename='NOM.html')
        plot(go.Figure(data=[go.Pie(labels=list(self.metrics['NDD'].keys()), 
                                    values=list(self.metrics['NDD'].values()), textinfo='none')],
                       layout=layout), auto_open=False, filename='NDD.html')
        plot(go.Figure(data=[go.Pie(labels=list(self.metrics['CALL'].keys()), 
                                    values=list(map(len, self.metrics['CALL'].values())),
                                    textinfo='none')],
                       layout=layout), auto_open=False, filename='CALL.html')
        plot(go.Figure(data=[go.Pie(labels=list(self.metrics['NOM'].keys()), 
                                    values=list(map(len, self.metrics['NOM'].values())),
                                    textinfo='none')],
                       layout=layout), auto_open=False, filename='NOM.html')
