#!/usr/bin/env python3
import pandas as pd
import time
import requests
import json
import argparse
import os

class Scrapper(object):
    """Updates data
    """

    def __init__(self, url, filename, interval, verbose, limit, pages):
        self.url = url + "?limit=" + str(limit)
        self.filename = filename
        self.interval = interval
        self.verbose = verbose
        self.counter = 0
        self.pages = pages

    def _get_data(self):
        """Loads data from internet
        :returns: TODO

        """
        rez = pd.DataFrame()
        for p in range(1, self.pages + 1):
            url = self.url + '&page=' + str(p)
            response = json.loads(requests.get(url).text)
            # print(url)
            rez.append(response, ignore_index=True)
        return pd.io.json.json_normalize(response['results'])

    def _get_local_data(self):
        """Downloads local data
        :returns: TODO

        """
        if os.path.isfile(self.filename):
            return pd.read_json(self.filename)
        else:
            return None

    def _concat(self, old, new):
        """Concatenates both dataframes
        :returns: TODO

        """
        new_df = pd.concat([old,new], sort=False)
        new_df.drop_duplicates(inplace=True, keep='last')
        return new_df.reset_index(drop=True)

    def _save_file(self, data):
        """Saves file locally

        :data: TODO
        :returns: TODO

        """
        data.to_json(self.filename)

    def _update(self):
        """Updates the local dataframe
        :returns: TODO

        """
        new = self._get_data()
        old = self._get_local_data()
        updated = self._concat(old, new)
        self._save_file(updated)
        if self.verbose:
            if self.counter > 0 and self.counter % 20 == 0:
                print()
            print(".", end = "", flush=True)


    def loop(self):
        """Loops
        :returns: TODO

        """
        while True:
            self._update()
            time.sleep(self.interval)
        # threading.Timer(self.interval, self.loop).start()

def main():
    """Main function
    :returns: TODO

    """
    parser = argparse.ArgumentParser("scrapper")
    parser.add_argument("-u", "--url", default = "https://api.openaq.org/v1/measurements", help="Url to get info from")
    parser.add_argument("-f", "--filename", default="data.json", help="Name of file where local changes are")
    parser.add_argument("-i", "--interval", type=int, default=10, help="Interval between updates of data in seconds")
    parser.add_argument("-v", "--verbose", action='store_true', help="Set to True to enable verbosity")
    parser.add_argument("-l", "--limit", type=int, default=100, help="Number of values to load in one update")
    parser.add_argument("-p", "--pages", type=int, default=1, help="Number of pages to load in one update")
    parser.add_argument('--version', action='version', version='%(prog)s 1.0')
    args = parser.parse_args()
    scrapper = Scrapper(args.url, args.filename, args.interval, args.verbose, args.limit, args.pages)
    scrapper.loop()

def wrapper(fun):
    """Wraps function, handles interruption

    :fun: TODO
    :returns: TODO

    """
    try:
        fun()
    except KeyboardInterrupt:
        print("Finished")
        quit()

if __name__ == "__main__":
    wrapper(main)
