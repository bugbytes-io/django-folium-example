import csv
from django.conf import settings
from django.core.management.base import BaseCommand
from core.models import EVChargingLocation


class Command(BaseCommand):
    help = 'Load data from EV Station file'

    def handle(self, *args, **kwargs):
        data_file = settings.BASE_DIR / 'data' / 'EV_Charging_Stations.csv'
        keys = ('Station Name', 'New Georeferenced Column')  # the CSV columns we will gather data from.
        
        records = []
        with open(data_file, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                records.append({k: row[k] for k in keys})

        # extract the latitude and longitude from the Point object
        for record in records:
            longitude, latitude = record['New Georeferenced Column'].split("(")[-1].split(")")[0].split()
            record['longitude'] = float(longitude)
            record['latitude'] = float(latitude)

            # add the data to the database
            EVChargingLocation.objects.get_or_create(
                station_name=record['Station Name'],
                latitude=record['latitude'],
                longitude=record['longitude']
            )