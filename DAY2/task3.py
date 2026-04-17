def classify_sentence(sentence):
    sentence = sentence.strip()
    
    if not sentence:
        return "Empty sentence"
    
    # Check last character
    if sentence.endswith('?'):
        return "Question"
    elif sentence.endswith('!'):
        return "Exclamation"
    else:
        return "Statement"


# Test the function
if __name__ == "__main__":
    print("Enter sentences (type 'exit' to stop):")
    
    while True:
        text = input(">> ")
        
        if text.lower() == "exit":
            break
        
        result = classify_sentence(text)
        print(f"Type: {result}")