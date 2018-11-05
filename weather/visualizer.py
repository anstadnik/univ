#!/usr/bin/env python3
import datetime
import argparse
import sys
# import matplotlib
import matplotlib.pyplot as plt
import os
import pandas as pd

class Visualizer(object):

    """Makes cool graphs"""

    def __init__(self):
        """Initializer"""
        args = self._parse()
        self.country = args.country
        self.city = args.city
        self.parameter = args.parameter
        self.time = args.time
        self.filename = args.filename
        self.df = self._get_data()

    def _parse(self):
        """Parses *args
        :returns: TODO

        """
        self.parser = argparse.ArgumentParser(epilog = "You have to provide at least one argument")
        self.parser.add_argument("-ci", "--city", default=None, help="City to show info for")
        self.parser.add_argument("-co", "--country", default=None, help="Country to show info for")
        self.parser.add_argument("-p", "--parameter", default=None, help="Type of the parameter", choices = ['bc', 'co', 'no2', 'o3', 'pm10', 'pm25', 'so2'])
        self.parser.add_argument("-t", "--time", default=None, help="Time constrains", choices = ['month', 'week', 'day', 'hour'])
        self.parser.add_argument("-f", "--filename", default='data.json', help="File to load data from")
        self.parser.add_argument('--version', action='version', version='%(prog)s 1.0')
        args = self.parser.parse_args()
        if args.city == args.country == args.parameter == args.time == None:
            self._error("You have to provide at least one argument")
        return args

    def _get_data(self):
        """Loads data from file
        :returns: TODO

        """
        if os.path.isfile(self.filename):
            return pd.read_json(self.filename)
        else:
            self._error("No such file: " + self.filename)

    def _error(self, msg: str):
        """Prints error and quits

        :msg: str: TODO
        :returns: TODO

        """
        self.parser.error(msg)
        sys.exit()

    def _filter(self):
        """Filters data
        :returns: TODO

        """
        if self.city:
            self.df = self.df[self.df['city'] == self.city]
        if self.country:
            self.df = self.df[self.df['country'] == self.country]
        if self.parameter:
            self.df = self.df[self.df['parameter'] == self.parameter]
        if self.time:
            conv = lambda t: datetime.datetime.strptime(t, '%Y-%m-%dT%H:%M:%S.%fZ')
            now = datetime.datetime.utcnow()
            if self.time == 'hour':
                days, hours = 0, 1
            elif self.time == 'day':
                days, hours = 1, 0
            elif self.time == 'week':
                days, hours = 2, 0
            elif self.time == 'month':
                days, hours = 365/12, 0
            # print(datetime.timedelta(days))
            filt = lambda df: (now - conv(df['date.utc'])) < datetime.timedelta(days)
            # for index, row in self.df.iterrows():
            #     # print(now - conv(row['date.utc']))
            #     print(conv(row['date.utc']))
            # self.df = self.df[now - conv(self.df['date.utc']) < datetime.timedelta(days).isoformat()]
            self.df = self.df[self.df.apply(filt, axis = 1)]

    def _draw(self):
        """Draws a graph
        :returns: TODO

        """
        # pass
        # print(self.df)
        fig, ax = plt.subplots()
        for key, grp in self.df.groupby(['parameter']):
            ax = grp.plot(ax=ax, kind='line', y='value', x='date.utc', label=key)

        # for parameter in self.df['parameter'].unique():
        #     self.df[self.df['parameter'] == parameter].plot(y='value', x='date.utc')
        plt.show()

    def process(self):
        """Combines all together
        :returns: TODO

        """
        self._filter()
        if len(self.df) == 0:
            self._error("Wrong arguments, no such entries")
        self._draw()

def main():
    """Main
    :returns: TODO

    """
    visualizer = Visualizer()
    visualizer.process()

if __name__ == "__main__":
    main()
