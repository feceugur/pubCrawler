import re
import pandas as pd


def preprocess_text(text):
    text = text.lower()
    return text


class DataProcessor:
    def __init__(self, keyphrase_extractor, sentiment_analyzer):
        self.keyphrase_extractor = keyphrase_extractor
        self.sentiment_analyzer = sentiment_analyzer

    def process_data(self, data):
        data_list = []
        for item in data:
            for index, review in enumerate(item["reviews"]):
                if review["review_text"] is not None:
                    text = review["review_text"]
                    text = preprocess_text(text)
                     # Use a more precise regex pattern to capture the text between "\(translated by google\)" and "\(original\)"
                    result = re.search(r'\(translated by google\)(.*?)\(original\)', text, re.DOTALL)
                
                    if result:
                        extracted_text = result.group(1)
                        extracted_text = re.sub(r'\n', '', extracted_text)
                        text = extracted_text[:500]
                    else:
                        text = text[:500]

                    sentiment_result = self.sentiment_analyzer.analyze_sentiment(text)
                    key_phrases_result = self.keyphrase_extractor(text)
                    data_list.append({
                        "place_name": item["name"],
                        "text": text,
                        "sentiment": sentiment_result,
                        "key_phrases": key_phrases_result
                    })

        return data_list
    

    def process_scrpd_data(self, csv_file_path):
        data_list = []
        df = pd.read_csv(csv_file_path)  # Read CSV file into DataFrame
        
        for index, row in df.iterrows():  # Iterate over DataFrame rows
            place_name = row['place_name']
            review_text = row['review_text']
            
            if pd.notnull(review_text):  # Check if review_text is not null
                review_text = preprocess_text(review_text)
                
                sentiment_result = self.sentiment_analyzer.analyze_sentiment(review_text)
                key_phrases_result = self.keyphrase_extractor(review_text)
                
                data_list.append({
                    "place_name": place_name,
                    "text": review_text,
                    "sentiment": sentiment_result,
                    "key_phrases": key_phrases_result
                })
        
        return data_list

