from AI_PRO_MAX import KBQA, gen_engine
from AI_PRO_MAX.iterpritator import interpretator_with_history
import random
import re

model = gen_engine.interact()


def AI_COMPIL(dialog: list[str], imageFlag=False) -> str:
    print("INFO: Вход:", dialog)
    if imageFlag:
        answer = gen_engine.generate(dialog, model, KBQA.KBQA_search(dialog))
        print("INFO: Ответ генератора", answer)
    else:
        processed_question = interpretator_with_history(dialog).replace("<extra_id_0> ", "").replace("</s>", "").lower()
        print("INFO: Интерпретация: ", processed_question)
        answer = gen_engine.generate(dialog, model, KBQA.KBQA_search(processed_question))
        print("INFO: Ответ генератора", answer)

    replacements = [
        ("[\\[A-Z]+]", ""), ("GPT4", ""),  ("GPT-3 ", ""), ("Answer:", ""), ("<https://betaren.ru>", "https://betaren.ru"),
        ("Agrochem", 'Агрохим'), ("Context:", ""), ("GPT 4:", ""), ("GPT-4:", ""),
        ("GPT", ""), ("G", ""), ("GPT4 Correct Assistant:", ""), ("Correct", ""),
        ("<[^>]+>", ""), ("ГПТ4 Asistant:", ''), ("Asistant:", ''), ('text:', ''),
        ('GPT-4', "Аигро"),("GPT:", ""), ("OpenAI", "Агрохим")
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


def regenerate(dialog: list[str]):
    print("INFO: Вход для регенерации:", dialog)
    if not dialog:
        return "Ошибка: Нет данных для регенерации."

    # Добавляем к последнему сообщению метку о том, что это был неправильный ответ
    modified_dialog = dialog + [f"Неправильный ответ: {dialog[-1]}"] if dialog else dialog

    # Обработка и генерация нового ответа
    processed_question = interpretator_with_history(modified_dialog).replace("<extra_id_0> ", "").replace("</s>",
                                                                                                          "").lower()
    print("INFO: Интерпретация для регенерации: ", processed_question)
    answer = gen_engine.generate(modified_dialog, model, KBQA.KBQA_search(processed_question))
    print("INFO: Ответ генератора после регенерации", answer)

    # Применение замен в ответе
    replacements = [
        ("[\\[A-Z]+]", ""), ("GPT4", ""), ("GPT-3 ", ""), ("Answer:", ""),
        ("<https://betaren.ru>", "https://betaren.ru"),
        ("Agrochem", 'Агрохим'), ("Context:", ""), ("GPT 4:", ""), ("GPT-4:", ""),
        ("GPT", ""), ("G", ""), ("GPT4 Correct Assistant:", ""), ("Correct", ""),
        ("<[^>]+>", ""), ("ГПТ4 Asistant:", ''), ("Asistant:", ''), ('text:', ''),
        ('GPT-4', "Аигро"), ("GPT:", ""), ("OpenAI", "Агрохим")
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
