"""this file is used to populate the database with static information on bus stops and dublin bikes stations by
backfilling static csv files into the database"""
from django.core.management.base import BaseCommand
from django.apps import AppConfig, apps
import csv


# to run this to migrate an existing csv file do the following:
# python manage.py backfill_csv --path="path_to_file" --model_name="model_class_name" --app_name="dublinbusapplication"

class Command(BaseCommand):
    help = 'Creating model objects for the specified file path'

    # adding arguments to the function when it is called directing it to the csv file, the model name and the app name
    def add_arguments(self, parser):
        parser.add_argument('--path', type=str, help="path to file")
        parser.add_argument('--model_name', type=str, help="name of model")
        parser.add_argument('--app_name', type=str, help="django app name")

    def handle(self, *args, **options):
        file_path = options['path']
        _model = apps.get_model(options['app_name'], options['model_name'])
        objects = []
        with open(file_path, 'rt') as csv_file:
            reader = csv.reader(csv_file, delimiter=',', quotechar='|')
            header = next(reader)
            for row in reader:
                _object_dict = {key: value for key, value in zip(header, row)}
                instance = _model(**_object_dict)
                objects.append(instance)
            csv_file.close()
        _model.objects.bulk_create(objects)
