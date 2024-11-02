import csv

filename = "./data/refineries.csv"

def csvparser(filename):
    fields = []
    rows = []
    with open(filename, "r") as csvfile:
        csvreader = csv.reader(csvfile, delimiter=";")
        fields = next(csvreader)
        for row in csvreader:
            rows.append(row)
    return fields, rows
