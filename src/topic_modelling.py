'''Topic modelling uses Latent Semantic Analysis (LSA) and Latent Dirichlet Allocation (LDA). 
Before we can use the preprocessed data as input to a LDA or LSA model, it must be converted to a term-document matrix using the corpora module from gensim library 
A term-document matrix is merely a mathematical representation of a set of documents and the terms contained within them. (https://www.datacamp.com/tutorial/what-is-topic-modeling)
''' 

from preprocessing import load_json
from gensim import corpora
from gensim.models.ldamulticore import LdaMulticore
from nltk.corpus import stopwords
from collections import Counter
import string
from nltk.stem.wordnet import WordNetLemmatizer
import re

if __name__ == "__main__":
    file_dir = "./data/output.json"
    corpus = load_json(file_dir)
    corpus = [doc.split(' [======>] ')[0] for doc in corpus if isinstance(doc, str)] # Only get the submissions
    corpus = [doc for doc in corpus if len(doc.split()) > 20] # To filter out short documents (submissions)

    stop = set(stopwords.words('english'))
    exclude = set(string.punctuation)
    lemma = WordNetLemmatizer()


    def clean(doc):
        doc = doc.lower()
        doc = re.sub(r"['|`]", "", doc)
        doc = re.sub(r"\bamp\b", " ", doc)
        doc = re.sub(r'[^a-zA-Z]', ' ', doc)
        doc = re.sub(r"\b(aita|nta|yta|edit|update)\b", "", doc)
        stop_free = " ".join([i for i in doc.lower().split() if i not in stop])
        punc_free = "".join(ch for ch in stop_free if ch not in exclude)
        normalized = " ".join(lemma.lemmatize(word) for word in punc_free.split())
        return normalized


    chunk_size = 5000
    clean_corpus_temp = []

    for i, doc in enumerate(corpus, 1):
        clean_doc = clean(doc).split()
        clean_corpus_temp.append(clean_doc)

    most_freq = Counter(word for doc in clean_corpus_temp for word in doc)
    banned_words = set([word for word, _ in most_freq.most_common(50)])

    def ban_most_freq():
        return [[word for word in doc if word not in banned_words]
            for doc in clean_corpus_temp]
    clean_corpus = ban_most_freq()

    dictionary = corpora.Dictionary(clean_corpus)
    dictionary.filter_extremes(no_below=3, no_above=0.5)
    doc_term_matrix = [dictionary.doc2bow(doc) for doc in clean_corpus]

    # Build LDA model
    lda_model = lda_model = LdaMulticore(
        corpus=doc_term_matrix,
        id2word=dictionary,
        num_topics=10,
        passes=8,
        workers=4,          # adjust to number of CPU cores
        chunksize=2000,
        random_state=42,
        per_word_topics=False
    )

    topics = lda_model.print_topics(num_words=5)
    for i, topic in topics:
        print(f"Topic {i + 1}: {topic}")
