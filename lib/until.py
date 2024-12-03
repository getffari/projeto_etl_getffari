import csv

def write_csv(data, filename, fieldNames):
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = fieldNames
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=';')
        writer.writeheader()
        for row in data:
            writer.writerow(row)