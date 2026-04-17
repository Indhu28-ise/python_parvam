#Text Cleaning Pipeline

import re

def clean_text(text):
    # Step 1: Lowercase
    text = text.lower()

    # Step 2: Remove URLs
    text = re.sub(r'http\S+|www\S+', '', text)

    # Step 3: Remove emails
    text = re.sub(r'\S+@\S+', '', text)

    # Step 4: Remove numbers & special characters
    text = re.sub(r'[^a-z\s]', '', text)

    # Step 5: Remove extra whitespace
    text = re.sub(r'\s+', ' ', text).strip()

    # Step 6: Remove stopwords
    stop_words = {"is", "in", "for", "the", "and", "to", "of"}
    words = [w for w in text.split() if w not in stop_words]

    return " ".join(words)


samples = [
    "Check out https://python.org for Python docs!!!",
    "AI is AMAZING in 2024... seriously!!!",
    "Email: test@mail.com | Phone: 9876543210"
]

for s in samples:
    print(f"Original : {s}")
    print(f"Cleaned  : {clean_text(s)}\n")
