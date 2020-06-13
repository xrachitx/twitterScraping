import json
import pandas as pd
import re
import lxml
import nltk
from bs4 import BeautifulSoup
from nltk.tokenize import word_tokenize
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords

def decodeHTML(data):
    data = BeautifulSoup(data,"lxml").text
    return data

def normaliseTextToLower(data):
    return data.lower()

def tokenizeAndPunctuationRemoval(data):
    tokenizedList=[]
    for token in RegexpTokenizer('\w+').tokenize(data):
        tokenizedList.append(token)
    return tokenizedList

def removeNumbers(dataList):
    dataListRefined = []
    for token in dataList:
        if not (token.isnumeric()):
            dataListRefined.append(token)
    # print("HELO")
    return dataListRefined

def removeStopWords(dataList): #stopwords are words like "the", "in" etc
    dataList = list(set(dataList))
    stopWords = set(stopwords.words("english"))
    nonStoppedWords = list(token for token in dataList if token not in stopWords)
    convertToText = " ".join(nonStoppedWords)
    return convertToText

def cleanData(data):
    return (removeStopWords(removeNumbers(tokenizeAndPunctuationRemoval(normaliseTextToLower(decodeHTML(data))))))


if __name__ == "__main__":
    f = open('./data/moddedData.json',)
    data = json.load(f)
    d = {}
    cnt = 0
    for i in data:
        cnt+=1
        finData = []
        textData = data[i]['0']
        finData.append(data[i]['1'])
        finData.append(data[i]['2'])
        finData.append(cleanData(textData))
        d[cnt] = finData
    with open('./data/cleanData.json', 'w') as fp:
        json.dump(d, fp)