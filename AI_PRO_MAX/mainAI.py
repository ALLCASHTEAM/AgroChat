from AI_PRO_MAX import ident_prod, iterpritator, KBQA, take_question

dialog = "-чем полить кукурузу?\n-Биостим кукуруза подойдет для полива кукурузы\n"
question = "как его использовать?"


def AI_COMPIL(dialog, question):
    processed_question = iterpritator.interpritator_with_history(dialog + question).replace("<extra_id_0> ","").replace("?</s>","")

    file_name = ident_prod.product_identification(processed_question)

    print("\n\n\nУ нас есть: \n", processed_question)
    print(file_name)
    answer = KBQA.KBQA_search(processed_question, file_name)



    return(answer)
