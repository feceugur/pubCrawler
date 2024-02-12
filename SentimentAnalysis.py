from transformers import AutoTokenizer, AutoConfig, AutoModelForSequenceClassification
from scipy.special import softmax
import numpy as np
import torch


class SentimentAnalysis:
    def __init__(self, model_name):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.config = AutoConfig.from_pretrained(model_name)
        self.model = AutoModelForSequenceClassification.from_pretrained(model_name)
        device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model = (self.model).to(device)

    def analyze_sentiment(self, text):
        try:
            encoded_input = self.tokenizer(text, return_tensors='pt')
            output = self.model(**encoded_input)
            scores = output.logits.squeeze().detach().numpy()
            scores = softmax(scores)

            ranking = np.argsort(scores)
            ranking = ranking[::-1]
            results = []
            for i in range(scores.shape[0]):
                l = self.config.id2label[ranking[i]]
                s = scores[ranking[i]]
                results.append(dict(label=l, score=s))

            return results

        except RuntimeError as e:
            print(f"RuntimeError: {e}")
            # Handle the error gracefully, you can return a default result or take appropriate action.
            return [{"label": "Error", "score": 0.0}]

