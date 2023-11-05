from AI_PRO_MAX import ident_prod,  realsweg
from sentence_transformers import SentenceTransformer, util
import torch
import os

def initialize_sentence_model():
    model_name = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
    sentence_model = SentenceTransformer(model_name, device='cuda')
    return sentence_model


def find_best_matches(user_query, sentence_model):
    liness = realsweg.list_return(user_query)
    liness = list(map(lambda x: x.split("|"), liness))
    lines = list(zip(*liness))[0]
    try:
        similarities = util.pytorch_cos_sim(sentence_model.encode(user_query.lower()),
                                            sentence_model.encode(list(map(lambda x: x.lower(), lines))))[0]

        # Создаем список совпадений и их оценок вместе с исходными индексами строк
        matches = [(lines[i], similarities[i], i) for i in range(len(lines))]

        # Сортируем список совпадений по оценкам в убывающем порядке
        matches.sort(key=lambda x: x[1], reverse=True)
        return matches[:3], liness
    except:
        return None


def KBQA_search(user_query):
    sentence_model = initialize_sentence_model()
    matches, liness = find_best_matches(user_query, sentence_model)
    answer = ""
    best_result = list(map(lambda x: str(x).replace("('", "").split("?")[0], matches))
    print(best_result)
    for line in liness:
        # Проверяем, содержит ли строка первую половину
        if line[0].replace('?', '').lower().strip() in list(map(lambda x: x.lower().strip(), best_result)):
            # Если да, выводим эту строку
            answer += line[1]
    print(answer)
    print("\nscript: KBQA.py\n################################ ПОИСК ПО БАЗЕ ЗНАНИЙ #################################")
    print("Вопрос пользователя: ", user_query)
    print("\n################################ КОНЕЦ ПОИСКА ПО БАЗЕ ЗНАНИЙ #################################")
    return (answer)


if __name__ == "__main__":
    user_query = "Чем обрабатывать кукурузу?"
    KBQA_search(user_query)
