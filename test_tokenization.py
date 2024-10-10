import nltk

# Add the al nltk_data path
nltk.data.path.append('/Users/mac/Desktop/Assignmet/punkt')  # Replace 'yourusername' with your actual username

# Test tokenization
text = "This is a test sentence."
tokens = nltk.word_tokenize(text)

# Print the tokens
print(tokens)
