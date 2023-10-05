import csv
import json


def write_to_csv(results, filename):
    fieldnames = (
        'datetime_utc', 'distance_au', 'velocity_km_s',
        'designation', 'name', 'diameter_km', 'potentially_hazardous'
    )
    with open(filename, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        # Writing the header row
        writer.writeheader()

        # Writing each close approach as a row in the CSV file
        for approach in results:
            writer.writerow({
                'datetime_utc': approach.time_str,
                'distance_au': approach.distance,
                'velocity_km_s': approach.velocity,
                'designation': approach.neo.designation,
                'name': approach.neo.name,
                'diameter_km': approach.neo.diameter,
                'potentially_hazardous': approach.neo.hazardous
            })


def write_to_json(results, filename):
    data = []

    # Creating a list of dictionaries representing close approaches and their NEOs
    for approach in results:
        approach_data = {
            'datetime_utc': approach.time_str,
            'distance_au': approach.distance,
            'velocity_km_s': approach.velocity,
            'neo': {
                'designation': approach.neo.designation,
                'name': approach.neo.name,
                'diameter_km': approach.neo.diameter,
                'potentially_hazardous': approach.neo.hazardous
            }
        }
        data.append(approach_data)
    with open(filename, mode='w') as file:
        json.dump(data, file, indent=2)
