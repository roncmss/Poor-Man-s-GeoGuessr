from typing import List, Dict
from enum import Enum
from dataclasses import dataclass
from getpass import getpass
import google_streetview.api
import csv
import random
import time


# class of coordinates, which is the key for requesting pictures of a certain location
@dataclass
class Coord:
    longitude: float
    latitude: float

    def __str__(self) -> str:
        return f'{self.longitude}, {self.latitude}'


# enumeration for easily handling status codes in results of API requests
class Result(Enum):
    OK = 1
    RETRY = 2
    ERROR = 3


#
class Query:
    def __init__(self, key: str):
        self._key = key

    def _get_param(self, coord: Coord, heading: int) -> Dict[str, str]:
        return {
            'size': '640x640',
            'location': str(coord),
            'fov': '90',
            'heading': str(heading),
            'key': self._key,
            'source': 'outdoor'
        }

    @staticmethod
    def _handle_status_codes(status_codes: List[str]) -> Result:
        retry = False
        for status_code in status_codes:
            if status_code == 'OK':
                continue
            if status_code in ('ZERO_RESULTS', 'NOT_FOUND'):
                retry = True
            else:
                return Result.ERROR
        return Result.RETRY if retry else Result.OK

    def download(self, coord: Coord) -> Result:
        headings = [0, 90, 180, 270]
        params = [self._get_param(coord, heading) for heading in headings]
        results = google_streetview.api.results(params)
        status_codes = [metadata['status'] for metadata in results.metadata]
        result = self._handle_status_codes(status_codes)
        if result == Result.OK:
            results.download_links('downloads')
        if result == Result.ERROR:
            results.save_metadata('downloads/metadata.json')
        return result

# class of elements in the database class
@dataclass
class Csv_row:
    iso_country_code: str
    country_name: str
    coord: Coord


# class for the database, read a .csv file and store information into list, then shuffle it.
class Database:
    def __init__(self, csv_file: str):
        db = []
        with open(csv_file, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                longitude = float(row['longitude'])
                latitude = float(row['latitude'])
                db.append(Csv_row(row['isocode'], row['country'], Coord(longitude, latitude)))
        random.shuffle(db)
        self._db = db

    def get_all_countries(self):
        return set(csv_row.country_name for csv_row in self._db)

    # method of get 1 row from the database
    def get_csv_row(self) -> Csv_row:
        return self._db.pop()


# function for checking answer from user
def check_answer(iso_country_code: str, guess: str) -> bool:
    if guess.upper() == iso_country_code:
        return True
    return False


def main(key: str):
    query = Query(key)
    score = 0
    database = Database('coordinates.csv')
    while True:
        while True:
            csv_row = database.get_csv_row()
            result = query.download(csv_row.coord)
            if result == Result.OK:
                break
            elif result == Result.RETRY:
                time.sleep(1)
            elif result == Result.ERROR:
                raise RuntimeError("Something happened and we cannot fix it.")
        guess = input("Which country is it? ").lower()
        if check_answer(csv_row.iso_country_code, guess):
            score += 1
            print(f'Correct! You have {score} points now.')
        else:
            print(f'No luck! This was {csv_row.iso_country_code}')
            print(f'Your final score is {score}')
            break


if __name__ == '__main__':
    key = getpass("Enter your key: ")
    main(key)
