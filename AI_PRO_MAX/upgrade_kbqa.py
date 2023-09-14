# Попробуем выполнить код снова
import nltk
import spacy
from gensim.models import FastText
from sklearn.metrics.pairwise import cosine_similarity
from nltk.tokenize import word_tokenize
import numpy as np


def word_tokenize1(texts):
    return [[word.lower() for word in word_tokenize(text, language="russian")] for text in
            texts]


# Примеры текстов (в реальности, этот датасет должен быть больше и разнообразнее)
def cosine_similarity1(texts, name):
    processed_texts = word_tokenize1(texts)
    # Обучение FastText модели
    model = FastText(sentences=processed_texts, vector_size=100, window=5, min_count=1, workers=4)

    def extract_keywords_fasttext(text, model, top_n=5):
        words = [word.lower() for word in word_tokenize(text, language="russian")]
        # Получение векторов для каждого слова в тексте
        word_vectors = np.array([model.wv[word] for word in words])
        # Вычисление усредненного вектора для текста
        avg_vector = np.mean(word_vectors, axis=0).reshape(1, -1)
        # Вычисление косинусного сходства между усредненным вектором и векторами слов
        similarities = cosine_similarity(avg_vector, word_vectors)
        # Получение индексов топ-N наиболее похожих слов
        top_indices = similarities.argsort()[0][::-1][:top_n]
        # Возвращаем топ-N ключевых слов
        return [words[i] for i in top_indices]

    # Пример использования функции для извлечения ключевых слов
    extracted_keywords = {text: extract_keywords_fasttext(text, model) for text in texts}
    name.append('?')
    return [x for x in extracted_keywords[texts[0]] if x not in name]
