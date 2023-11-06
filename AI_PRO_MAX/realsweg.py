import re
import json
from gensim.models import Word2Vec, KeyedVectors
from AI_PRO_MAX import hash_list

with open('./AI_PRO_MAX/index.json', 'r', encoding='utf-8') as f_json:
    loaded_index = json.load(f_json)
rhash = hash_list.hash_creator()

w2v_model = KeyedVectors.load_word2vec_format('./AI_PRO_MAX/model.bin', binary=True)


# Функция для поиска файлов и позиций вопросов по заданному вопросу


# Выполним поиск по индексу
def search_with_w2v_synonyms(question, index, w2v_model, topn=6):
    results = set()
    for word in re.sub(r'[^\w\s]', '', question.lower()).split():
        # Добавляем слово в поиск
        search_terms = [word]
        # Если слово есть в модели, ищем его синонимы
        if word in w2v_model:
            search_terms.extend([similar[0] for similar in w2v_model.most_similar(word, topn=topn)])
        # Для каждого поискового термина обновляем результаты
        for term in search_terms:
            if term in index:
                results.update(tuple(i) for i in index[term])
    return results


def list_return(sample_question: str) -> list:
    list = []
    for i in search_with_w2v_synonyms(sample_question, loaded_index, w2v_model, topn=6):
        list.append(rhash[f'{i[0]}.txt'][i[1]])
    return list


if __name__ == '__main__':
    for i in list_return("Чем мне удобрить свеклу?"):
        print(i)
