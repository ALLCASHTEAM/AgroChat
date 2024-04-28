from AI_PRO_MAX import KBQA, gen_engine
from AI_PRO_MAX.iterpritator import interpretator_with_history
import random
import re

model = gen_engine.interact()


def ai_main(dialog: list[str], image_flag=False, regenerate_flag=False) -> str:
    print("INFO: Вход:", dialog)
    if image_flag:
        # Если изображение
        answer = gen_engine.generate(dialog, model, KBQA.KBQA_search(dialog))
        print("INFO: Ответ генератора", answer)
    if regenerate_flag:
        # Если реген
        if not dialog:
            return "Ошибка: Нет данных для регенерации."
        processed_question = interpretator_with_history(dialog).replace("<extra_id_0> ", "").replace("</s>",
                                                                                                             "").lower()
        print("INFO: Интерпретация: ", processed_question)
        answer = gen_engine.generate(dialog, model, KBQA.KBQA_search(processed_question))
        print("INFO: Ответ генератора", answer)
    else:
        # Дефолт
        processed_question = interpretator_with_history(dialog).replace("<extra_id_0> ", "").replace("</s>", "").lower()
        print("INFO: Интерпретация: ", processed_question)
        answer = gen_engine.generate(dialog, model, KBQA.KBQA_search(processed_question))
        print("INFO: Ответ генератора", answer)

    replacements = [
        ("[\\[A-Z]+]", ""), ("GPT4", ""),  ("GPT-3 ", ""), ("Answer:", ""), ("<https://betaren.ru>", "https://betaren.ru"),
        ("Agrochem", 'Агрохим'), ("Context:", ""), ("GPT 4:", ""), ("GPT-4:", ""),
        ("GPT", ""), ("G", ""), ("GPT4 Correct Assistant:", ""), ("Correct", ""),
        ("<[^>]+>", ""), ("ГПТ4 Asistant:", ''), ("Asistant:", ''), ('text:', ''),
        ('GPT-4', "Аигро"),("GPT:", ""), ("OpenAI", "Агрохим"), ("[/", '')
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
