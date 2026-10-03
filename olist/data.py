from pathlib import Path
import pandas as pd

DATA_PATH = Path.home() / ".workintech" / "olist" / "data" / "csv"

class Olist:

    def __init__(self):
        self.data_path = DATA_PATH

    def get_data(self):
        file_paths = list(self.data_path.iterdir())

        file_names = []

        for file_path in file_paths:
            file_names.append(file_path.name)

        key_names = []

        for name in file_names:
            key_names.append(
                name.replace(".csv", "")
                    .replace("_dataset", "")
                    .replace("olist_", "")
            )

        data = {}

        for key, file_path in zip(key_names, file_paths):
            data[key] = pd.read_csv(file_path)

        return data

    def ping(self):
        return "pong"
