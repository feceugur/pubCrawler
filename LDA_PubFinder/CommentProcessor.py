import pandas as pd
from LDA_PubFinder.LDAModel import LDATopicModeling

class DataProcessor:
    def __init__(self, get_all, data_path="data.csv", n=1000, random_state=42):
        if get_all:
            self.data = pd.read_csv(data_path)
        else:
            self.data = pd.read_csv(data_path).sample(n=n, random_state=random_state)
        self.result_df = pd.DataFrame(columns=['place_name', 'VADER_score', 'topic', 'comment'])
        self.lda_model = LDATopicModeling(dev_mode=True)

    def process_data(self):
        self.data["preprocess_fda_text"] = self.data["text"].apply(lambda x: self.lda_model.preprocess_fda(x))
        df = pd.DataFrame(columns=['place_name', 'vader_score', 'topic', 'text'])
        for place_name, grouped_data in self.data.groupby('place_name'):
            grouped_data["topic"] = grouped_data["preprocess_fda_text"].apply(lambda x: self.lda_model.get_comments_with_topics(x))

            grouped_data["vader_score"] = grouped_data["text"].apply(lambda x: self.lda_model.calculate_vader_score(x)["vader_score"])

            grouped_data = grouped_data[['place_name', 'vader_score', 'topic', 'text']]
            df = df._append(grouped_data)
        df.to_csv("processed_data.csv", index=False)



if __name__ == '__main__':
    import ssl
    try:
        _create_unverified_https_context = ssl._create_unverified_context
    except AttributeError:
        pass
    else:
        ssl._create_default_https_context = _create_unverified_https_context


    DataProcessor(get_all=True, data_path="data.csv",
                  n=2000,
                  random_state=42).process_data()