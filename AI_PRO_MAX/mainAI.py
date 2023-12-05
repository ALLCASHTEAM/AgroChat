from AI_PRO_MAX import iterpritator, KBQA, gen_engine

model, tokens = gen_engine.interact()


def AI_COMPIL(question: str) -> str:
    print("Вход:", question)
    processed_question = iterpritator.interpritator_with_history(question).replace("<extra_id_0> ",  "").replace("?</s>", "").lower()

    print("\n Интерпретация: ", processed_question)
    answer = gen_engine.generate(question, tokens, model, KBQA.KBQA_search(processed_question))
    answer = answer.replace("GPT4", "").replace("G", '', 1).replace("Answer:", "").replace("Agrochem", 'Агрохим')
    print(answer)
    with open('tmp.txt', 'w', encoding='utf-8') as tmp_file:
        tmp_file.write(processed_question)
        tmp_file.write('\n')
        tmp_file.write(answer)
    return answer
