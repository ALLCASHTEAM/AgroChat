import string
import nltk
import iterpritator

def Process_query(text):
    #
    print("\nscript: take_question.py\n################################# ОБРАБОТКА ЗАПРОСА #################################\n")
    print("Запрос на входе: ",text,"\n")

    dialog = "-чем полить кукурузу?\n-Биостим кукуруза подойдет для полива кукурузы\n" + text

    question = iterpritator.interpritator_with_history(dialog)

    upd_text = question.lower()

    print("Обработанный запрос: ", upd_text, "\n")

    #
    print("\n################################# КОНЕЦ ОБРАБОТКИ ЗАПРОСА #################################")
    return(upd_text)

#Process_query("Муха вЕСиТ 10 грамм, а не 10 милиграмм?") #тк этот скрипт сам не должен запускаться это оставлю в комменте, потом удалим