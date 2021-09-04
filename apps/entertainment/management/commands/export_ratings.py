import os
import csv

from django.core.management.base import BaseCommand
from django.utils import timezone


class Command(BaseCommand):
    help = 'Exports ratings order by rating average count'

    def add_arguments(self, parser):
        parser.add_argument(
            '--path',
            help='specify the path for csv file',
            default='./'
        )
        parser.add_argument(
            '--file_name',
            help='name of the csv file',
            default='output'
        )

    def handle(self, *args, **kwargs):
        from apps.entertainment.models import Channel
        from apps.utils import recursive_average_calculator

        time = timezone.now().strftime('%X')
        self.stdout.write("Creating Rating Csv file operation started %s" % time)

        path = kwargs.get('path', './')
        file_name = f"{kwargs.get('file_name', 'output')}.csv"

        self.stdout.write(f'the path of file is specified as: {path}')
        self.stdout.write(f'the name of file is specified as: {file_name}')

        root_channels = Channel.objects.filter(parent=None)
        calculated_average_list = []
        for channel in root_channels:
            recursive_average_calculator(channel, calculated_average_list)

        with open(os.path.join(path, file_name), 'w', encoding='UTF8') as f:
            writer = csv.writer(f)

            writer.writerow(['Channel Title', 'Average Rating'])

            for calculated_average in calculated_average_list:
                writer.writerow(list(calculated_average.values()))

        self.stdout.write('Creating Rating Csv file operation ended')
