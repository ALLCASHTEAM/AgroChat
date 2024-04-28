import os
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
from pathlib import Path

model = SentenceTransformer('intfloat/multilingual-e5-large')


def read_and_preprocess_data(folder_path):
    # Прочитка всех txt в папке
    folder_path = Path(folder_path)
    return [(parts[0], parts[1]) for file in folder_path.glob("*.txt") for parts in
            [line.strip().split(" | ") for line in file.open('r', encoding='utf-8')] if len(parts) == 2]


def vectorize_questions(questions):
    # Вопросы трансформируем в векторы
    return model.encode(questions, normalize_embeddings=True)


def create_faiss_index(vectors):
    # Создание индексов векторов (см. выше)
    dimension = vectors.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(vectors)
    return index


def search(query, index, questions_answers, top_k=15):
    """
    Поиск подходящих данных
    :param query:
    :param index:
    :param questions_answers:
    :param top_k:
    :return: массив из 15 элементов формата [[вопрос, ответ]]
    """
    query_vector = vectorize_questions([query])[0].astype('float32')
    distances, indices = index.search(np.array([query_vector]), top_k)
    return [[questions_answers[i][0], questions_answers[i][1]] for i in indices[0]]


def list_return(user_query) -> list:
    # буферка
    return search(user_query, index, questions_answers)


# инициализация всего что нужно для работы
folder_path = Path(__file__).resolve().parent.parent / "rofls"
questions_answers = read_and_preprocess_data(folder_path)
questions = [qa[1] for qa in questions_answers]
vectors = vectorize_questions(questions)
index = create_faiss_index(np.array(vectors).astype('float32'))
