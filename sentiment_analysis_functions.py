from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer
def rule_based_sentiment_analysis(text):
	utf8_friendly_text = text.decode('utf8','ignore')
	blob = TextBlob(utf8_friendly_text)
	return (blob.sentiment[0], blob.sentiment[1])

def machine_learning_sentiment_analysis(text):
	utf8_friendly_text = text.decode('utf8','ignore')
	blob = TextBlob(utf8_friendly_text,analyzer=NaiveBayesAnalyzer())
	return blob.sentiment.classification