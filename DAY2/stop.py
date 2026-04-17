text = "this is a simple nlp example"

custom_stopwords = {"is", "a", "this"}

words = text.split()

filtered = [w for w in words if w not in custom_stopwords]

print(filtered)
