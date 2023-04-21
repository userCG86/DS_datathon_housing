import csv
import io

def validate_csv_file(file):
    try:
        content = file.read().decode()
        csv.reader(io.StringIO(content))
        return True
    except csv.Error:
        return False
