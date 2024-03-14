import pandas as pd


class DataWriter:
    def __init__(self, file_path):
        self.file_path = file_path

    def write_to_csv(self, data):
        df = pd.DataFrame(data)
        df.to_csv(self.file_path, index=False)