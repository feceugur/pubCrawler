import gensim
from gensim import corpora
from gensim.models import CoherenceModel
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords, wordnet as wn
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.util import ngrams
from nltk import word_tokenize
import string
import pyLDAvis
import pyLDAvis.gensim_models
import networkx as nx
import nltk
import liwc
import urllib.request
from nltk.sentiment import SentimentIntensityAnalyzer


class LDATopicModeling:
    def __init__(self, dev_mode=False):
        self.dev_mode=dev_mode
        self.cat_remove = ['funct', 'article', 'preps', 'conj', 'present', 'past', 'auxverb', 'relativ', 'pronoun',
                           'auxverb', 'quant', 'conj', 'ipron', 'article', 'time', 'past', 'cogmech']

        # Tokenization
        self.tokenizer = RegexpTokenizer(r'\w+')
        self.words_ly = [word for word in nltk.corpus.words.words() if word.endswith('ly')]
        self.tagged_words = nltk.pos_tag(nltk.word_tokenize(" ".join(stopwords.words('english'))))
        self.adverbs = [word for word, pos in self.tagged_words if pos == 'RB']
        self.additional_words = {'room', 'hotel', 'like', 'recommended', 'nice', 'price', 'people', 'go', 'really',
                                 'excellent', 'table', 'horrible', 'best', 'bad', 'euro', 'great', 'many', 'excellent',
                                 'went', 'give', 'un', 'met', 'del', 'de', 'la', 'place', 'lol', 'good', 'ever', 'us',
                                 'would', '2024', '2023', 'also', 'back', 'last', 'almost', 'around', 'I', 'am', 'us',
                                 'one', 'much', 'today', 'better', 'is', 'are', 'will', 'a', 'the', 'and', 'in', 'on',
                                 'at', 'to', 'for', 'with', 'it', 'of', 'that', 'this', 'as', 'by', 'from', 'was',
                                 'were',
                                 'an', 'be', 'first', 'day', 'video', 'find', 'watch', 'time', 'episode', 'seen',
                                 'even',
                                 'every', 'gets', 'season', 'made', 'dont', 'new', 'highly', 'homemade', 'lot',
                                 'pretty',
                                 'barrio', 'recommend', 'menu', 'service', 'location', 'food', 'selection',
                                 'atmosphere',
                                 'fast', 'always', 'big', 'option', 'get', 'share', 'group', 'makes', 'some',
                                 'entertaining',
                                 'competition', 'well', 'decorated', 'pretty', 'going', 'here', 'very', 'make', 'you', }
        self.en_stop = set(stopwords.words('english') + list(self.additional_words) + [str(num) for num in range(100)]
                           + self.words_ly + self.adverbs)

        self.sia = SentimentIntensityAnalyzer()
        self.load_liwc()

    def load_liwc(self):
        url_liwc = "https://raw.githubusercontent.com/usc-sail/mica-text-characternetworks/master/LIWC/LIWC2007_English131104.dic"
        infile = urllib.request.urlopen(url_liwc)
        outfile = open('liwc.dic', 'w')
        outfile.writelines([line.decode("utf-8") for line in infile if not '/' in str(line)])
        outfile.close()

    def calculate_vader_score(self, text):
        parse, _ = liwc.load_token_parser('liwc.dic')
        tokens = self.preprocess(text, vader=True)
        vader_scores = {word: self.sia.polarity_scores(word)['compound'] for word in tokens}
        try:
            vader_score = sum(vader_scores.values()) / len(vader_scores)
        except ZeroDivisionError:
            vader_score = 0

        negative_words = []
        positive_words = []

        for word, score in vader_scores.items():
            if score < -0.3:
                negative_words.append((word, score))
            elif score > 0.1:
                positive_words.append((word, score))


        return {"vader_score": vader_score,
                "negative_words": negative_words,
                "positive_words": positive_words}

    def preprocess(self, text, vader=False):
        text = text.replace('\n\n', '')
        text = text.translate(str.maketrans('', '', string.punctuation))
        tokens = word_tokenize(text.lower())
        if vader:
            stop_words = stopwords.words("english")
        else:
            stop_words = self.en_stop
        tokens = [word for word in tokens if word not in stop_words]
        tokens = [WordNetLemmatizer().lemmatize(word) for word in tokens]
        return tokens

    def preprocess_fda(self, text):
        tokens = self.preprocess(text)
        synsets = [wn.synsets(word) for word in tokens]
        tokens = [word for word, synset in zip(tokens, synsets) if synset and synset[0].pos() not in self.cat_remove]

        for i in range(len(tokens)):
            if tokens[i] == 'not':
                tokens[i] = 'not_' + tokens[i + 1]
                tokens[i + 1] = ''
        tokens = [word for word in tokens if word]
        tokens_lemma = [WordNetLemmatizer().lemmatize(token) for token in tokens]

        n_grams = []
        for n in range(1, 4):
            n_grams.extend([' '.join(gram) for gram in ngrams(tokens_lemma, n)])
        return n_grams

    def find_optimum_topic_number(self, corpus, dictionary, processed_comments):
        coherence_values = []
        for num_topics in range(1, 6):
            if corpus != [[]]:
                lda_model = gensim.models.ldamodel.LdaModel(corpus, num_topics=num_topics, id2word=dictionary, passes=15)
                coherence_model_lda = CoherenceModel(model=lda_model, texts=processed_comments, dictionary=dictionary,
                                                    coherence='c_v')
                coherence_lda = coherence_model_lda.get_coherence()
                coherence_values.append((num_topics, coherence_lda))
        try:
            # Select the optimal number of topics based on coherence scores
            optimal_num_topics = max(coherence_values, key=lambda x: x[1])[0]
        except ValueError:
            optimal_num_topics = 1
        return optimal_num_topics

    def get_comments_with_topics(self, processed_comments):
        dictionary = corpora.Dictionary([processed_comments])
        corpus = [dictionary.doc2bow(text) for text in [processed_comments]]

        if self.dev_mode:
            optimal_num_topics = 3
        else:
            optimal_num_topics = self.find_optimum_topic_number(corpus, dictionary, [processed_comments])

        if corpus != [[]]:
            lda_model_result = gensim.models.ldamodel.LdaModel(corpus,
                                                               num_topics=optimal_num_topics,
                                                               id2word=dictionary,
                                                               passes=15)

            extracted_topics = []
            for topic_idx in range(optimal_num_topics):
                top_words = lda_model_result.show_topic(topic_idx, topn=3)  # Adjust topn as needed
                extracted_topics.append(dict(top_words))
            return extracted_topics