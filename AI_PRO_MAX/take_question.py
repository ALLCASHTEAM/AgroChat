import string
from transformers import BertForMaskedLM, BertTokenizer, pipeline



def Process_query(text):
    #
    print("################################# ОБРАБОТКА ЗАПРОСА #################################")
    print("необработанный запрос: ","\n",text)
    #

    #
    upd_text = text.translate(str.maketrans('', '', string.punctuation)).lower()
    print("Убраны знаки препинания + нижний регистр: ","\n",upd_text)
    #

    #----
    print("################################# КОНЕЦ ОБРАБОТКИ ЗАПРОСА #################################")
    return(upd_text)
