import unittest
from api import app

class DataLoad(unittest.TestCase):

  def setUp(self):
    self.app = app.test_client()

  def test_sucessfull_data_load(self):

    response = self.app.post('/nlp/project_a/load?text=text&sentiment=airline_sentiment' , headers={"enctype" : "multipart/form-data", "Content-Type" : "multipart/form-data"}, data='../../data/Tweets.csv')
    self.assertEqual(200, response.status_code)

