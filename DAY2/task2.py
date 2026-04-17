import string

def tokenize_sentence(sentence):
    # Remove punctuation
    cleaned = sentence.translate(str.maketrans('', '', string.punctuation))
    
    # Convert to lowercase (optional but useful)
    cleaned = cleaned.lower()
    
    # Split into words (tokens)
    tokens = cleaned.split()
    
    return tokens


# Example usage
text = "Hello! This is a simple sentence, for testing."
tokens = tokenize_sentence(text)

print(tokens)