import re
import math


class TfidfVectorizer:
  def __init__(self, docs):
    self.n_docs = 0
    self.vocab = {}
    self.docs_frequencies = {}

  def fit(self, docs):
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

  def transfrom(self, docs):
    tfidf_vec = []

    for doc in docs:
      curr_vec = []
      tf = self._calc_tf(doc)
      for term in re.findall(r"\b\w+\b", doc):
        term = term.lower()

        idf = self._calc_idf(len(list(docs)), term, self.docs_frequencies)
        tfidf = round(tf[term] * idf, 1)
        curr_vec.insert(self.vocab[term], tfidf)

      tfidf_vec.append(curr_vec)

    return tfidf_vec

  def _calc_tf(self, doc):
    tf = {}
    for term in doc.split():
      if term not in self.vocab:
        tf[term] = 1
      else:
        tf[term] = tf[term] + 1

    return tf

  def _calc_idf(self, n_docs, term):
    return math.log(n_docs / self.docs_frequencies[term])
