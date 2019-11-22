########################################################################
#                             Vansh Sethi                              #
#            Extractive Approach using Unsupervised Learning &         #
#                     Natural Language Processing                      #
########################################################################

import bs4 as BeautifulSoup #Webscrapping and getting article that user requests to be summarized
import urllib.request
from nltk.corpus import stopwords #data processing to get rid of unncessary words ("the", "and" etc.)
from nltk.stem import PorterStemmer #reducing words into root from (ex. Fighter, Fighting, Fought ----> Fight)
from nltk import word_tokenize, sent_tokenize #used in data processing to make data into list
import nltk
from flask import Flask
import json

app = Flask(__name__)

########################################################################
####                      1. Getting Data                           ####
########################################################################
'''
@app.route('/getmethod/<data>',methods=['POST'])
def x(data):
    x = _run_article_summary(data)
    response = app.response_class(
        response=json.dumps(x),
        status=200,
        mimetype='application/json'
    )
    return response
'''

'''
os.chdir("..\..\..")
path = "Users/vansh/Desktop/TextSummarizerWebApplication/Website/br.txt"
f = open(path,'r+')
article_content = f.read()
'''

#USED WHEN USING CONSOLE
'''
if (x.lower() == 'link'):
    stop_words = set(stopwords.words('english'))
    articleprompt = input('Insert Wikipedia Link Here: ')

    article = urllib.request.urlopen(articleprompt)

    article_data = article.read()

    article_parsed = BeautifulSoup.BeautifulSoup(article_data,'html.parser')

    # Returning <p> tags
    paragraphs = article_parsed.find_all('p')

    article_content = ''

    # Looping through the paragraphs and adding them to the variable
    for p in paragraphs:  
        article_content += p.text
else:
    articleprompt = input('Insert Text Here: ')
    article_content = articleprompt

#Arbritray value that determines how many sentences you will get (Should change to sentences)
potency = int(input("Insert Potency—how much summary—Value Here: "))
'''


########################################################################
####            2. Processing Data & Word Frequency Table           ####
########################################################################
def dictionary_table(text_to_be_summarised) -> dict:

    #List containing all uneccary words to filter them out
    stop_words = set(stopwords.words('english'))
    
    #Breaks up text into list of indexed words
    words = word_tokenize(text_to_be_summarised)

    #Function to reduce words into root form
    stem = PorterStemmer()

    #Dictionary Word Frequency Table (Unsupervised A.I. Part)
    frequency_table = dict()
    for word in words:

        word = stem.stem(word) #Putting word into root form
        
        #if it's a stop word, get rid of it and move on to next word
        if word in stop_words:
            continue

        #Add one to occurence of current word
        if word in frequency_table:
            frequency_table[word] += 1

        #Never seen before word, make an occurence value for it and sent it to 1    
        else:
            frequency_table[word] = 1    


    #sending back table with common words
    return frequency_table


########################################################################
####         3. Calculating most Important Sentences in Data        ####
########################################################################

def importance_of_sentence(sentences,frequency_table) -> dict:
    sentence_importance = dict()

    for sentence in sentences:
        sentence_wordcount = (len(word_tokenize(sentence)))
        sentence_wordcount_without_stopwords = 0
        for word_weight in frequency_table:
            if word_weight in sentence.lower():
                sentence_wordcount_without_stopwords += 1
                if sentence[:7] in sentence_importance:
                    sentence_importance[sentence[:7]] += frequency_table[word_weight]
                else:
                    sentence_importance[sentence[:7]] = frequency_table[word_weight]

        sentence_importance[sentence[:7]] = sentence_importance[sentence[:7]]         
      
    return sentence_importance

#I use the number 7 to shorten the length of the sentence in the dictionary... just for simplicity

########################################################################
####   4. Filtering out the least Important Sentences Via Average   ####
########################################################################

def _calculate_average_score(sentence_weight) -> int:
   
    # Calculating the average score for the sentences
    sum_values = 0
    for entry in sentence_weight:
        sum_values += sentence_weight[entry]

    # Getting sentence average value from source text
    average_score = (sum_values / len(sentence_weight))

    return average_score

########################################################################
####    5.Putting Everything Together for Summary (Running Model)   ####
########################################################################
def _get_article_summary(sentences, sentence_weight, threshold):
    sentence_counter = 0
    article_summary = ''

    for sentence in sentences:
        if sentence[:7] in sentence_weight and sentence_weight[sentence[:7]] >= (threshold):
            article_summary += " " + sentence
            sentence_counter += 1

    return article_summary


########################################################################
####           6.Executable Code of the Defined Functions           ####
########################################################################

def _run_article_summary(article):
    
    #creating a dictionary for the word frequency table
    frequency_table = dictionary_table(article)

    #tokenizing the sentences
    sentences = sent_tokenize(article)

    #algorithm for scoring a sentence by its words
    sentence_scores = importance_of_sentence(sentences, frequency_table)

    #getting the threshold
    threshold = _calculate_average_score(sentence_scores)

    #producing the summary
    article_summary = _get_article_summary(sentences, sentence_scores, 2 * threshold)
    

    return article_summary



