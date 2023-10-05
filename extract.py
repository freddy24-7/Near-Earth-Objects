import csv
import json

from models import NearEarthObject, CloseApproach


def load_neos(neo_csv_path):
    """Load NEO data from a CSV file into a list of `NearEarthObject`s.

    :param neo_csv_path: A path to a CSV file containing NEO data.
    :return: A list of `NearEarthObject`s.
    """
    neo_objects = []

    with open(neo_csv_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            neo = NearEarthObject(
                pdes=row["pdes"],
                name=row['name'] if row['name'] else None,
                diameter=float(row['diameter']) if row['diameter'] else float('nan'),
                pha=row['pha'] == 'Y'
            )
            neo_objects.append(neo)

    return neo_objects


def load_approaches(cad_json_path):
    """Load close approach data from a JSON file into a list of `CloseApproach`s.

    :param cad_json_path: A path to a JSON file containing close approach data.
    :return: A list of `CloseApproach`s.
    """
    approach_objects = []

    with open(cad_json_path, 'r', encoding='utf-8') as jsonfile:
        data = json.load(jsonfile)
        for item in data['data']:
            approach = CloseApproach(
                des=item[0],
                cd=item[3],
                dist=float(item[4]),
                v_rel=float(item[7])
            )
            approach_objects.append(approach)

    return approach_objects
