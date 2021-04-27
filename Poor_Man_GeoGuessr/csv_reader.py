import csv

def get_coord():
    country_list = []
    with open('coordinates.csv', 'r', newline='') as coordinates:
        reader = csv.DictReader(coordinates)
        for row in reader:
            print(row)


get_coord()
