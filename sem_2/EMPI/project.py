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
                                            not re.match('.*class.*', s.split('//')[0]) and
                                            not re.match('.*try.*', s.split('//')[0]) and
                                            not re.match('.*switch.*', s.split('//')[0]) and
                                            not re.match('.*if.*', s.split('//')[0]) and
                                            not re.match('.*else.*', s.split('//')[0]) and
                                            not re.match('.*while.*', s.split('//')[0]) and
                                            not re.match('.*for.*', s.split('//')[0]) and
                                            not re.match('.*catch.*', s.split('//')[0]))]
                               for name, content in zip(self.files_p, self.files)}
        self.metrics['total']['NOM'] = sum(map(len, self.metrics['NOM'].values()))

    def calc_WMC(self):
        self.metrics['WMC'] = {name[1]:len([len(re.findall('if|while|for|case|else', s)) + 1
                                            for s in content
                                            if not s.strip().startswith(('//', '*'))])
                               for name, content in zip(self.files_p, self.files)}
        self.metrics['total']['WMC'] = sum(self.metrics['WMC'].values())

    def calc_TCC(self):
        self.metrics['TCC'] = {}
        self.classes = {}
        for f, cont in zip(self.files_p, self.files):
            f = f[1]
            self.classes[f] = {cl: {} for cl in self.metrics['NOC'][f]}
            n_meths = 0
            con_cl = 0
            for cl, cl_meths in self.classes[f].items():
                for meth in self.metrics['NOM'][f]:
                    indent = None
                    for line in cont:
                        if indent:
                            if len(line) - len(line.lstrip()) <= indent and len(line.lstrip()):
                                break
                            cl_meths[meth] |= set(re.findall('this.\w+', line))
                        if meth in line:
                            indent = len(line) - len(line.lstrip())
                            cl_meths[meth] = set()
                n_meths += len(cl_meths)
                if len(cl_meths.values()) > 1:
                    for perm in permutations(cl_meths.values(), 2):
                        if perm[0] & perm[1]:
                            con_cl += 1
            n_meths *= n_meths - 1
            self.metrics['TCC'][f] = con_cl / n_meths if n_meths else 0
        self.metrics['total']['TCC'] = sum(self.metrics['TCC'].values()) / len(self.metrics['TCC'].values())

    def calc_PNAS(self):
        self.metrics['PNAS'] = {}
        all_meth = 0
        overr_meth = 0
        for f, clss in self.classes.items():
            s = []
            for cl, meths in clss.items():  # For every class
                tokens = cl.split()
                base_meths = set()
                for i, word in enumerate(tokens):
                    if word in {'implements', 'extends'}:
                        if i + 1 >= len(tokens):
                            continue
                        base = tokens[i + 1]
                        for f, clss in self.classes.items():
                            if base in clss.keys():
                                base_meths |= clss.values()
                                break
                if len(meths):
                    s.append(len(set(meths.keys()) - base_meths) / len(set(meths.keys())))
            self.metrics['PNAS'][f] = sum(s) / len(s) if len(s) else 0
        self.metrics['total']['PNAS'] = sum(self.metrics['PNAS'].values()) / len(self.metrics['PNAS'].values())
                    

        

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
        plot(go.Figure(data=[go.Pie(labels=list(self.metrics['WMC'].keys()), 
                                    values=list(self.metrics['WMC'].values()),
                                    textinfo='none')],
                       layout=layout), auto_open=False, filename='WMC.html')
        TCC = {item[0]:item[1] for item in self.metrics['TCC'].items() if item[1] != 0}
        plot(go.Figure(data=[go.Pie(labels=list(TCC.keys()), 
                                    values=list(TCC.values()),
                                    textinfo='none')],
                       layout=layout), auto_open=False, filename='TCC.html')
        PNAS = {item[0]:item[1] for item in self.metrics['PNAS'].items() if item[1] != 0}
        plot(go.Figure(data=[go.Pie(labels=list(PNAS.keys()), 
                                    values=list(PNAS.values()),
                                    textinfo='none')],
                       layout=layout), auto_open=False, filename='PNAS.html')
