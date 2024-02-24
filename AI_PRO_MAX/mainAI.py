from AI_PRO_MAX import KBQA, gen_engine
from AI_PRO_MAX.iterpritator import interpretator_with_history
import random
import re

model = gen_engine.interact()


def AI_COMPIL(dialog: list[str]) -> str:
    print("INFO: Вход:", dialog)
    processed_question = interpretator_with_history(dialog).replace("<extra_id_0> ", "").replace("?</s>", "").lower()
    print("INFO: Интерпретация: ", processed_question)
    answer = gen_engine.generate(dialog, model, KBQA.KBQA_search(processed_question))
    print("INFO: Ответ генератора", answer)

    replacements = [
        ("[\\[A-Z]+]", ""), ("GPT4", ""), ("GPT:", ""), ("Answer:", ""),
        ("Agrochem", 'Агрохим'), ("Context:", ""), ("GPT 4:", ""), ("GPT-4:", ""),
        ("GPT", ""), ("G", ""), ("GPT4 Correct Assistant:", ""), ("Correct", ""),
        ("<[^>]+>", ""), ("ГПТ4 Asistant:", ''), ("Asistant:", ''), ('text:', '')
    ]
    for old, new in replacements:
        answer = re.sub(old, new, answer)
    answer.replace("*", "")
    # Выбор случайного сообщения, если ответ пуст
    if len(answer.strip()) > 0:
        return answer.strip()
    else:
        default_messages = [
            "Спасибо за ваше сообщение. Давайте попробуем ещё раз, или вы можете уточнить ваш вопрос для более конкретного ответа.",
            "Я готов помочь вам дальше. Пожалуйста, предоставьте дополнительную информацию или задайте другой вопрос.",
            "Мне бы хотелось лучше понять ваш запрос. Можете ли вы переформулировать или задать дополнительный вопрос?"
        ]
        return random.choice(default_messages)