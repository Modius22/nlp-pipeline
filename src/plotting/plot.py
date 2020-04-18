import pandas as pd

import matplotlib.pyplot as plt

df = pd.read_csv('data/Tweets.csv')

sentiment_count=df['airline_sentiment'].value_counts()
Index = [1,2,3]
plt.bar(Index,sentiment_count)
plt.xticks(Index,['negative','neutral','positive'],rotation=45)
plt.ylabel('Sentiment Count')
plt.xlabel('Sentiment')
plt.title('Count of Sentiment')


##


df2 = pd.read_csv('data/Sentiment.csv')

sentiment_count=df2['airline_sentiment'].value_counts()
Index = [1,2,3]
plt.bar(Index,sentiment_count)
plt.xticks(Index,['negative','neutral','positive'],rotation=45)
plt.ylabel('Sentiment Count')
plt.xlabel('Sentiment')
plt.title('Count of Sentiment')

