from ast import literal_eval
import pandas as pd
from DataWriter import DataWriter
from KeyphraseExtraction import KeyphraseExtraction
from PlaceSearchLda import PlaceSearch
from PlaceSorter import PlaceSorter

keyphrase_extractor = KeyphraseExtraction("davanstrien/deberta-v3-base_fine_tuned_food_ner")
place_search = PlaceSearch('LDA_PubFinder/data_with_unique_topic_words.csv', keyphrase_extractor)


user_input = input("Enter a sentence: ")
matching_places = place_search.search_places(user_input)
data_writer = DataWriter('LDA_PubFinder/matching_places_lda.csv')
data_writer.write_to_csv(matching_places)


if matching_places is not None:
    matching_places = matching_places.reset_index(drop=True)
    sentiment_values = matching_places["vader_score"]

    place_sorter = PlaceSorter('LDA_PubFinder/matching_places_lda.csv')
    group_summary = place_sorter.get_group_summary()
    sorted_summary = sorted(group_summary, key=lambda x: (x[1], x[2] if x[2] >= 0 else float('inf')), reverse=True)

    print("\n\n")
    # Print table header
    print("{:<40} {:<20} {:<15}".format("Place Name", "Number of Comments", "Vader Score"))
    # Print each row of the table
    for place, group_length, total_score in sorted_summary:
        print("{:<40} {:<20} {:<15}".format(place, group_length, total_score))

else:
    print("No matching places found.")
