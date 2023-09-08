import string
import nltk


def Process_query(text):
    #
    print("\nscript: take_question.py\n################################# ОБРАБОТКА ЗАПРОСА #################################\n")
    print("Запрос на входе: ",text,"\n")

    upd_text = text.translate(str.maketrans('', '', string.punctuation)).lower()

    print("Обработанный запрос: ", upd_text, "\n")

    #
    print("\n################################# КОНЕЦ ОБРАБОТКИ ЗАПРОСА #################################")
    return(upd_text)

#Process_query("Муха вЕСиТ 10 грамм, а не 10 милиграмм?") #тк этот скрипт сам не должен запускаться это оставлю в комменте, потом удалим