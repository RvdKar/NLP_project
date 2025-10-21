'''Topic modelling uses Latent Semantic Analysis (LSA) and Latent Dirichlet Allocation (LDA). 
Before we can use the preprocessed data as input to a LDA or LSA model, it must be converted to a term-document matrix using the corpora module from gensim library 
A term-document matrix is merely a mathematical representation of a set of documents and the terms contained within them. (https://www.datacamp.com/tutorial/what-is-topic-modeling)
''' 

from gensim import corpora
from gensim.models import LsiModel, LdaModel

