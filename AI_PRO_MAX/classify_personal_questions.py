import joblib
import sys

# Загрузка модели и векторизатора
model = joblib.load('logistic_model_personal_questions.pkl')
vectorizer = joblib.load('tfidf_vectorizer_personal_questions.pkl')


def is_personal(question):
    # Очистка и векторизация вопроса
    question_clean = question.replace('[^\w\s]', '').lower()
    question_vectorized = vectorizer.transform([question_clean])
    # Предсказание с помощью модели
    prediction = model.predict(question_vectorized)
    return prediction[0] == 1

def kbqa(question):
    pass
# Входное предложение
# input_sentence = "Чем удобрить свеклу?"

# Вывод результата
# print(is_personal(input_sentence))
