import csv

from django.core.management import BaseCommand


class Command(BaseCommand):

    def handle(self, old_filename, new_filename, **options):
        rows = self.get_rows_from_csv_file(old_filename)
        cleaned_rows = self.clean_rows(rows)
        self.assert_rectangular_matrix(cleaned_rows)
        self.write_to_csv(cleaned_rows, new_filename)

    @staticmethod
    def clean_rows(rows):
        header = rows[0]
        body = rows[1:]

        def _clean_row(row):
            assert len(row) >= len(header)
            while len(row) > len(header):
                row = row[0:2] + [row[2] + ',' + row[3]] + row[4:]
            return row

        return [header] + [_clean_row(row) for row in body if row[0] != '266291']

    @staticmethod
    def assert_rectangular_matrix(matrix):
        assert len(set(len(row) for row in matrix)) == 1

    @staticmethod
    def get_rows_from_csv_file(filename):
        with open(filename, 'rU') as csvfile:
            csvreader = csv.reader(csvfile)
            return list(csvreader)

    @staticmethod
    def write_to_csv(rows, filename):
        with open(filename, 'wb') as csvfile:
            csvwriter = csv.writer(csvfile)
            for row in rows:
                csvwriter.writerow(row)

    def add_arguments(self, parser):
        parser.add_argument('old_filename')
        parser.add_argument('new_filename')