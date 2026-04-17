# Simple Text Analyzer
# Works in Python 3.13 (no external libraries required)

from collections import Counter
import string

def analyze_text(text):
    # Remove punctuation
    clean_text = text.translate(str.maketrans('', '', string.punctuation))
    
    # Convert to lowercase
    clean_text = clean_text.lower()
    
    # Split words
    words = clean_text.split()
    
    # Word count
    word_count = len(words)
    
    # Character count (excluding spaces)
    char_count = len(text.replace(" ", ""))
    
    # Sentence count
    sentence_count = text.count('.') + text.count('!') + text.count('?')
    
    # Most common words
    word_freq = Counter(words)
    common_words = word_freq.most_common(5)
    
    # Average word length
    if word_count > 0:
        avg_word_length = sum(len(word) for word in words) / word_count
    else:
        avg_word_length = 0

    # Display results
    print("\n--- TEXT ANALYSIS REPORT ---")
    print(f"Total Words: {word_count}")
    print(f"Total Characters (no spaces): {char_count}")
    print(f"Total Sentences: {sentence_count}")
    print(f"Average Word Length: {avg_word_length:.2f}")
    
    print("\nTop 5 Most Common Words:")
    for word, freq in common_words:
        print(f"{word} : {freq}")


# Main Program
if __name__ == "__main__":
    print("Enter your text (press Enter twice to finish):")
    
    lines = []
    while True:
        line = input()
        if line == "":
            break
        lines.append(line)
    
    text = "\n".join(lines)
    
    analyze_text(text)