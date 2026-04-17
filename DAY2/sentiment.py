# sentiment analysis example
import sys
from textblob import TextBlob
sys.stdout.reconfigure(encoding="utf-8")
text = "I love this product! It's amazing and works great."
blob = TextBlob(text)
sentiment = blob.sentiment
print(f"Sentiment: {sentiment}")

