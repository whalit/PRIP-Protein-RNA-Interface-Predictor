from gensim.models import Word2Vec
from gensim.test.utils import datapath
from gensim import utils
import pandas as pd

def load_model(path):
    return Word2Vec.load(path)

def split_protein_sequence(protein_sequence, segment_length):
    
    if segment_length % 2 == 0 :
        raise ValueError("Segment length must be an odd number and greater than or equal to 2*n + 1")

    segments = []
    sequence_length = len(protein_sequence)

    n = (segment_length - 1)// 2

    # Iterate over each residue in the protein sequence
    for i in range(sequence_length):
        # Determine the start and end indices of the segment
        start_index = max(0, i - n)
        end_index = min(sequence_length, i + n + 1)

        # Pad the segment with "X" characters at the start or end if needed
        if start_index == 0:
            padded_segment = "X" * (n - i) + protein_sequence[:end_index]
        elif end_index == sequence_length:
            padded_segment = protein_sequence[start_index:] + "X" * (n - (sequence_length - 1 - i))
        else:
            segment = protein_sequence[start_index:end_index]
            padded_segment = "X" * (n - (i - start_index)) + segment

        # Add the segment to the list of segments
        segments.append(padded_segment)

    return segments

def feature_extract(segments , W2V_model):
    semantic_vect_concat = []
    for segment in segments :
        seg_vect = []
        for residue in segment : 
            if residue != 'X' : 
                seg_vect.extend(W2V_model.wv[residue])
            else: 
                seg_vect.extend([0 for i in range(25)])
        semantic_vect_concat.append(seg_vect)

    return semantic_vect_concat
                 


model = load_model("model_W2V.model")

df_train = pd.read_csv("Datasets/RB198.csv")
df_test = pd.read_csv("Datasets/RB111.csv")

protein_seqs_train = df_train['Sequence'].to_list()
label_interfaces_train = df_train['Interface'].to_list()


protein_seqs_test= df_test['Sequence'].to_list()
label_interfaces_test = df_test['Interface'].to_list()

pairs = list(zip(protein_seqs_train , label_interfaces_train))


# Sequence splitting + assigning the interface labels for each split
X , y = [] , []
for elem in pairs : 
    prot_sequence = elem[0]
    label_interf = elem[1]
    segments = split_protein_sequence(prot_sequence ,segment_length = 39, n = 10)

    # X represents the segments (sequences split) and y represents the respective labels
    X.extend(segments)
    y.extend(label_interf)
    


# Feature extraction
semantic_vects = feature_extract(X , model)

print(semantic_vects)