#pip install -U spacy
#python -m spacy download en_core_web_sm
#pip install transformers
#pip install torch

import spacy
import os
import operator
import json

import pandas as pd


from Document_Index_Maker import open_browser
from selenium.webdriver.common.by import By

from rank_bm25 import BM25Okapi
from transformers import AutoTokenizer, AutoModelForQuestionAnswering, QuestionAnsweringPipeline

if __name__ == "__main__":

#Question Input
    SPACY_MODEL = os.environ.get('SPACY_MODEL', 'en_core_web_sm')
    QA_MODEL = os.environ.get('QA_MODEL', 'distilbert-base-cased-distilled-squad')
    nlp = spacy.load(SPACY_MODEL, disable=['ner', 'parser', 'textcat'])

    words_to_keep = None or {'PROPN', 'NUM', 'VERB', 'NOUN', 'ADJ'}

    text = input("Ask a Question :")


#Document Retrieval
####################################################################################
    tmp = nlp(text)
    final_question = " ".join(x.text for x in tmp if x.pos_ in words_to_keep)

    word_list = [x.replace(x, "(?=.*" + x + ")") for x in final_question.split()]

    regex_and = ' '.join(word_list)
    regex_or = '|'.join(final_question.split(" "))

    doc_dataframe = pd.read_excel("Document_Index_List.xlsx")
    link_list = list(doc_dataframe[doc_dataframe['Description'].str.lower().str.contains(regex_and)]['Links'])
    if len(link_list) == 0:
        link_list = list(doc_dataframe[doc_dataframe['Description'].str.lower().str.contains(regex_or)]['Links'])

    documents = []
    browser = open_browser()
    for link in link_list:
        browser.get(link)
        documents.append(browser.find_element(By.CLASS_NAME, "c-column-blog-post-body").text)

    browser.close()
    points = [paragraph for text in documents for paragraph in text.split("\n")]

#Content Selection
#################################################################################################
    tokenize = lambda text: [token.lemma_ for token in nlp(text)]

    tmp_points = [tokenize(x) for x in points]
    tmp_question = text.split(" ")

    passage_selection = BM25Okapi(tmp_points)

    final_selection = passage_selection.get_top_n(tmp_question, points, n=10)

#Extracting Answer
###################################################################################################
Pre_trained_model = AutoModelForQuestionAnswering.from_pretrained(QA_MODEL)
Pre_trained_tokens = AutoTokenizer.from_pretrained(QA_MODEL)
nlp = QuestionAnsweringPipeline(model=Pre_trained_model, tokenizer=Pre_trained_tokens)
final_answer = []
for dot in final_selection:
    reply = nlp(question=text, context=dot)
    reply['text'] = dot
    final_answer.append(reply)

final_answer.sort(reverse=True, key=operator.itemgetter("score"))

json = json.dumps(final_answer, indent=4)
file = open("Final_Answer.json", "w")
file.write(json)
file.write("===============================================\nLink_List")
file.close()

print("Your answer has been saved as \"Final_Answer.json\"")