import pandas as pd
from transformers import AutoModelForTokenClassification, AutoTokenizer, pipeline


class KeyphraseExtraction:
    def __init__(self, model_name):
        self.model_name = model_name
        self.keyphrase_extractor = pipeline('ner', model=AutoModelForTokenClassification.from_pretrained(model_name),
                                           tokenizer=AutoTokenizer.from_pretrained(model_name), aggregation_strategy="simple")

    def extract_keyphrases(self, text):
        key_phrases = self.keyphrase_extractor(text)
        print(key_phrases[0]['word'])
        return key_phrases[0]['word']
    
    
