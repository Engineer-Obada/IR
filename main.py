import string
from textwrap import wrap
from tkinter import Tk, Label, Text, Button, Entry
from operator import itemgetter
import tkinter as tk


from tkinter import *
from turtle import pd

from nltk import LancasterStemmer, word_tokenize
from nltk.corpus import stopwords
from scipy import spatial
from dot_product import  dot_product
# from calculate_cosine import calculate_cosine
from length import length

from read_documents import read_documents
from read_mappings import read_mappings

from read_queries import read_queries
from vectorize import vectorize

# -----------------------------------------------------

documents = read_documents()
queries = read_queries()
mappings = read_mappings()

# # ----------------------------------------------------
def get_terms(text):
    stoplist = set(stopwords.words('english'))
    terms = {}
    st = LancasterStemmer()
    word_list = [st.stem(word) for word in word_tokenize(text.lower())
                 if not word in stoplist and not word in string.punctuation]
    for word in word_list:
        terms[word] = terms.get(word, 0) + 1
    return terms
doc_terms = {}
qry_terms = {}
for doc_id in documents.keys():
    doc_terms[doc_id] = get_terms(documents.get(doc_id))
for qry_id in queries.keys():
    qry_terms[qry_id] = get_terms(queries.get(qry_id))
# -------------------------------------------------
def collect_vocabulary():
    all_terms = []
    for doc_id in doc_terms.keys():
        for term in doc_terms.get(doc_id).keys():
            all_terms.append(term)
    for qry_id in qry_terms.keys():
        for term in qry_terms.get(qry_id).keys():
            all_terms.append(term)
    return sorted(set(all_terms))
all_terms = collect_vocabulary()

doc_vectors = vectorize(doc_terms, all_terms)
qry_vectors = vectorize(qry_terms, all_terms)
# --------------------------------------------------
def find_key(input_dict, value):
    return next((k for k, v in input_dict.items() if v == value), None)

# --------------------------------------------------
def calculate_cosine(query, document):
    cosine =dot_product(query, document) / (length(query) * length(document))
    return cosine

def search():
    input = someFunction()
    keey = find_key(queries, input)
    query = qry_vectors.get(keey)
    results = {}
    for doc_id in doc_vectors.keys():
        document = doc_vectors.get(doc_id)
        cosine = calculate_cosine(query, document)
        results[doc_id] = cosine
    retrived = []
    for items in sorted(results.items(), key=itemgetter(1), reverse=True)[:10]:
        retrived.append(items[0])
    output1 = Label(root,text=retrived).place(x=470, y=50,width=300)
    scroll_bar = Scrollbar(root)


    i=70
    for k in retrived:
        x = documents.get(k)
        output2 = Label(root, text=x,wraplength=600).place(x=470, y=i)
        i+=80
    precision_all = 0.0
    found_all = 0.0
    s=[]
    s.append(keey)
    for query_id in s:
        gold_standard = mappings.get(str(query_id))
        query = qry_vectors.get(str(query_id))
        results = {}
        model_output = []
        for doc_id in prefiltered_docs.get(str(query_id)):
            document = doc_vectors.get(doc_id)
            cosine = calculate_cosine(query, document)
            results[doc_id] = cosine
        for items in sorted(results.items(), key=itemgetter(1),
                            #                         reverse=True)[:min(40, len(gold_standard))]:
                            # reverse=True)[:min(3, len(gold_standard))]:
                            reverse=True)[:]:
            model_output.append(items[0])

        precision = calculate_precision(model_output, gold_standard)
        recall = calculate_recall(model_output, gold_standard)
        precision_10 = calculate_precision_10(model_output, gold_standard)
        found = calculate_found(model_output, gold_standard)
        output4 = Label(root, text="precision:").place(x=15, y=250)
        output3 = Label(root, text=precision).place(x=85, y=250)

        output4 = Label(root, text="recall:").place(x=15, y=290)
        output3 = Label(root, text=recall).place(x=85, y=290)

        output4 = Label(root, text="precision_10:").place(x=15, y=320)
        output3 = Label(root, text=precision_10).place(x=95, y=320)

        rank_all = 0.0
        ss = []
        ss.append(keey)
        for query_id in ss:
            gold_standard = mappings.get(str(query_id))
            query = qry_vectors.get(str(query_id))
            results = {}
            for doc_id in doc_vectors.keys():
                document = doc_vectors.get(doc_id)
                cosine = calculate_cosine(query, document)
                results[doc_id] = cosine
            sorted_results = sorted(results.items(), key=itemgetter(1), reverse=True)
            index = 0
            found = False
            while found == False:
                item = sorted_results[index]
                index += 1
                if index == len(sorted_results):
                    found = True
                if item[0] in gold_standard:
                    found = True
                    MRR = float(1) / float(index)
                    rank_all += float(1) / float(index)

                    output4 = Label(root, text="MRR:").place(x=15, y=350)
                    output3 = Label(root, text=MRR).place(x=95, y=350)




