from AI_PRO_MAX import ident_prod, iterpritator, KBQA, gen_engine

model, tokens = gen_engine.interact()


def AI_COMPIL(dialog, question):
    file_name, processed_question = ident_prod.product_identification(question)

    print("\n\n\nУ нас есть: \n", processed_question)
    print(file_name)
    answer = gen_engine.generate(processed_question, tokens, model, KBQA.KBQA_search(processed_question, file_name))
    answer = answer.replace("Agrochat: ", "").replace("Выход:", '').replace("BioStim Start", "Биостим Старт").replace("BioStim", "Биостим").replace("biostim", "Биостим")
    print(answer)
    with open('tmp.txt', 'w', encoding='utf-8') as tmp_file:
        tmp_file.write(processed_question)
        tmp_file.write('\n')
        tmp_file.write(answer)
    return answer
