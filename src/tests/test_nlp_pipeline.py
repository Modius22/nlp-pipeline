import unittest
import os
import pandas as pd

from api import app

class NlpPipeline(unittest.TestCase):

  def setUp(self):
    self.app = app.test_client()

  def test_complete_pipeline(self):
#    # create directory
#    assert os.path.exists('../working') == 1
#    response = self.app.get('/nlp/create_project?project_name=project_a')
#    self.assertEqual(200, response.status_code)
#    assert os.path.exists('../working/project_a') == 1
#    print(os.getcwd())

#    res = self.client.post('/', data=dict(
#      upload_var=(StringIO("hi everyone"), 'test.txt'),
#    ))
#    assert res.status_code == 200
#    assert 'file saved' in res.data


    # Load Data
    assert os.path.exists('../working/project_a') == 1


    df = pd.read_csv('../data/Tweets.csv')
    csv = df.to_csv(index=False)
    response = self.app.post('/nlp/project_a/load?text=text&sentiment=airline_sentiment', headers={'enctype': 'multipart/form-data', 'Content-Type': 'multipart/form-data'}, data=csv)
    self.assertEqual(200, response.status_code)
    assert os.path.isfile('../working/project_a/project_a_raw.feather') == 1


#    # Load Data
#    assert os.path.exists('../working/project_a') == 1
#    response = self.app.post('/nlp/project_a/load?text=text&sentiment=airline_sentiment', headers={'enctype': 'multipart/form-data', 'Content-Type': 'multipart/form-data'}, data='../data/Tweets.csv')
#    self.assertEqual(200, response.status_code)
#    assert os.path.isfile('../working/project_a/project_a_raw.feather') == 1





    # Explore data
    assert os.path.exists('../working/project_a') == 1
    response = self.app.get('/nlp/project_a/exploartion')
    self.assertEqual(200, response.status_code)
    assert os.path.isfile('../working/project_a/project_a_exploration.feather') == 1

    # clean data
    assert os.path.exists('../working/project_a') == 1
    response = self.app.get('/nlp/project_a/clean')
    self.assertEqual(200, response.status_code)
    assert os.path.isfile('../working/project_a/project_a_clean.feather') == 1

    # vectorize data
    assert os.path.exists('../working/project_a') == 1
    response = self.app.get('/nlp/project_a/vectorize')
    self.assertEqual(200, response.status_code)
    assert os.path.isfile('../working/project_a/project_a_countVec.p') == 1
    assert os.path.isfile('../working/project_a/project_a_tfidf_trans.p') == 1

    # modeling data LR
    assert os.path.exists('../working/project_a') == 1
    response = self.app.get('/nlp/project_a/model?algorithm=LR')
    self.assertEqual(200, response.status_code)
    assert os.path.isfile('../working/project_a/project_a_logistic_regression.p') == 1

    # modeling data MNB
    assert os.path.exists('../working/project_a') == 1
    response = self.app.get('/nlp/project_a/model?algorithm=MNB')
    self.assertEqual(200, response.status_code)
    assert os.path.isfile('../working/project_a/project_a_multinomial_nb.p') == 1

    # predict data LR
    assert os.path.exists('../working/project_a') == 1
    response = self.app.post('/nlp/project_a/predict?algorithm=LR&text=told%20work%20joke%20fail')
    self.assertEqual(200, response.status_code)

    # predict data MNB
    assert os.path.exists('../working/project_a') == 1
    response = self.app.post('/nlp/project_a/predict?algorithm=MNB&text=told%20work%20joke%20fail')
    self.assertEqual(200, response.status_code)

    # delete directory
    assert os.path.exists('../working') == 1
    response = self.app.get('/nlp/delete_project?project_name=project_a')
    self.assertEqual(200, response.status_code)
    assert os.path.exists('../working/project_a') == 0
