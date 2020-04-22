import os
import pickle
import feather
import numpy as np
import pandas as pd
import scipy
import json
from flask import request
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer

from helpers import textcount
from helpers import clean

#################################################################################
# inital
#################################################################################

np.random.seed(37)

count_vect = CountVectorizer()
tfidf_transformer = TfidfTransformer()

dataLoad = pd.DataFrame()
debugging = True


#################################################################################
# load data
#################################################################################

def load_data(project, text, sentiment):
    """ copy data from local system to api server into working directory.

    Parameters
    ----------
    project : str
        name of the project
    text    : str
        column with the text of the source
    sentiment : str
        column with the sentiment of the source

    """
    try:
        if debugging:
            print('### Load Data ###')
           # print('file directory: ' + os.path.abspath("."))


        file = request.files.get('file')
        df = pd.read_csv(file)
        print(df.count())
        df = df.reindex(np.random.permutation(df.index))
        df = df[[text, sentiment]]
        feather.write_dataframe(df, '../working/' + project + '/' + project + '_raw.feather')
    except:
        return 'Error'
    else:
        return 'Data Successful loaded'


#################################################################################
# exploration
#################################################################################

def exploartion_data(project):
    """ function to get data insights

    Parameters
    ----------
    project : str
        name of the project
    """
    if debugging:
        print('### Exploration Data ###')
    df = pd.read_feather('../working/' + project + '/' + project + '_raw.feather')  # with api

    counts = textcount.TextCounts()
    x = counts.fit_transform(df.text)
    x['airline_sentiment'] = df.airline_sentiment

    feather.write_dataframe(x, '../working/' + project + '/' + project + '_exploration.feather')


#################################################################################
# preprocessing
#################################################################################

def clean_data(project):
    """ clean data (remove stopwords, punctation, stemming)

    Parameters
    ----------
    project : str
        name of the project
    """
    if debugging:
        print('### Clean Data ###')

    df = pd.read_feather('../working/' + project + '/' + project + '_raw.feather')

    clean_text = clean.Clean()
    t = clean_text.fit_transform(df.text)

    empty_clean = t == ''
    t.loc[empty_clean] = '[no_text]'

    clean_data = pd.DataFrame(t)
    clean_data['sentiment'] = df.airline_sentiment

    feather.write_dataframe(clean_data, '../working/' + project + '/' + project + '_clean.feather')

    if debugging:
        print('{} records have no words left after text cleaning'.format(t[empty_clean].count()))


#################################################################################
# vectorize
#################################################################################

def vectorize_data(project):
    """ vectorize data (tf-idf)

    Parameters
    ----------
    project : str
        name of the project
    """
    if debugging:
        print('### Vectorize Data ###')

    clean_data = pd.read_feather('../working/' + project + '/' + project + '_clean.feather')

    word_count = count_vect.fit_transform(clean_data.text)
    vectors = tfidf_transformer.fit_transform(word_count)

    scipy.sparse.save_npz('../working/' + project + '/' + project + '_vectors.npz', vectors)
    pickle.dump(count_vect.vocabulary_, open('../working/' + project + '/' + project + '_countVec.p', 'wb'))
    pickle.dump(tfidf_transformer.idf_, open('../working/' + project + '/' + project + '_tfidf_trans.p', 'wb'))


#################################################################################
# learn one Model
#################################################################################

def model_data(project, model):
    """ learn model

    Parameters
    ----------
    project : str
        name of the project
    model : str
        name of the model algorithm
    """
    if debugging:
        print('### Modle Data ###')


    clean_data = pd.read_feather('../working/' + project + '/' + project + '_clean.feather')
    vectors = scipy.sparse.load_npz('../working/' + project + '/' + project + '_vectors.npz')
    count_vect.vocabulary_ = pickle.load(open('../working/' + project + '/' + project + '_countVec.p', 'rb'))
    tfidf_transformer.idf_ = pickle.load(open('../working/' + project + '/' + project + '_tfidf_trans.p', 'rb'))



    if model == 'MNB':
        from sklearn.naive_bayes import MultinomialNB
        clf = MultinomialNB().fit(vectors, clean_data.sentiment)
        pickle.dump(clf, open('../working/' + project + '/' + project + '_multinomial_nb.p', 'wb'))

    if model == 'LR':
        from sklearn.linear_model import LogisticRegression
        logreg = LogisticRegression().fit(vectors, clean_data.sentiment)
        pickle.dump(logreg, open('../working/' + project + '/' + project + '_logistic_regression.p', 'wb'))


#################################################################################
# prediction
#################################################################################

def prediction_data(project, model, text):
    """

    Parameters
    ----------
    project : str
        name of the project
    model : str
        name of the model algorithm
    text : str
        text to predict sentiment

    Returns
    -------

    """
    if debugging:
        print('### predict function')

    count_vect.vocabulary_ = pickle.load(open('../working/' + project + '/' + project + '_countVec.p', 'rb'))
    tfidf_transformer.idf_ = pickle.load(open('../working/' + project + '/' + project + '_tfidf_trans.p', 'rb'))

    if model == 'MNB':
        clf = pickle.load(open('../working/' + project + '/' + project + '_multinomial_nb.p', 'rb'))
        snipped = count_vect.transform([text])
        to_predict = tfidf_transformer.transform(snipped)
        predicted = clf.predict(to_predict)

    if model == 'LR':
        logreg = pickle.load(open('../working/' + project + '/' + project + '_logistic_regression.p', 'rb'))
        snipped = count_vect.transform([text])
        to_predict = tfidf_transformer.transform(snipped)
        predicted = logreg.predict(to_predict)

    if debugging:
       print(predicted)
    return json.dumps(predicted.tolist())
