import ident_prod
from sentence_transformers import SentenceTransformer, util
import torch
import os
import upgrade_kbqa
import Search_script


def initialize_sentence_model():
    model_name = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
    sentence_model = SentenceTransformer(model_name)
    return sentence_model


def find_best_matches(user_query, sentence_model,file_name):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    file_path = os.path.join(project_root, "rofls", f"{file_name}.txt")

    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    lines = list(map(lambda x: x.split("|")[0], lines))
    similarities = util.pytorch_cos_sim(sentence_model.encode(user_query.lower()), sentence_model.encode(list(map(lambda x: x.lower(), lines))))[0]

    # Создаем список совпадений и их оценок вместе с исходными индексами строк
    searcher = Search_script.Search(upgrade_kbqa.cosine_similarity1([user_query], file_name.lower().split(' ')))
    matches = [(lines[i], similarities[i], i) for i in range(len(lines)) if searcher.search(upgrade_kbqa.word_tokenize1(lines[i].lower().split(" ")))]

    # Сортируем список совпадений по оценкам в убывающем порядке
    matches.sort(key=lambda x: x[1], reverse=True)

    return matches


if __name__ == "__main__":
    user_query = "Преимущества биостим кукуруза?"
def KBQA_search(user_query, file_name):
    sentence_model = initialize_sentence_model()
    matches = find_best_matches(user_query, sentence_model, file_name)
    answer = ""
    best_result = str(matches[0])
    #############################################################
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    file_path = os.path.join(project_root, "rofls", f"{file_name}.txt")
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            # Проверяем, содержит ли строка первую половину
            if best_result in line:
                # Если да, выводим эту строку
                answer = line.replace(best_result, "").replace("|", "")
    ###############################################################
    print(best_result)
    print("\nscript: KBQA.py\n################################ ПОИСК ПО БАЗЕ ЗНАНИЙ #################################")
    print("Вопрос пользователя: ", user_query)

    print("Подобран похожий вопрос: ", best_result.split(',')[0].strip().replace("('", ""), 'Score:',
          # best_result.split('|')[1].strip().split('\\n')[0].strip(), "\nScore: ",
          best_result.split(", tensor(")[1].split(")")[0])

    print("\nТоп 4 варианта по скор: ")
    for i in range(1, len(matches)):
        if i > 4:
            break
        # print("Топ ", i, ": ", str(matches[i]).split('|')[0].strip().replace("('", ""), "\nПодобран ответ: ",
        #       str(matches[i]).split('|')[1].strip().split('\\n')[0].strip(), "\nScore: ",
        #       str(matches[i]).split("tensor(")[1].split(")")[0])
    print("\n################################ КОНЕЦ ПОИСКА ПО БАЗЕ ЗНАНИЙ #################################")
    return (answer)