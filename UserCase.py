from ast import literal_eval
import pandas as pd
from DataWriter import DataWriter
from KeyphraseExtraction import KeyphraseExtraction
from PlaceSearch import PlaceSearch
from SentimentExtractor import SentimentExtractor

keyphrase_extractor = KeyphraseExtraction("davanstrien/deberta-v3-base_fine_tuned_food_ner")
place_search = PlaceSearch('data.csv', keyphrase_extractor)
sentiment_extractor = SentimentExtractor()

user_input = input("Enter a sentence: ")
matching_places = place_search.search_places(user_input)
data_writer = DataWriter('matching_places.csv')
data_writer.write_to_csv(matching_places)

if matching_places is not None:
    matching_places = matching_places.reset_index(drop=True)
    sentiment_values = sentiment_extractor.extract_highest_score_label(matching_places["sentiment"])
    df_concat = pd.concat([matching_places, sentiment_values], axis=1)
    df_concat = df_concat.drop(columns=['sentiment'])
    df_concat = df_concat.groupby('place_name').mean(numeric_only=True)
    df_concat['count'] = matching_places['place_name'].value_counts()
    condition = df_concat['positive'] < 0.5
    df_concat.loc[condition, 'info'] = 'Original count: ' + df_concat['count'].astype(str) 
    df_concat.loc[condition, 'count'] = 1
    df_concat = df_concat.sort_values(by=['count', 'positive'], ascending=[False, False])
    print(df_concat)

else:
    print("No matching places found.")