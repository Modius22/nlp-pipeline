import string
import re
from sklearn.base import BaseEstimator, TransformerMixin
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

class Clean(BaseEstimator, TransformerMixin):
    def remove_mentions(self,text):
        """ remove mentions from text

        Parameters
        ----------
        text : str
            text element
        """
        return re.sub(r'@\w+', '', text)

    def remove_urls(self, text):
        """ remove urls from text

        Parameters
        ----------
        text : str
            text element
        """
        return re.sub(r'http.?://[^\s]+[\s]?', '', text)

    def emoji_oneword(self, text):
        """ By compressing the underscore, the emoji is kept as one word

        Parameters
        ----------
        text : str
            text element
        """
        return text.replace('_', '')

    def remove_punctuation(self, text):
        """ remove punctuations from text

        Parameters
        ----------
        text : str
            text element
        """
        punct = string.punctuation
        trantab = str.maketrans(punct, len(punct) * ' ')
        return text.translate(trantab)

    def remove_digits(self, text):
        """ remove digits from text

        Parameters
        ----------
        text : str
            text element
        """
        return re.sub('\d+', '', text)

    def to_lower(self, text):
        """ Converts all words to lower case

        Parameters
        ----------
        text : str
            text element
        """
        return text.lower()

    def remove_stopwords(self, text):
        """ Removes stopwords from the text

        Parameters
        ----------
        text : str
            text element
        """
        stopwords_list = stopwords.words('english')
        whitelist = ["n't", "not", "no"]
        words = text.split()
        clean_words = [word for word in words if (word not in stopwords_list or word in whitelist) and len(word) > 1]
        return " ".join(clean_words)

    def stemming(self, text):
        """ stemming of the words

        Parameters
        ----------
        text : str
            text element
        """
        porter = PorterStemmer()
        words = text.split()
        stemmed_words = [porter.stem(word) for word in words]
        return " ".join(stemmed_words)

    def fit(self, X, y=None, **fit_params):
        return self

    def transform(self, X, **transform_params):
        clean_X = X.apply(self.remove_mentions).apply(self.remove_urls).apply(self.emoji_oneword).apply(
            self.remove_punctuation).apply(self.remove_digits).apply(self.to_lower).apply(self.remove_stopwords).apply(
            self.stemming)
        return clean_X