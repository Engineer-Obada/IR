import nltk
import string
from nltk import word_tokenize
from nltk.corpus import stopwords


def process(text):
    stoplist = set(stopwords.words('english'))
    word_list = [word for word in word_tokenize(text.lower())
                 if not word in stoplist and not word in string.punctuation]
    return word_list

