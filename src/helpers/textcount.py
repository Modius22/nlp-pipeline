import re
import emoji
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin


class TextCounts(BaseEstimator, TransformerMixin):

    def count_regex(self, pattern, text):
        """ creates a count from a given regex and text

         Parameters
         ----------
         pattern : str
            regex pattern
         text : str
            text to which the pattern is applied
         """
        return len(re.findall(pattern, text))

    def fit(self, X, y=None, **fit_params):
        return self

    def transform(self, X, **transform_params):
        words_count = X.apply(lambda x: self.count_regex(r'\w+', x))
        mentions_count = X.apply(lambda x: self.count_regex(r'@\w+', x))
        hashtags_count = X.apply(lambda x: self.count_regex(r'#\w+', x))
        capital_words_count = X.apply(lambda x: self.count_regex(r'\b[A-Z]{2,}\b', x))
        excl_quest_marks_count = X.apply(lambda x: self.count_regex(r'!|\?', x))
        urls_count = X.apply(lambda x: self.count_regex(r'http.?://[^\s]+[\s]?', x))

        emojis_count = X.apply(lambda x: emoji.demojize(x)).apply(lambda x: self.count_regex(r':[a-z_&]+:', x))

        df = pd.DataFrame({'count of words': words_count
                              , 'count of mentions': mentions_count
                              , 'count of hashtags': hashtags_count
                              , 'count of capital words': capital_words_count
                              , 'count of excl quest marks': excl_quest_marks_count
                              , 'count of urls': urls_count
                              , 'count of emojis': emojis_count
                           })

        return df