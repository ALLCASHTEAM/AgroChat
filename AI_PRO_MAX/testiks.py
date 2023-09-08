import ident_prod
from sentence_transformers import SentenceTransformer, util
import torch
import os

def initialize_sentence_model():
    model_name = "Den4ikAI/sbert_large_mt_ru_retriever"
    sentence_model = SentenceTransformer(model_name)
    return sentence_model

def find_best_matches(user_query, sentence_model):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    ident_file = ident_prod.product_identification(user_query)
    file_path = os.path.join(project_root, "rofls", f"{ident_file}.txt")

    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # Разделяем каждую строку на две части: текст до символа "|" и текст после "|"
    line_parts = [line.strip().split('|', 1) for line in lines]
    document_texts = [part[0] for part in line_parts]  # Текст до "|"

    query_embedding = sentence_model.encode(user_query)

    # Кодируем только текст до "|" для строк из базы знаний
    document_embeddings = sentence_model.encode(document_texts)

    similarities = util.pytorch_cos_sim(query_embedding, document_embeddings)[0]

    # Создаем список совпадений и их оценок вместе с полными строками и исходными индексами строк
    matches = [(lines[i], similarities[i], i) for i in range(len(lines))]

    # Сортируем список совпадений по оценкам в убывающем порядке
    matches.sort(key=lambda x: x[1], reverse=True)

    return matches

if __name__ == "__main__":
    user_query = "Для чего используется биостим кукуруз?"
    sentence_model = initialize_sentence_model()
    matches = find_best_matches(user_query, sentence_model)

    print("\nscript: KBQA.py\n################################ ПОИСК ПО БАЗЕ ЗНАНИЙ #################################")
    print("Вопрос пользователя: ", user_query)

    for i, (match, similarity_score, original_index) in enumerate(matches, 1):
        print(f"Исходный номер строки: {original_index + 1}")
        print(f"Строка {i}: {match.strip()}")
        print(f"Скор совпадения: {similarity_score:.2f}\n")

    print("\n################################ КОНЕЦ ПОИСКА ПО БАЗЕ ЗНАНИЙ #################################")
