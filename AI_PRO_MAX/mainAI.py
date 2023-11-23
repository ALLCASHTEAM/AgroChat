from AI_PRO_MAX import iterpritator, KBQA, gen_engine, take_question

model, tokens = gen_engine.interact()


def AI_COMPIL(question):
    processed_question = take_question.Process_query(question)

    print("\n\n\nУ нас есть: \n", processed_question)
    answer = gen_engine.generate(question, tokens, model, KBQA.KBQA_search(processed_question))
    answer = answer.replace("Agrochat: ", "").replace("Выход:", '').replace("BioStim Start", "Биостим Старт").replace("BioStim", "Биостим").replace("biostim", "Биостим").replace("Answer:", "")
    print(answer)
    with open('tmp.txt', 'w', encoding='utf-8') as tmp_file:
        tmp_file.write(processed_question)
        tmp_file.write('\n')
        tmp_file.write(answer)
    return answer
