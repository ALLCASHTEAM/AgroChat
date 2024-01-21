from AI_PRO_MAX import iterpritator, KBQA, gen_engine

model, tokens = gen_engine.interact()


def AI_COMPIL(question: str) -> str:
    global tokens
    print("INFO. Вход:", question)
    processed_question = iterpritator.interpretator_with_history(question).replace("<extra_id_0> ", "").replace("?</s>", "").lower()
    print("INFO. Интерпретация: ", processed_question)
    answer = gen_engine.generate(question, tokens, model, KBQA.KBQA_search(processed_question))
    answer = answer[0].replace("GPT4", "").replace("GPT:", '', 1).replace("Answer:", "").replace("Agrochem", 'Агрохим').replace("Context:", "").replace("GPT 4:", "").replace("GPT-4:", "").replace("GPT", "").replace("G", "").replace("GPT4 Correct Assistant:", "").replace("Correct", "").replace("<|end_of_turn|>", "")
    print("INFO. Ответ генератора", answer)
    with open('tmp.txt', 'w', encoding='utf-8') as tmp_file:
        tmp_file.write(processed_question)
        tmp_file.write('\n')
        tmp_file.write(answer)
    return answer
