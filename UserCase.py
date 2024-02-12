from KeyphraseExtraction import KeyphraseExtraction
from PlaceSearch import PlaceSearch


keyphrase_extractor = KeyphraseExtraction("davanstrien/deberta-v3-base_fine_tuned_food_ner")
place_search = PlaceSearch('data.csv', keyphrase_extractor)

user_input = input("Enter a sentence: ")
matching_places = place_search.search_places(user_input)

if matching_places is not None:
    print("Matching Places:")
    print(matching_places)
else:
    print("No matching places found.")