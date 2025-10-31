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

    '''Here is the result:
    Topic 1: 0.016*"wedding" + 0.012*"party" + 0.011*"christmas" + 0.011*"birthday" + 0.010*"plan"
    Topic 2: 0.033*"car" + 0.012*"phone" + 0.011*"drive" + 0.008*"minute" + 0.007*"call"
    Topic 3: 0.012*"room" + 0.009*"help" + 0.007*"clean" + 0.007*"need" + 0.006*"sleep"
    Topic 4: 0.008*"talk" + 0.006*"tell" + 0.006*"talking" + 0.006*"made" + 0.005*"call"
    Topic 5: 0.011*"school" + 0.011*"job" + 0.008*"class" + 0.006*"working" + 0.006*"teacher"
    Topic 6: 0.027*"food" + 0.018*"eat" + 0.013*"dinner" + 0.009*"eating" + 0.008*"drink"
    Topic 7: 0.033*"dog" + 0.012*"room" + 0.011*"cat" + 0.008*"door" + 0.006*"play"
    Topic 8: 0.031*"money" + 0.025*"pay" + 0.011*"job" + 0.009*"rent" + 0.008*"move"
    Topic 9: 0.026*"gift" + 0.016*"christmas" + 0.009*"something" + 0.007*"wanted" + 0.007*"present"
    Topic 10: 0.021*"kid" + 0.016*"husband" + 0.015*"mother" + 0.013*"daughter" + 0.013*"wife"
    '''

    topic_counts = Counter()

    for bow in doc_term_matrix:
        topic_probabilities = lda_model.get_document_topics(bow) # Gets a list of tuples with first index of tuple being the index of topic and second being the probability
        if topic_probabilities:
            dominant_topic = max(topic_probabilities, key=lambda x: x[1])[0]
            topic_counts[dominant_topic] += 1
    
    print(topic_counts)

    '''Here is the result:
    Counter({3: 15432, 9: 9107, 2: 8168, 0: 8014, 7: 6499, 4: 5127, 6: 4575, 1: 3985, 8: 3257, 5: 3127})
    The indices are shifted by one thus we can say that ->  1) Topic 4: Communication
                                                            2) Topic 10: Family
                                                            3) Topic 3: Personal space
                                                            4) Topic 1: Social events
                                                            5) Topic 8: Finances
                                                            6) Topic 5: Education
                                                            7) Topic 7: Pets
                                                            8) Topic 2: Transport
                                                            9) Topic 9: Gifts
                                                            10) Topic 6: Food
    '''