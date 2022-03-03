from fastapi import FastAPI
from bs4 import BeautifulSoup
import urllib.request
import nltk
import re
import heapq
from random import choice
from parrot import Parrot
from urllib.parse import unquote
import warnings

warnings.filterwarnings("ignore")

app = FastAPI()

user_agent_list = [
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15',
'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0',
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0',
'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36'
]

PARROT_MODEL = None
@app.on_event("startup")
async def startup_event():
    global PARROT_MODEL
    PARROT_MODEL = Parrot(model_tag="prithivida/parrot_paraphraser_on_T5", use_gpu=False)

@app.get("/summarize/", response_model = str)
def getSummaryFromWebsite(url: str, nrSentences: int = 10):
    req = urllib.request.Request(
        unquote(url), 
        data=None, 
        headers={
            'User-Agent': choice(user_agent_list)
        }
    )
    html = urllib.request.urlopen(req).read()
    soup = BeautifulSoup(html)
    
    for script in soup(["script", "style"]):
        script.decompose()

    strips = list(soup.stripped_strings)
    
    strips = list(soup.stripped_strings)
    article_text = ' '.join(strips)
    # Removing Square Brackets and Extra Spaces
    article_text = re.sub(r'[[0-9]*]', ' ', article_text)
    article_text = re.sub(r's+', ' ', article_text)
    # Removing special characters and digits
    formatted_article_text = re.sub('[^a-zA-Z]', ' ', article_text )
    formatted_article_text = re.sub(r's+', ' ', formatted_article_text)

    sentence_list = nltk.sent_tokenize(" ".join(strips))

    # weighted frequencies
    stopwords = nltk.corpus.stopwords.words('english')
    word_frequencies = {}

    for word in nltk.word_tokenize(formatted_article_text):
        if word not in stopwords:
            if word not in word_frequencies.keys():
                word_frequencies[word] = 1
            else:
                word_frequencies[word] += 1
                
    # sentence scores
    sentence_scores = {}
    for sent in sentence_list:
        for word in nltk.word_tokenize(sent.lower()):
            if word in word_frequencies.keys():
                if len(sent.split(' ')) < 30:
                    if sent not in sentence_scores.keys():
                        sentence_scores[sent] = word_frequencies[word]
                    else:
                        sentence_scores[sent] += word_frequencies[word]
                        
    summary_sentences = heapq.nlargest(nrSentences, sentence_scores, key=sentence_scores.get)
    summary = ' '.join(summary_sentences)
    return summary


@app.get("/paraphrase/{sentence}")
def paraphrase(sentence: str):
    global PARROT_MODEL
    para_phrases = PARROT_MODEL.augment(input_phrase=sentence)
    # for para_phrase in para_phrases:
    #     print(para_phrase)
    selection = None
    if para_phrases[0][0] == sentence:
        if len(para_phrases) > 1:
            if para_phrases[0][1] != sentence:
                selection = para_phrases[0][1]
    else:
        selection = para_phrases[0][0]
    return selection