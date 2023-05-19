import pandas as pd
from googletrans import Translator
import re
import nltk
from nltk.tokenize import word_tokenize
nltk.download('stopwords')
from nltk.corpus import stopwords
import pyarabic.araby as araby
import unicodedata as ud




def remove_non_arabic(text):
    # Match any character that is not in the Arabic Unicode block or is not a space character
    pattern = re.compile('[^\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF\uFB50-\uFDCF\uFDF0-\uFDFF\uFE70-\uFEFF ]+')
    return pattern.sub('', text)

def count_english_words(data):
    # Tokenize the text into words
    tokens = data['Tweet'].astype(str).apply(word_tokenize)
    # Regular expression pattern to match any non-Arabic characters
    english_pattern = r'\b[A-Za-z]+\b'
    # Filter out non-Arabic words using the regular expression
    english_words = tokens.apply(lambda words: [word for word in words if re.match(english_pattern, word)])

    # Count the occurrences of each Arabic word
    english_words = pd.Series([word for words in english_words for word in words]).value_counts()

    # Print the top 10 most frequent Arabic words
    print(english_words.head(10))

def count_digits(data):
    # Regular expression pattern to match any digits
    digits_pattern = r'\d+'
    # Apply the regular expression pattern to each row of the "tweet" column and count the digits
    digit_counts = data['Tweet'].apply(lambda x: len(re.findall(digits_pattern, x))).sum()

    # Print the total count of digits in all tweets
    print('Total digits count:', digit_counts)

def remove_stop_words(tweet):
    stop_words = set(stopwords.words('arabic'))
    tokens = word_tokenize(tweet)
    filtered_tokens = [token for token in tokens if token not in stop_words]
    return ' '.join(filtered_tokens)

def remove_diacritics(tweet):
    return araby.strip_tashkeel(tweet)

def remove_emojis(text):
    # Match all Unicode emojis and remove them
    pattern = re.compile("[\U0001F600-\U0001F64F\u2600-\u26FF\u2700-\u27BF]+")
    return pattern.sub('', text)

# Define a function to normalize Arabic text
def normalize_arabic(tweet):
    # Normalize hamza and alef characters
    tweet = araby.normalize_hamza(tweet)
    tweet = araby.normalize_alef(tweet)
    
    return tweet

def remove_punctuation(text):
    res = ''.join(c for c in text if not ud.category(c).startswith('P'))
    res2 = ''.join(c for c in res if not c == "،")
    return res


# Read the dataset
def preprocess(datapath):
    data = pd.read_excel(datapath)


    data_raw = data.copy()

    digits_pattern = r'\d+'

    english_pattern = r'\b[A-Za-z]+\b'

    stop_words = set(stopwords.words('arabic'))

    data['Tweet'] = data['Tweet'].apply(lambda x: re.sub(english_pattern, '', str(x)))


    # Apply the regular expression pattern to each row of the "tweet" column
    data['Tweet'] = data['Tweet'].astype(str).apply(lambda x: re.sub(digits_pattern, '', str(x)))

    # Apply the function to each row of the "tweet" column
    data['Tweet'] = data['Tweet'].astype(str).apply(remove_stop_words)


    # Apply the function to each row of the "tweet" column
    data['Tweet'] = data['Tweet'].astype(str).apply(remove_diacritics)


    # Apply the normalization function to each row of the "tweet" column
    data['Tweet'] = data['Tweet'].astype(str).apply(normalize_arabic)




    # Apply the normalization function to each row of the "tweet" column
    data['Tweet'] = data['Tweet'].astype(str).apply(remove_emojis)



    # Remove non-Arabic characters from the "tweet" column
    data['Tweet'] = data['Tweet'].astype(str).apply(remove_non_arabic)

    # Remove punctuation
    data['Tweet'] = data['Tweet'].astype(str).apply(remove_punctuation)



    # save the DataFrame to an xlsx file
    return data




