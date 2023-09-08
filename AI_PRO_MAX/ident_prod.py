import take_question
import os
import nltk
from nltk.stem import SnowballStemmer

text = "Что такое биосостим кукуруз?"  # Замените на запрос пользователя

# Инициализация стеммера (русский язык)
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')
nltk.download('sentiwordnet')
stemmer = SnowballStemmer("russian")

def product_identification(text):
    query = take_question.Process_query(text)  # Обработка запроса

    prods = []

    # Определение названий всех товаров по названиям файлов в папке rofls
    now_dir = os.path.dirname(os.path.abspath(__file__))
    ai_pro_max = os.path.dirname(now_dir)
    dir_rofls = os.path.join(ai_pro_max, "rofls")
    prods_names = os.listdir(dir_rofls)

    # Добавление всех названий в массив
    for prod in prods_names:
        prods.append(prod.replace(".txt", "").replace(",", "").replace("+", "").replace("-", ""))

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
    print("################################ ОПРЕДЕЛЕНИЕ ТОВАРА О КОТОРОМ ИДЁТ РЕЧЬ #################################\n")
    if best_product:
        print(best_product)
    else:
        best_product = "None"
        print("No match found.")
    print("\n################################ КОНЕЦ ОПРЕДЕЛЕНИЕ ТОВАРА #################################")

    return best_product

product_identification(text)
