import csv
import re
import codecs
from pdb import set_trace as st

folderPath = '/home/tech/Reports/'

class csvEngine:
    def CreateCSVReport(self, objData, filename):
        report_data = open(folderPath + filename, 'w', newline='')
        csvwriter = csv.writer(report_data)
        for count, data in enumerate(objData):
            if count == 0:
                header = data.keys()
                csvwriter.writerow(header)
            csvwriter.writerow(data.values())
        report_data.close()
        return "Report created on location " + folderPath + filename + " Successfully."

   