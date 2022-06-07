import nltk
import string
from nltk import word_tokenize, WordNetLemmatizer, pos_tag
from nltk.corpus import stopwords

def process(text):
    stoplist = set(stopwords.words('english'))
    lemmatizer = WordNetLemmatizer()
    pos_list = pos_tag(word_tokenize(text.lower()))
    word_list = [entry for entry in pos_list
                 if not entry[0] in stoplist and not entry[0] in string.punctuation]
    lemmatized_wl = []
    for entry in word_list:
        if entry[1].startswith("V"):
            lemmatized_wl.append(lemmatizer.lemmatize(entry[0], "v"))
        else:
            lemmatized_wl.append(lemmatizer.lemmatize(entry[0]))
    return lemmatized_wl