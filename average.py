"""
This file contains logic to calculate the average value of
the overlap percentage between two repositories from the CSV output
of this tool.
"""

import os
import pandas as pd


def calculate_average(path: str):
    """Calculates the average value of overlap in CSVs in the given directory."""

    if not os.path.isdir(path):
        raise NotADirectoryError(f"{path} is not a valid directory path")

    csv_files = [file for file in os.listdir(path) if file.endswith(".csv")]

    for csv_file in csv_files:
        file_path = os.path.join(path, csv_file)

        # Read the CSV file into a pandas DataFrame
        df = pd.read_csv(
            file_path,
            header=None,
            names=["Column1", "Column2", "Column3"],
        )

        # Calculate the average of the float values in the third column
        avg_value = df["Column3"].astype(float).mean()

        # Print or use the average value as needed
        print(f"Average value for {csv_file}: {avg_value}")


if __name__ == "__main__":
    folder_path = os.path.dirname(__file__)
    calculate_average(folder_path)
