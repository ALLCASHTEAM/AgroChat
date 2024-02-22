import os
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
from pathlib import Path
model = SentenceTransformer('hivaze/ru-e5-large')


def read_and_preprocess_data(folder_path):
    questions_answers = []
    for file_name in os.listdir(folder_path):
        if file_name.endswith(".txt"):
            file_path = os.path.join(folder_path, file_name)
            with open(file_path, 'r', encoding='utf-8') as file:
                for line in file:
                    parts = line.strip().split(" | ")
                    if len(parts) == 2:
                        questions_answers.append((parts[0], parts[1]))
    return questions_answers


def vectorize_questions(questions):
    return model.encode(questions)


def create_faiss_index(vectors):
    dimension = vectors.shape[1]  # Получаем размерность векторов
    index = faiss.IndexFlatL2(dimension)  # Создаем индекс для L2 расстояния
    index.add(vectors)  # Добавляем векторы в индекс
    return index


def search(query, index, questions_answers, top_k=30):
    query_vector = vectorize_questions([query])[0].astype('float32')  # Векторизуем запрос
    distances, indices = index.search(np.array([query_vector]), top_k)  # Поиск в Faiss
    answer = [[questions_answers[i][0], questions_answers[i][1]] for j, i in enumerate(indices[0])]
    return answer


def list_return(user_query) -> list: # Замените на интересующий вопрос
    return search(user_query, index, questions_answers)


folder_path = Path(__file__).resolve().parent.parent / "rofls"
questions_answers = read_and_preprocess_data(folder_path)
questions = [qa[1] for qa in questions_answers]  # Извлекаем вопросы
vectors = vectorize_questions(questions)
index = create_faiss_index(np.array(vectors).astype('float32'))
