import re
import json
from gensim.models import Word2Vec, KeyedVectors
from AI_PRO_MAX import hash_list

# Путь к сохраненной модели
model_path = './model.bin'
index_json_path = './index.json'
# Загрузка модели

with open(index_json_path, 'r', encoding='utf-8') as f_json:
    loaded_index = json.load(f_json)
rhash = hash_list.hash_creator()

w2v_model = KeyedVectors.load_word2vec_format(model_path, binary=True)
# Функция для поиска файлов и позиций вопросов по заданному вопросу


# Выполним поиск по индексу
def search_with_w2v_synonyms(question, index, w2v_model, topn=6):
    # Предобработка входящего вопроса
    question_proc = re.sub(r'[^\w\s]', '', question.lower())
    words = question_proc.split()
    # Поиск соответствующих файлов и позиций вопросов
    results = set()
    for word in words:
        # Добавляем слово в поиск
        search_terms = [word]
        # Если слово есть в модели, ищем его синонимы
        if word in w2v_model:
            similar_words = w2v_model.most_similar(word, topn=topn)
            # Добавляем синонимы в поисковые термины
            search_terms.extend([similar[0] for similar in similar_words])
        # Для каждого поискового термина обновляем результаты
        for term in search_terms:
            if term in index:
                results.update(tuple(i) for i in index[term])
    return results


def list_return(sample_question: str) -> list:
    search_results_w2v = search_with_w2v_synonyms(sample_question, loaded_index, w2v_model, topn=6)
    list = []
    for i in search_results_w2v:
        list.append(rhash[f'{i[0]}.txt'][i[1]])
    return list


if __name__ == '__main__':
    for i in list_return("Чем мне удобрить свеклу?"):
        print(i)
