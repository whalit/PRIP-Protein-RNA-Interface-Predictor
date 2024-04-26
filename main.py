import tempfile
from gensim.models import Word2Vec
from gensim.test.utils import datapath
from gensim import utils
import pandas as pd

def load_model(path):
    return gensim.models.Word2Vec.load(path)


class RB198Corpus:
    def __init__(self, data_path):
        df = pd.read_csv(data_path)
        self.protein_sequences = df["Sequence"].tolist()

    def __iter__(self):
        for sequence in self.protein_sequences:
            nucleotides = [char for char in sequence]
            yield nucleotides # Split each protein sequence into individual amino acids



corpus = RB198Corpus("Datasets/RB198.csv")
model = Word2Vec(sentences=corpus, vector_size=25, window=5, min_count=1, workers=1 , epochs=200, sg=0, negative=5)
model.save("protein_word2vec.model")

# Get the vocabulary (list of unique tokens)
vocabulary = model.wv.index_to_key

# Print the vocabulary
print("Vocabulary (amino acid residues):", vocabulary)

residue_vector = model.wv["M"]
print("Vector representation of amino acid 'M':", residue_vector)

# Find most similar amino acids to a given amino acid
similar_residues = model.wv.most_similar("M")
print("Most similar amino acids to 'M':", similar_residues)

