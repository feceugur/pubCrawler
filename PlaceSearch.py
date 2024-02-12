import pandas as pd


class PlaceSearch:
    def __init__(self, data_path, keyphrase_extractor):
        self.data = pd.read_csv(data_path)
        self.keyphrase_extractor = keyphrase_extractor

    def search_places(self, user_input):
        key_phrases = self.keyphrase_extractor.extract_keyphrases(user_input)
        matching_rows = self.data[self.data['key_phrases'].apply(lambda x: any(phrase in x for phrase in key_phrases))]

        if not matching_rows.empty:
            return matching_rows[['place_name']]
        else:
            return None