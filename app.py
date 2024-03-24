import requests

from DataProcessor import DataProcessor
from DataWriter import DataWriter
from KeyphraseExtractionPipeline import KeyphraseExtractionPipeline
from SentimentAnalysis import SentimentAnalysis

keyphrase_extractor = KeyphraseExtractionPipeline("ml6team/keyphrase-extraction-kbir-inspec")
sentiment_analyzer = SentimentAnalysis("cardiffnlp/twitter-roberta-base-sentiment-latest")

data_processor = DataProcessor(keyphrase_extractor, sentiment_analyzer)
data_writer = DataWriter('data.csv')

url = 'https://cxusncka8i.execute-api.eu-central-1.amazonaws.com/api/search'
response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    processed_data = data_processor.process_data(data)
    data_writer.write_to_csv(processed_data)
