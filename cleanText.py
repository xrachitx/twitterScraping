import json
import pandas as pd
import re
import lxml
import nltk
from bs4 import BeautifulSoup
from nltk.tokenize import word_tokenize
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer,PorterStemmer 
nltk.download('wordnet')

def decodeHTML(data):
    data = BeautifulSoup(data,"lxml").text
    return data

def normaliseTextToLower(data):
    return data.lower()

def tokenizeAndPunctuationRemoval(data):
    tokenizedList=[token for token in RegexpTokenizer('\w+').tokenize(data)]
    return tokenizedList

def removeNumbers(dataList):
    dataListRefined = [token for token in dataList if not (token.isnumeric())]
    return dataListRefined

def removeStopWords(dataList): 
    dataList = list(set(dataList))
    stopWords = set(stopwords.words("english"))
    nonStoppedWords = list(token for token in dataList if token not in stopWords)
    return nonStoppedWords

def wordLemmatizer(dataList):
    lemmatizer = WordNetLemmatizer()
    lemmatizedText = [lemmatizer.lemmatize(token) for token in dataList]
    return lemmatizedText

def stemming(dataList):
    stemmer = PorterStemmer()
    return " ".join([stemmer.stem(token) for token in dataList])


def cleanData(data):
    data = data.lower()
    tokenizedList=[token for token in RegexpTokenizer('\w+').tokenize(data)]
    dataList = [token for token in tokenizedList if not (token.isnumeric())]
    stopWords = set(stopwords.words("english"))
    nonStoppedWords = list(token for token in dataList if token not in stopWords)
    lemmatizer = WordNetLemmatizer()
    lemmatizedText = [lemmatizer.lemmatize(token) for token in nonStoppedWords]
    # stemmer = PorterStemmer()
    return " ".join(lemmatizedText)


if __name__ == "__main__":
    f = open('./data/moddedData.json',)
    data = json.load(f)
    # print(data)
    for i in data:
        print(i)
        data[i]["text"] = cleanData(data[i]["text"])
        print(data[i])
    with open('./data/cleanData.json', 'w') as fp:
        json.dump(data, fp)