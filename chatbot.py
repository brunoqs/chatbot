import os
import time
import random
import string
import warnings
import nltk

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# Configuração para ignorar warnings
warnings.filterwarnings('ignore')

# Saudações
GREETING_INPUTS = ['ola', 'oi', 'opa', 'eae']
GREETING_RESPONSES = ['ola', 'oi', 'opa', 'eae']


class Chatbot:
    """
    Representa a entidade do chatbot
    """
    def __init__(self):
        """
        Instancia o objeto configurado para português.
        """
        self.stopwords = nltk.corpus.stopwords.words('portuguese')
        self.remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)
        self.lemmer = nltk.stem.WordNetLemmatizer()

        self.sent_tokens = []
        self.sent_tokens.extend(self.load_sentences('corpora/tecnologia/'))
        self.sent_tokens.extend(self.load_sentences('corpora/mercado/'))
        self.sent_tokens.extend(self.load_sentences('corpora/telefonia/'))
        self.sent_tokens.extend(self.load_sentences('corpora/saude/'))
        
    def load_sentences(self, corpus_dir: str) -> list:
        """
        Carrega as sentenças dos corpora.

        :param corpus_dir: Caminho do diretório dos corpora, terminado com 
        :return: Lista com todas as sentenças
        """
        all_sentences = []
        for file_path in os.listdir(corpus_dir):
            with open(corpus_dir + file_path) as fp:
                for line in fp:
                    sentences = nltk.sent_tokenize(line)
                    all_sentences.extend(sentences)
        return all_sentences

    def lem_tokens(self, tokens: list) -> list:
        """
        Lematiza os tokens.

        :param tokens: Lista com tokens
        :return: Lista com tokens lematizados
        """
        return [self.lemmer.lemmatize(token) for token in tokens]

    def lem_normalize(self, text: str) -> list:
        """
        Normaliza o texto gerando lista de tokens.

        :param text: Texto qualquer de entrada
        :return: Lista de tokens normalizados
        """
        return self.lem_tokens(nltk.word_tokenize(text.lower().translate(self.remove_punct_dict)))

    def greeting(self, sentence: str) -> str:
        """
        Gera resposta para cumprimento.

        :param sentence: Sentença de entrada
        :return: Resposta de cumprimento se identificada saudação
        """
        for word in sentence.split():
            if word.lower() in GREETING_INPUTS:
                return random.choice(GREETING_RESPONSES)
        return ''

    def response(self, user_request: str) -> str:
        """
        Gera resposta para pergunta feita.

        :param user_request: Pergunta de entrada
        :return: Resposta se for possível respondê-la
        """
        request = ' '.join(self.lem_normalize(user_request))
        self.sent_tokens.append(request)
        
        tfidf_vec = TfidfVectorizer(tokenizer=self.lem_normalize, stop_words=self.stopwords)
        tfidf = tfidf_vec.fit_transform(self.sent_tokens)
        
        vals = cosine_similarity(tfidf[-1], tfidf)
        
        idx = vals.argsort()[0][-2]        
        flat = vals.flatten()
        flat.sort()
        
        req_tfidf = flat[-2]
        
        self.sent_tokens.pop()

        if(req_tfidf == 0):
            return 'Desculpe, não consigo entender essa pergunta.'
        else:
            return self.sent_tokens[idx]
