import numpy as np

## I'll leave it here tho I use scikit-learn for that stuff
def cos_similarity(vec1, vec2):
  return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))
