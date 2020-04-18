from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.base import BaseEstimator, TransformerMixin


class vectorizer(BaseEstimator, TransformerMixin):

  def termcount(self, data):
    """ create termcount

     Parameters
     ----------
     data : data frame
        pandas data frame with text
     """
    count_vect = CountVectorizer()
    X_train_counts = count_vect.fit_transform(data)
    return X_train_counts

  def tf(self, data):
    """ create tf-idf

     Parameters
     ----------
     data : data frame
        pandas data frame with text
     """
    tf_transformer = TfidfTransformer(use_idf=False).fit(self.termcount(data))
    X_train_tf = tf_transformer.transform(self.termcount(data))
    return X_train_tf



  def fit(self, X, y=None, **fit_params):
    data = TfidfTransformer(use_idf=False).fit_transform(self.termcount(X))
    return data


  def transform(self, X, **transform_params):
    data = TfidfTransformer().transform(self.termcount(X))
    return data
