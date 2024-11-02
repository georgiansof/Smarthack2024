from utils.csv_parser import csvparser
from classes.refinery import Refinery

refineries_csv = "./data/refineries.csv"

fields, rows = csvparser(refineries_csv)

refineries = []

for row in rows:
    refineries.append(Refinery(*row[:-1]))

for refinery in refineries:
    print(refinery)

# Repeat for each class. Don't forget to add __str__(self) for remaining classes. (Adrifot, 15:05)