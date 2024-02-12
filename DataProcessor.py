import re


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
