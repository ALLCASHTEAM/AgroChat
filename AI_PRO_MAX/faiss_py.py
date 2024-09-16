import os
from sentence_transformers import SentenceTransformer
import numpy as np
from pathlib import Path
import hnswlib

# Load the sentence transformer model
model = SentenceTransformer('intfloat/multilingual-e5-large')


def read_and_preprocess_data(folder_path):
    # Read all txt files in the folder
    folder_path = Path(folder_path)
    return [(parts[0], parts[1]) for file in folder_path.glob("*.txt") for parts in
            [line.strip().split(" | ") for line in file.open('r', encoding='utf-8')] if len(parts) == 2]


def vectorize_questions(questions):
    # Transform questions into vectors
    return model.encode(questions)


def create_hnsw_index(vectors, ef=200, M=16):
    # Create HNSW index for the vectors
    num_elements, dim = vectors.shape
    index = hnswlib.Index(space='cosine', dim=dim)  # Use L2 distance
    index.init_index(max_elements=num_elements, ef_construction=ef, M=M)

    # Add vectors to the index
    index.add_items(vectors)

    # Set ef (parameter controlling recall vs speed tradeoff)
    index.set_ef(ef)

    return index


def search(query, index, questions_answers, top_k=20):
    query_vector = vectorize_questions([query])[0].astype('float32')
    labels, distances = index.knn_query(np.array([query_vector]), k=top_k)
    return [[questions_answers[i][0], questions_answers[i][1]] for i in labels[0]]


def list_return(user_query) -> list:
    # Buffer
    return search(user_query, index, questions_answers)


# Initialization of everything needed for the process
folder_path = Path(__file__).resolve().parent.parent / "rofls"
questions_answers = read_and_preprocess_data(folder_path)
questions = [qa[1] for qa in questions_answers]
vectors = vectorize_questions(questions)

# Create HNSW index with vectorized data
index = create_hnsw_index(np.array(vectors).astype('float32'))
