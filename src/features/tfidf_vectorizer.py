import re
import math


class TfidfVectorizer:
  def __init__(self):
    self.n_docs = 0
    self.vocab = {}
    self.docs_frequencies = {}

  def fit(self, movies):
    docs = [movie["overview"] for movie in movies]
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
    self.n_docs = len(list(docs))
    tfidf_vec = []

    for doc in docs:
      tf = self._calc_tf(doc)
      curr_vec = [0] * len(self.vocab)
      for term in re.findall(r"\b\w+\b", doc):
        term = term.lower().strip()

        idf = self._calc_idf(term)
        tfidf = round(tf[term] * idf, 1)
        curr_vec[self.vocab[term]] = tfidf

      tfidf_vec.append(curr_vec)

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
    return math.log(self.n_docs / self.docs_frequencies[term])
