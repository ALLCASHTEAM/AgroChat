import os
import pickle
from sentence_transformers import SentenceTransformer
import numpy as np
from pathlib import Path
import hnswlib

model = SentenceTransformer('intfloat/multilingual-e5-large')


def read_and_preprocess_data(folder_path):
    folder_path = Path(folder_path)
    data = []
    for file in folder_path.glob("*.txt"):
        with file.open('r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split(" | ")
                if len(parts) == 2:
                    data.append((parts[0], parts[1]))
    return data


def vectorize_questions(questions):
    return model.encode(questions).astype('float32')


def create_hnsw_index(vectors, ef=200, M=16):
    num_elements, dim = vectors.shape
    index = hnswlib.Index(space='cosine', dim=dim)
    index.init_index(max_elements=num_elements, ef_construction=ef, M=M)

    index.add_items(vectors, ids=np.arange(num_elements))

    index.set_ef(ef)

    return index


def search(query, index, questions_answers, top_k=20):
    query_vector = vectorize_questions([query])[0]
    labels, distances = index.knn_query(np.array([query_vector]), k=top_k)
    return [[questions_answers[i][0], questions_answers[i][1]] for i in labels[0]]


def list_return(user_query) -> list:
    # Buffer
    return search(user_query, index, questions_answers)


folder_path = Path(__file__).resolve().parent.parent / "rofls"
index_path = 'hnsw_index.bin'
vectors_path = 'vectors.npy'
qa_path = 'questions_answers.pkl'


if os.path.exists(index_path) and os.path.exists(vectors_path) and os.path.exists(qa_path):
    vectors = np.load(vectors_path)
    dim = vectors.shape[1]

    index = hnswlib.Index(space='cosine', dim=dim)
    index.load_index(index_path)

    with open(qa_path, 'rb') as f:
        questions_answers = pickle.load(f)
else:
    questions_answers = read_and_preprocess_data(folder_path)
    questions = [qa[1] for qa in questions_answers]
    vectors = vectorize_questions(questions)
    dim = vectors.shape[1]

    index = create_hnsw_index(vectors)

    index.save_index(index_path)
    np.save(vectors_path, vectors)
    with open(qa_path, 'wb') as f:
        pickle.dump(questions_answers, f)