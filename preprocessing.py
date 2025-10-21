import json
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
import pandas as pd


def load_reddit_data(data_directory, output_path):
    with open(data_directory, 'r', encoding='utf-8') as file, \
         open(output_path, 'w', encoding='utf-8') as outfile: # By doing that we aim to avoid loading the whole data at the same time
        for i, line in enumerate(file, 1):
            try:
                if i >= 10000:
                    break
                data = json.loads(line)
                body = data.get('body', '').strip()
                outfile.write(body + "\n")
            except json.JSONDecodeError:
                continue  # This is done to avoid missing comments or bad lines

data_dir = './data/amitheasshole_comments.ndjson'
reddit_data = load_reddit_data(data_dir, './data/amitheasshole_comments.txt') # Can be commented out after writing the data to a file

def tokenize_text(text):
    return word_tokenize(text)

def remove_stopwords(text):
    stop_words = set(stopwords.words('english'))
    word_tokens = tokenize_text(text)
    return [word for word in word_tokens if not word in stop_words] # This ensures the return of the words that are not in the stopwords list

def lemmetize_text(text):
    lemmatizer = WordNetLemmatizer()
    words = tokenize_text(text)
    lemmatized_words = [lemmatizer.lemmatize(word) for word in words]
    return ' '.join(lemmatized_words)


reddit_data_txt = "./data/amitheasshole_comments.txt"

def write_reddit_data(text, output_directory):
    with open(text, 'r', encoding='utf-8') as file, \
         open(output_directory, 'a', encoding='utf-8') as outfile:
        for line in file:
            data = remove_stopwords(lemmetize_text(line))
            cleaned_line = " ".join(data)
            outfile.write(cleaned_line + "\n")

#write_reddit_data(reddit_data_txt, './data/amitheasshole_comments_preprocessed.txt')
