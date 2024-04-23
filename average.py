import pandas as pd
import os


def calculate_average(path: str):
    csv_files = [
        file for file in os.listdir(folder_path) if file.endswith('.csv')
    ]

    for csv_file in csv_files:
        file_path = os.path.join(folder_path, csv_file)

        # Read the CSV file into a pandas DataFrame
        df = pd.read_csv(
            file_path,
            header=None,
            names=['Column1', 'Column2', 'Column3'],
        )

        # Calculate the average of the float values in the third column
        avg_value = df['Column3'].astype(float).mean()

        # Print or use the average value as needed
        print(f'Average value for {csv_file}: {avg_value}')


if __name__ == '__main__':
    folder_path = os.path.dirname(__file__)
    calculate_average(folder_path)
