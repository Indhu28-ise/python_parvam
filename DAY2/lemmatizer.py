
# lemmatizer example
import sys
import nltk
from nltk.data import find
from nltk.stem import WordNetLemmatizer

sys.stdout.reconfigure(encoding="utf-8")

def ensure_nltk_data():
    try:
        find("corpora/wordnet")
    except LookupError:
        try:
            find("corpora/wordnet.zip")
        except LookupError:
            nltk.download("wordnet", quiet=True)

    try:
        find("corpora/omw-1.4")
    except LookupError:
        try:
            find("corpora/omw-1.4.zip")
        except LookupError:
            nltk.download("omw-1.4", quiet=True)

words = ["playing", "running", "studies", "better"]

ensure_nltk_data()
lemmatizer = WordNetLemmatizer()

for word in words:
    print(word, "->", lemmatizer.lemmatize(word, pos="v"))

raise SystemExit

for word in words:
    print(word, "→", lemmatizer.lemmatize(word))
