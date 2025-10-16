import csv

def detectar_delimitador(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        sample = f.read(1024)
        dialect = csv.Sniffer().sniff(sample, delimiters=";,")
        return dialect.delimiter
