from AI_PRO_MAX import take_question
import os
import nltk
from nltk.stem import SnowballStemmer

# Инициализация стеммера (русский язык) ПРИ ПЕРВОМ ЗАПУСКЕ НА МАШИНЕ, ВЫТАЩИТЬ ИЗ КОММЕНТА
#nltk.download('punkt')
#nltk.download('stopwords')
#nltk.download('wordnet')
#nltk.download('averaged_perceptron_tagger')
#nltk.download('sentiwordnet')
stemmer = SnowballStemmer("russian")

def product_identification(text):
    temp_query = take_question.Process_query(text)  # Обработка запроса
    query = temp_query.replace("<extra_id_0>", "").replace("</s>","").replace("?","")
    prods = []
    rel_prods = []

    # Определение названий всех товаров по названиям файлов в папке rofls
    now_dir = os.path.dirname(os.path.abspath(__file__))
    ai_pro_max = os.path.dirname(now_dir)
    dir_rofls = os.path.join(ai_pro_max, "rofls")
    prods_names = os.listdir(dir_rofls)

    # Добавление всех названий в массив
    for prod in prods_names:
        rel_prods.append(prod.replace(".txt", ""))
        prods.append(prod.replace(".txt", "").replace(",", "").replace("+", "").replace("-", "").lower())

    # Сплит запроса на отдельные слова и выполнение стемминга
    query_words = [stemmer.stem(word) for word in query.split()]

    max_matching_words = 0
    best_product = ""

    for product in prods:
        # Сплит названия товара и выполнение стемминга
        product_words = [stemmer.stem(word) for word in product.split()]

        matching_words_count = sum(1 for query_word in query_words if
                                   query_word.lower() in [product_word.lower() for product_word in product_words])

        if matching_words_count > max_matching_words:
            max_matching_words = matching_words_count
            best_product = product
        elif matching_words_count == max_matching_words and len(best_product) > len(product):
            best_product = product

    # Вывод результатов поиска
    print("\nscript: ident_prod.py\n################################ ОПРЕДЕЛЕНИЕ ТОВАРА О КОТОРОМ ИДЁТ РЕЧЬ #################################\n","\nЗапрос на входе: ",query)
    if best_product:
        pass
        #print("Товар называется: ",best_product, "\n Название файла: ", rel_prods[indx])
    else:
        best_product = "profile_facts"
        #print("No match found.")

    # Ищем индекс элемента в массиве
    indx = prods.index(best_product)

    # Выводим индекс
    if(best_product == "profile_facts"):
        print("Товар называется: ", best_product, "\nНазвание файла: ", rel_prods[indx])
    else:
        print("Товар называется: ", best_product, "\nНазвание файла: ", rel_prods[indx])

    print("\n################################ КОНЕЦ ОПРЕДЕЛЕНИЕ ТОВАРА #################################")
    return rel_prods[indx]

#product_identification(text)#тк этот скрипт сам не должен запускаться это оставлю в комменте, потом удалим
