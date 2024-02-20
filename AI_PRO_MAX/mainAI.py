from AI_PRO_MAX import iterpritator, KBQA, gen_engine
import random

model = gen_engine.interact()


def AI_COMPIL(dialog: list[str]) -> str:
    print("INFO: Вход:", dialog)
    processed_question = iterpritator.interpretator_with_history(dialog).replace("<extra_id_0> ", "").replace("?</s>", "").lower()
    print("INFO: Интерпретация: ", processed_question)
    answer = gen_engine.generate(dialog, model, KBQA.KBQA_search(processed_question))
    print("INFO: Ответ генератора", answer)
    answer = answer.replace("GPT4", "").replace("GPT:", '', 1).replace("Answer:", "").replace("Agrochem", 'Агрохим').replace("Context:", "").replace("GPT 4:", "").replace("GPT-4:", "").replace("GPT", "").replace("G", "").replace("GPT4 Correct Assistant:", "").replace("Correct", "").replace("<|end_of_turn|>", "")
    answer = answer.replace("[/INST]", "").replace("[/SYS]", "").replace("ГПТ4 Asistant:", '').replace("Asistant:", '').replace('text:', '')
    if len(answer) > 0:
        return answer
    else:
        defaultMessage = ["Спасибо за ваше сообщение. Давайте попробуем ещё раз, или вы можете уточнить ваш вопрос для более конкретного ответа.","Я готов помочь вам дальше. Пожалуйста, предоставьте дополнительную информацию или задайте другой вопрос.", "Мне бы хотелось лучше понять ваш запрос. Можете ли вы переформулировать или задать дополнительный вопрос?"]
        return random.choice(defaultMessage)