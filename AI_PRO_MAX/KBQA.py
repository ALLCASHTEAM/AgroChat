from AI_PRO_MAX import ident_prod
from sentence_transformers import SentenceTransformer, util
import torch
import os


def initialize_sentence_model():
    model_name = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
    sentence_model = SentenceTransformer(model_name)
    return sentence_model


def find_best_matches(user_query, sentence_model,file_name):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    file_path = os.path.join(project_root, "rofls", f"{file_name}.txt")

    with open(file_path, 'r', encoding='utf-8') as file:
        liness = file.readlines()
    lines = list(map(lambda x: x.split("|")[0], liness))
    try:
        liness = list(map(lambda x: x.split("|")[1], liness))
    except:
        liness = None
    similarities = util.pytorch_cos_sim(sentence_model.encode(user_query.lower()), sentence_model.encode(list(map(lambda x: x.lower(), lines))))[0]

    # Создаем список совпадений и их оценок вместе с исходными индексами строк
    matches = [(lines[i], similarities[i], i) for i in range(len(lines)) ]

    # Сортируем список совпадений по оценкам в убывающем порядке
    matches.sort(key=lambda x: x[1], reverse=True)

    return matches




def KBQA_search(user_query, file_name):
    sentence_model = initialize_sentence_model()
    matches = find_best_matches(user_query, sentence_model, file_name)[0]
    answer = ""
    best_result = str(matches[0]).replace("('", "").split("?")[0]
    #############################################################
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    file_path = os.path.join(project_root, "rofls", f"{file_name}.txt")
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            # Проверяем, содержит ли строка первую половину
            if best_result in line:
                # Если да, выводим эту строку
                answer = line.split("|")[1]
    ###############################################################
    print(answer)
    print("\nscript: KBQA.py\n################################ ПОИСК ПО БАЗЕ ЗНАНИЙ #################################")
    print("Вопрос пользователя: ", user_query)

    print("\n################################ КОНЕЦ ПОИСКА ПО БАЗЕ ЗНАНИЙ #################################")
    return (answer)

if __name__ == "__main__":
    user_query = "Преимущества биостим кукуруза?"
    KBQA_search(user_query, ident_prod.product_identification(user_query))