# ----------------------------------------------------------------------------------


def prefilter(doc_terms, query):
    docs = []
    for doc_id in doc_terms.keys():
        found = False
        i = 0
        while i<len(query.keys()) and not found:
            term = list(query.keys())[i]
            if term in doc_terms.get(doc_id).keys():
                docs.append(doc_id)
                found=True
            else:
                i+=1
    return docs

docs = prefilter(doc_terms, qry_terms.get("6"))
print(docs[:100])
print(len(docs))

prefiltered_docs = {}
for query_id in mappings.keys():
    prefiltered_docs[query_id] = prefilter(doc_terms, qry_terms.get(str(query_id)))

def calculate_precision(model_output, gold_standard):
    true_pos = 0
    for item in model_output:
        if item in gold_standard:
            true_pos += 1
    return float(true_pos) / float(len(model_output))


def calculate_recall(model_output, gold_standard):
    true_pos = 0
    for item in model_output:
        if item in gold_standard:
            true_pos += 1
    return float(true_pos) / float(len(gold_standard))


def calculate_precision_10(model_output, gold_standard):
    true_pos = 0
    for item in model_output:
        if item in gold_standard:
            true_pos += 1
    return true_pos / 10


def calculate_found(model_output, gold_standard):
    found = 0
    for item in model_output:
        if item in gold_standard:
            found = 1
    return float(found)


precision_all = 0.0
found_all = 0.0
s = ['1', '2']
# for query_id in s:
#     gold_standard = mappings.get(str(query_id))
#     query = qry_vectors.get(str(query_id))
#     results = {}
#     model_output = []
#     for doc_id in prefiltered_docs.get(str(query_id)):
#         document = doc_vectors.get(doc_id)
#         cosine = calculate_cosine(query, document)
#         results[doc_id] = cosine
#     for items in sorted(results.items(), key=itemgetter(1),
#                         #                         reverse=True)[:min(40, len(gold_standard))]:
#                         # reverse=True)[:min(3, len(gold_standard))]:
#                         reverse=True)[:]:
#         model_output.append(items[0])
#
#     precision = calculate_precision(model_output, gold_standard)
#     recall = calculate_recall(model_output, gold_standard)
#     precision_10 = calculate_precision_10(model_output, gold_standard)
#     found = calculate_found(model_output, gold_standard)
#
#     print(f"{str(query_id)}:precision {str(precision)}")
#     print(f"{str(query_id)}:recall {str(recall)}")
#     print(f"{str(query_id)}:precision_10 {str(precision_10)}")
#
#     #     print(model_output)
#
#     precision_all += precision
#     found_all += found
# print(precision_all / float(len(s)))
# print(found_all / float(len(mappings.keys())))

# # -----------------------------------------------------------------------------------
# # ---------------------------------wordembing--------------------------------------------------

# import spacy
# nlp = spacy.load("en_core_web_sm")
# vector_wordembding = []
# for doc in documents:
#     a = get_terms(documents.get(doc))
#     doc_to_string = ' '.join(a)
#     document_embadding = list(nlp(doc_to_string).vector)
#     vector_wordembding.append(document_embadding)
#
# import spacy
# nlp = spacy.load("en_core_web_sm")
# a = get_terms(documents.get("1"))
# b = get_terms(queries.get("1"))
# # doc_to_string = ' '.join(a)
# query_to_string = ' '.join(b)
# # document_embadding = list(nlp(doc_to_string).vector)
# query_embadding = list(nlp(query_to_string).vector)
# # similarity = 1 - spatial.distance.cosine(document_embadding, query_embadding)
# print(len(vector_wordembding))
#
#
# from operator import itemgetter
#
# results = {}
#
# for doc in range(len(vector_wordembding)):
#     document_embadding = vector_wordembding[doc]
#     cosine = 1 - spatial.distance.cosine(document_embadding, query_embadding)
#     results[doc] = cosine
#
# for items in sorted(results.items(), key=itemgetter(1), reverse=True)[:10]:
#     print(items[0])

# ---------------------------------------------------------------------------------------

def someFunction():
    text = name_var .get()
    return text


root = Tk()
root.geometry("800x600")
root.title("IR")
name_var=tk.StringVar()

input1 = Entry(root, width=50,textvariable=name_var).place(x=5, y=0,height=70)
B = Button(root, text="search", font=("Arial Bold", 10),command=search).place(x=320, y=0)



lable1 = Label(root, text="correct query", font=("Arial Bold", 10)).place(x=5, y=100)

correctQuery = Entry(root).place(x=5, y=150)


lable1 = Label(root, text="result", font=("Arial Bold", 10)).place(x=380, y=0)

# lable2 = Message(root, text="retrived", justify=LEFT).place(x=470, y=0, width=300, height=300)




root.mainloop()