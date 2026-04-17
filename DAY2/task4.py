import string

def text_processing(text):
    cleaned = text.translate(str.maketrans('', '', string.punctuation))
    words = cleaned.split()
    
    print("\n--- Result ---")
    print("Lower:", cleaned.lower())
    print("Words:", words)
    print("Joined:", " ".join(words))
    print("Replaced:", cleaned.replace("Python", "AI"))
    print("Contains 'Python':", "Python" in text)


# Main
while True:
    text = input("\nEnter text (type 'exit' to stop): ")
    
    if text.lower() == "exit":
        break
    
    text_processing(text)