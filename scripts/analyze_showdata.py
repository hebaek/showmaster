import argparse
import json
import pathlib

from pprint import pprint






def load_data(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)






if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    args = parser.parse_args()

    shows = load_data('data/sources/shows.json')

    micmap = {}

    for show in shows:
        data = load_data(f'data/compiled/showdata/{show}/showdata.json')

        for row in data.get('micmap'):
            location = row['location']['target']
            if not location in micmap: micmap[location] = {}

            mics = row.get('mics')

            micmap[location][show] = { mic: mics[mic]['role'] for mic in mics }


    for location in micmap:
        miclist = {}
        for show in micmap[location]:
            for mic in micmap[location][show]:
                if not mic in miclist: miclist[mic] = micmap[location][show][mic]

                if miclist[mic] != micmap[location][show][mic]:
                    print('MISMATCH', show, mic, location)
