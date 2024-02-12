from ast import literal_eval
import pandas as pd
from KeyphraseExtraction import KeyphraseExtraction
from PlaceSearch import PlaceSearch
from SentimentExtractor import SentimentExtractor


keyphrase_extractor = KeyphraseExtraction("davanstrien/deberta-v3-base_fine_tuned_food_ner")
place_search = PlaceSearch('data.csv', keyphrase_extractor)
sentiment_extractor = SentimentExtractor()

user_input = input("Enter a sentence: ")
matching_places = place_search.search_places(user_input)
"""
if matching_places is not None:
    matching_places = matching_places.reset_index(drop=True)
    sentiment_values = sentiment_extractor.extract_highest_score_label(matching_places["sentiment"])

    df_concat = pd.concat([matching_places, sentiment_values], axis=1)
    df_concat = df_concat.drop(columns=['sentiment'])
    df_concat = df_concat.groupby('place_name').mean()
    df_concat['count'] = matching_places['place_name'].value_counts()
    print(df_concat)

else:
    print("No matching places found.")
"""

def extract_highest_score_label(sentiments):
    column_names = ['negative', 'neutral', 'positive']
    total_scores = []
    for senti in sentiments:
        scores = []
        for sentiment in literal_eval(senti):
            for c in column_names:
                if sentiment['label'] == c:
                    scores.append({c: sentiment['score']})
        total_scores.append(scores)

    flattened_data = [{k: v for d in item for k, v in d.items()} for item in total_scores]
    df_sentiments = pd.DataFrame(flattened_data).reindex(columns=column_names)
    return df_sentiments



if matching_places is not None:
    matching_places = matching_places.reset_index(drop=True)
    sentiment_values = extract_highest_score_label(matching_places["sentiment"])

    df_concat = pd.concat([matching_places, sentiment_values], axis=1)
    print(df_concat.groupby(['place_name']).mean())


else:
    print("No matching places found.")