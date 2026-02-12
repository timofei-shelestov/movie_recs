import re
import math
import numpy as np


class TfidfVectorizer:
  def __init__(self):
    self.n_docs = 1
    self.vocab = {}
    self.docs_frequencies = {}

  def fit(self, movies):
    docs = [movie["overview"] for movie in movies]
    self.n_docs = len(list(docs))
    termInCurrentDoc = False
    c = 0
    for doc in docs:
      for term in re.findall(r"\b\w+\b", doc):
        term = term.lower().strip()
        if term not in self.vocab:
          self.vocab[term] = c
          c = c + 1
        if term not in self.docs_frequencies:
          self.docs_frequencies[term] = 1
          termInCurrentDoc = True
        else:
          if not termInCurrentDoc:
            self.docs_frequencies[term] = self.docs_frequencies[term] + 1

      termInCurrentDoc = False

  def transform(self, movies):
    docs = [movie["overview"] for movie in movies]
    tfidf_mtx = np.zeros((len(movies), len(self.vocab)), dtype=np.float32)

    for doc_idx, doc in enumerate(docs):
      tf = self._calc_tf(doc)
      for term in re.findall(r"\b\w+\b", doc):
        term = term.lower().strip()

        if term in self.vocab:
          idf = self._calc_idf(term)
          tfidf = tf[term] * idf
          tfidf_mtx[doc_idx, self.vocab[term]] = tfidf
          
    return tfidf_mtx

  def vecrorize_sigle_movie(self, movie):
    doc = movie["overview"]
    tf = self._calc_tf(doc)
    tfidf_vec = np.zeros((1, len(tf)), dtype=np.float32)

    for term in re.findall(r"\b\w+\b", doc):
      term = term.lower().strip()

      if term in self.vocab:
        idf = self._calc_idf(term)
        tfidf = tf[term] *  idf
        tfidf_vec[0, self.vocab[term]] = tfidf
      
    return tfidf_vec




  def _calc_tf(self, doc):
    tf = {}
    for term in re.findall(r"\b\w+\b", doc):
      term = term.lower().strip()
      if term not in tf:
        tf[term] = 1
      else:
        tf[term] = tf[term] + 1

    return tf

  def _calc_idf(self, term):
    return math.log10(self.n_docs / self.docs_frequencies[term])
