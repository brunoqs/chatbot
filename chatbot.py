import io
import os
import random
import string # to process standard python strings
import warnings
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import warnings
warnings.filterwarnings('ignore')

import nltk
from nltk.stem import WordNetLemmatizer
nltk.download('popular', quiet=True) # for downloading packages

# uncomment the following only the first time
#nltk.download('punkt') # first-time use only
#nltk.download('wordnet') # first-time use only


#Reading in the corpus
def load_sentences(corpus_dir):   
    all_sentences = []
    for file_path in os.listdir(corpus_dir):
        with open(corpus_dir + file_path) as fp:
            for line in fp:
                # line = normalizer.to_lowercase(line)
                sentences = nltk.sent_tokenize(line)
                # sentences = [normalizer.tokenize_words(sent) for sent in sentences]
                all_sentences.extend(sentences)
    return all_sentences

#TOkenisation
sent_tokens = []
sent_tokens.extend(load_sentences('corpora/tecnologia/'))
sent_tokens.extend(load_sentences('corpora/mercado/'))
sent_tokens.extend(load_sentences('corpora/telefonia/'))
sent_tokens.extend(load_sentences('corpora/saude/'))

stopwords = nltk.corpus.stopwords.words('portuguese')

# Preprocessing
lemmer = WordNetLemmatizer()
def LemTokens(tokens):
    return [lemmer.lemmatize(token) for token in tokens]
remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)
def LemNormalize(text):
    return LemTokens(nltk.word_tokenize(text.lower().translate(remove_punct_dict)))


# Keyword Matching
GREETING_INPUTS = ("ola", "oi", "como vai",)
GREETING_RESPONSES = ["ola", "oi", "100%", ]

def greeting(sentence):
    """If user's input is a greeting, return a greeting response"""
    for word in sentence.split():
        if word.lower() in GREETING_INPUTS:
            return random.choice(GREETING_RESPONSES)


# Generating response
def response(user_response):
    robo_response=''
    sent_tokens.append(user_response)
    TfidfVec = TfidfVectorizer(tokenizer=LemNormalize, stop_words=stopwords)
    tfidf = TfidfVec.fit_transform(sent_tokens)
    vals = cosine_similarity(tfidf[-1], tfidf)
    idx=vals.argsort()[0][-2]
    flat = vals.flatten()
    flat.sort()
    req_tfidf = flat[-2]
    if(req_tfidf==0):
        robo_response=robo_response+"Desculpe, não consigo entender essa pergunta"
        return robo_response
    else:
        robo_response = robo_response+sent_tokens[idx]
        return robo_response


flag=True
print("BOT: Olá querido usuário, fico a disposição para responder perguntas sobre mercado, saúde, tecnologia e telefonia. Diga tchau quando encerrar!")
while(flag==True):
    user_response = input('Pergunta: ')
    user_response=user_response.lower()
    if(user_response!='tchau'):
        if(user_response=='obrigado' or user_response=='muito obrigado' ):
            flag=False
            print("BOT: Não há de que...")
        else:
            if(greeting(user_response)!=None):
                print("BOT: "+greeting(user_response))
            else:
                print("BOT: Pensando...")
                print("BOT: " + response(user_response))
                sent_tokens.remove(user_response)
    else:
        flag=False
        print("BOT: Até mais...")    