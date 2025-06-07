import csv
import json

def load_country_coordinates():
    with open("app/static/data/places.json") as f:
        data = json.load(f)
        return {entry["country"]: {
            "latitude": entry["latitude"],
            "longitude": entry["longitude"],
            "alpha3": entry["alpha3"]
        } for entry in data["ref_country_codes"]}


def read_visited_csv():
    with open("app/static/data/visited.csv") as f:
        reader = csv.DictReader(f)
        return [row for row in reader]
