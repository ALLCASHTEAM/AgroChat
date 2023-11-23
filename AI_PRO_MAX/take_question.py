import string
import nltk
from AI_PRO_MAX import iterpritator

def Process_query(text):
    #
    print("\nscript: take_question.py\n################################# ОБРАБОТКА ЗАПРОСА #################################\n")
    print("Запрос на входе: ",text,"\n")
    upd_text = iterpritator.interpritator_with_history(text).replace("<extra_id_0> ",  "").replace("?</s>", "").lower()

    print("Обработанный запрос: ", upd_text, "\n")

    return(upd_text)

#Process_query("Муха вЕСиТ 10 грамм, а не 10 милиграмм?") #тк этот скрипт сам не должен запускаться это оставлю в комменте, потом удалим