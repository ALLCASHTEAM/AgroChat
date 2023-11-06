from AI_PRO_MAX import ident_prod, realsweg
from sentence_transformers import SentenceTransformer, util
import torch
import os

def initialize_sentence_model():
    return SentenceTransformer("sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2", device='cuda')


def find_best_matches(user_query, sentence_model):
    liness = list(map(lambda x: x.split("|"), realsweg.list_return(user_query)))
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
    matches, liness = find_best_matches(user_query, initialize_sentence_model())
    answer = ""
    for line in liness:
        if line[0].replace('?', '').lower().strip() in list(map(lambda x: x.lower().strip(), list(map(lambda x: str(x).replace("('", "").split("?")[0], matches)))):
            answer += line[1]
    print(answer)
    print("\nscript: KBQA.py\n################################ ПОИСК ПО БАЗЕ ЗНАНИЙ #################################")
    print("Вопрос пользователя: ", user_query)
    print("\n################################ КОНЕЦ ПОИСКА ПО БАЗЕ ЗНАНИЙ #################################")
    return (answer)


if __name__ == "__main__":
    user_query = "Чем обрабатывать кукурузу?"
    KBQA_search(user_query)

