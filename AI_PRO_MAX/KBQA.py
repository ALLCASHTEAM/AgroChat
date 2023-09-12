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

    document_embeddings = sentence_model.encode(lines)
    query_embedding = sentence_model.encode(user_query)

    similarities = util.pytorch_cos_sim(query_embedding, document_embeddings)[0]

    # Создаем список совпадений и их оценок вместе с исходными индексами строк
    matches = [(lines[i], similarities[i], i) for i in range(len(lines))]

    # Сортируем список совпадений по оценкам в убывающем порядке
    matches.sort(key=lambda x: x[1], reverse=True)

    return matches

if __name__ == "__main__":
    user_query = "Для чего используется биостим кукуруз?"
    sentence_model = initialize_sentence_model()
    matches = find_best_matches(user_query, sentence_model)
    best_result = str(matches[0])
    print(best_result)
    print("\nscript: KBQA.py\n################################ ПОИСК ПО БАЗЕ ЗНАНИЙ #################################")
    print("Вопрос пользователя: ", user_query)

    print("Подобран похожий вопрос: ", best_result.split('|')[0].strip().replace("('", ""), "\nПодобран ответ: ", best_result.split('|')[1].strip().split('\\n')[0].strip(), "\nScore: ", best_result.split("tensor(")[1].split(")")[0])

    print("\n################################ КОНЕЦ ПОИСКА ПО БАЗЕ ЗНАНИЙ #################################")
