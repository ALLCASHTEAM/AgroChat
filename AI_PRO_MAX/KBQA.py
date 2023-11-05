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
        return matches[0], liness
    except:
        return None


def KBQA_search(user_query):
    sentence_model = initialize_sentence_model()
    matches, liness = find_best_matches(user_query, sentence_model)
    best_result = list(map(lambda x: str(x).replace("('", "").split("?")[0], matches))
    found_answers = ''
    for question in best_result:
        for q, a in liness:
            if q.strip().lower().replace('?', '') == question.strip().lower():
                found_answers += f',{a}'
    found_answers = found_answers[1:]
    print(found_answers)
    print("\nscript: KBQA.py\n################################ ПОИСК ПО БАЗЕ ЗНАНИЙ #################################")
    print("Вопрос пользователя: ", user_query)
    print("\n################################ КОНЕЦ ПОИСКА ПО БАЗЕ ЗНАНИЙ #################################")
    return (found_answers)


if __name__ == "__main__":
    user_query = "Чем обрабатывать сою?"
    KBQA_search(user_query)
