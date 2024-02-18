import pandas as pd


class PlaceSearch:
    def __init__(self, data_path, keyphrase_extractor):
        self.data = pd.read_csv(data_path)
        self.keyphrase_extractor = keyphrase_extractor

    def search_places(self, user_input):
        key_phrases = self.keyphrase_extractor.extract_keyphrases(user_input)
        filtered_df = self.data[self.data['key_phrases'].apply(lambda phrases: any(word in phrases for word in key_phrases))]
        filtered_df['matched_key_phrases'] = filtered_df['key_phrases'].apply(lambda phrases: [word for word in key_phrases if word in phrases])

        if not filtered_df.empty:
            return filtered_df[["place_name", "text", "sentiment", "key_phrases", "matched_key_phrases"]]
        else:
            return None
