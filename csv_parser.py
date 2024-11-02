import csv

filename = "./data/refineries.csv"

fields = []
rows = []

with open(filename, "r") as csvfile:
    csvreader = csv.reader(csvfile, delimiter=";")
    fields = next(csvreader)
    for row in csvreader:
        rows.append(row)

print(" | ".join(field for field in fields))
for i in range(5):
    print(" ".join(col for col in rows[i]))