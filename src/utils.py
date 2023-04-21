import pandas as pd

def validate_csv_file(file):
    try:
        file.seek(0)  # Reset file pointer to the beginning
        df = pd.read_csv(file)

        required_columns = ['Id', 'Expensive']
        if set(required_columns).issubset(df.columns):
            return True
        else:
            return False
    except Exception as e:
        return False
