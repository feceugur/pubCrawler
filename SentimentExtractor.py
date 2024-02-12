from ast import literal_eval

import pandas as pd


class SentimentExtractor:
    def __init__(self, column_names=['negative', 'neutral', 'positive']):
        self.column_names = column_names

    def extract_highest_score_label(self, sentiments):
        total_scores = []
        for senti in sentiments:
            scores = []
            for sentiment in literal_eval(senti):
                for c in self.column_names:
                    if sentiment['label'] == c:
                        scores.append({c: sentiment['score']})
            total_scores.append(scores)

        flattened_data = [{k: v for d in item for k, v in d.items()} for item in total_scores]
        df_sentiments = pd.DataFrame(flattened_data).reindex(columns=self.column_names)
        return df_sentiments
