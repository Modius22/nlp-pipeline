import json
import os

import numpy as np
import pandas as pd
from flask import request
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer

import filestore_controller as fc
from helpers import clean
from helpers import textcount

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
      print('file directory: ' + os.path.abspath("."))

    file = request.files.get('file')
    df = pd.read_csv(file)
    df = df.reindex(np.random.permutation(df.index))
    df = df[[text, sentiment]]
    fc.save_feather(df, 'Twitter_raw', project)
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
  df = fc.load_feather('Twitter_raw', project)

  counts = textcount.TextCounts()
  x = counts.fit_transform(df.text)
  x['airline_sentiment'] = df.airline_sentiment

  fc.save_feather(df, 'Twitter_exploration', project)


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

  df = fc.load_feather('Twitter_raw', project)

  clean_text = clean.Clean()
  t = clean_text.fit_transform(df.text)

  empty_clean = t == ''
  t.loc[empty_clean] = '[no_text]'

  clean_data = pd.DataFrame(t)
  clean_data['sentiment'] = df.airline_sentiment

  fc.save_feather(clean_data, 'Twitter_clean', project)

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

  clean_data = fc.load_feather('Twitter_clean', project)

  word_count = count_vect.fit_transform(clean_data.text)
  vectors = tfidf_transformer.fit_transform(word_count)

  fc.save_npz(vectors, 'Twitter_vectors', project)
  fc.save_pickel(count_vect.vocabulary_, 'Twitter_countVec', project)
  fc.save_pickel(tfidf_transformer.idf_, 'Twitter_tfidf_trans', project)


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

  clean_data = fc.load_feather('Twitter_clean', project)
  vectors = fc.load_npz('Twitter_vectors', project)
  count_vect.vocabulary_ = fc.load_pickel('Twitter_countVec', project)
  tfidf_transformer.idf_ = fc.load_pickel('Twitter_tfidf_trans', project)

  if model == 'MNB':
    from sklearn.naive_bayes import MultinomialNB
    clf = MultinomialNB().fit(vectors, clean_data.sentiment)
    fc.save_pickel(clf, 'TwitteR_multinomial_nb', project)

  if model == 'LR':
    from sklearn.linear_model import LogisticRegression
    logreg = LogisticRegression().fit(vectors, clean_data.sentiment)
    fc.save_pickel(logreg, 'Twitter_logistic_regression', project)


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

  count_vect.vocabulary_ = fc.load_pickel('Twitter_countVec', project)
  tfidf_transformer.idf_ = fc.load_pickel('Twitter_tfidf_trans', project)

  if model == 'MNB':
    clf = fc.load_pickel('Twitter_multinomial_nb', project)
    snipped = count_vect.transform([text])
    to_predict = tfidf_transformer.transform(snipped)
    predicted = clf.predict(to_predict)

  if model == 'LR':
    logreg = fc.load_pickel('Twitter_logistic_regression', project)
    snipped = count_vect.transform([text])
    to_predict = tfidf_transformer.transform(snipped)
    predicted = logreg.predict(to_predict)

  if debugging:
    print(predicted)
  return json.dumps(predicted.tolist())
