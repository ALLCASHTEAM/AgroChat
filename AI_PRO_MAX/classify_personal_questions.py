import joblib

model = joblib.load('./AI_PRO_MAX/logistic_model_personal_questions.pkl')
vectorizer = joblib.load('./AI_PRO_MAX/tfidf_vectorizer_personal_questions.pkl')


def is_personal(question):
    question_clean = question.replace('[^\w\s]', '').lower()
    question_vectorized = vectorizer.transform([question_clean])
    # Предсказание с помощью модели
    prediction = model.predict(question_vectorized)
    return prediction[0] == 1


# input_sentence = "Чем удобрить свеклу?"
# print(is_personal(input_sentence))
