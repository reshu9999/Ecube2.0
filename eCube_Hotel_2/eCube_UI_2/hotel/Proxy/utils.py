import pandas as pd
from django.conf import settings


class CSVReader(object):

    MEDIA_ROOT = settings.MEDIA_ROOT

    def __init__(self, file_path):
        self.file_path = file_path
        self.filename = self.file_path.split('/')[-1]
        self.source_path = self.MEDIA_ROOT + self.file_path
        #self.csv_file = open(self.source_path, 'r')
        self.csv_file = open(self.source_path, 'r',encoding='cp1252')
        self._csv_data = None
        self._headers = None

    @classmethod
    def _csv_reader_map(cls):
        return {
            'xls': {'func': lambda x: pd.read_excel(x.name).values.T.tolist()[0]},
            'xlsx': {'func': lambda x: pd.read_excel(x.name).values.T.tolist()[0]},
            'csv': {'func': lambda x: [line.replace('\n', '').split(',') for line in x.readlines()]},
        }

    @property
    def _get_extension(self):
        return self.csv_file.name.split('.')[-1]

    @property
    def csv_data(self):
        if not self._csv_data == None:
            return self._csv_data

        READER_MAP = self._csv_reader_map()
        if self._get_extension not in READER_MAP:
            return None

        csv_data = READER_MAP[self._get_extension]['func'](self.csv_file)
        self._csv_data = csv_data[1:]
        
        if len(csv_data) == 0:
            return None
        else:
            self._headers = csv_data[0]
            return self.csv_data

    def get_value(self, header, row):
        return row[self._headers.index(header)]

    def __exit__(self, *args):
        self.csv_file.close()
