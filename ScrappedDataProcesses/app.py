from DataProcessor import DataProcessor
from DataWriter import DataWriter
from KeyphraseExtractionPipeline import KeyphraseExtractionPipeline
from SentimentAnalysis import SentimentAnalysis

keyphrase_extractor = KeyphraseExtractionPipeline("ml6team/keyphrase-extraction-kbir-inspec")
sentiment_analyzer = SentimentAnalysis("cardiffnlp/twitter-roberta-base-sentiment-latest")

data_processor = DataProcessor(keyphrase_extractor, sentiment_analyzer)
data_writer = DataWriter('scrapped_analysed_data.csv')

processed_data = data_processor.process_scrpd_data('/Users/fuldeneceugur/PycharmProjects/pubCrawler/Scrapper/recent_reviews.csv')
data_writer.write_to_csv(processed_data)

