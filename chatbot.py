import io
import os
import random
import string
import warnings
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import warnings
import nltk
from nltk.stem import WordNetLemmatizer


GREETING_INPUTS = ("ola", "oi", "como vai",)
GREETING_RESPONSES = ["ola", "oi", "100%", ]

class Chatbot:

    def __init__(self):
        nltk.download('popular', quiet=True)

        self.sent_tokens = []
        self.stopwords = nltk.corpus.stopwords.words('portuguese')
        self.remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)
        self.lemmer =  WordNetLemmatizer()

        self.sent_tokens.extend(self.load_sentences('corpora/tecnologia/'))
        self.sent_tokens.extend(self.load_sentences('corpora/mercado/'))
        self.sent_tokens.extend(self.load_sentences('corpora/telefonia/'))
        self.sent_tokens.extend(self.load_sentences('corpora/saude/'))
        
    def load_sentences(self, corpus_dir):   
        all_sentences = []
        for file_path in os.listdir(corpus_dir):
            with open(corpus_dir + file_path) as fp:
                for line in fp:
                    sentences = nltk.sent_tokenize(line)
                    all_sentences.extend(sentences)
        return all_sentences

    def lem_tokens(self, tokens):
        return [self.lemmer.lemmatize(token) for token in tokens]

    def lem_normalize(self, text):
        return self.lem_tokens(nltk.word_tokenize(text.lower().translate(self.remove_punct_dict)))

    def greeting(self, sentence):
        for word in sentence.split():
            if word.lower() in GREETING_INPUTS:
                return random.choice(GREETING_RESPONSES)

    def response(self, user_request):
        robo_response = ''
        self.sent_tokens.append(user_request)
        TfidfVec = TfidfVectorizer(tokenizer=self.lem_normalize, stop_words=self.stopwords)
        tfidf = TfidfVec.fit_transform(self.sent_tokens)
        vals = cosine_similarity(tfidf[-1], tfidf)
        idx = vals.argsort()[0][-2]
        flat = vals.flatten()
        flat.sort()
        req_tfidf = flat[-2]
        if(req_tfidf == 0):
            robo_response = robo_response + "Desculpe, não consigo entender essa pergunta"
            return robo_response
        else:
            robo_response = robo_response + self.sent_tokens[idx]
            return robo_response