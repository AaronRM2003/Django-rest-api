import json
from django.core.management.base import BaseCommand
from myapp.models import MyModel

class Command(BaseCommand):
    help = 'Import data from a JSON file'

    def add_arguments(self, parser):
        parser.add_argument('json_file', type=str)

    def handle(self, *args, **kwargs):
        file_path = kwargs['json_file']
        with open("products.json", 'r') as file:
            data = json.load(file)
            for item in data:
                MyModel.objects.create(**item)
        self.stdout.write(self.style.SUCCESS('Successfully imported data'))
