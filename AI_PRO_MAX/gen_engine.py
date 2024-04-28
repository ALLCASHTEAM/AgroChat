from llama_cpp import Llama


def interact():
    """
    Функция инициализации модели

    model_path - путь к файлу модели
    n_ctx - размер контекста модели (должно писаться в конфигах модели)
    n_gpu_layers - кол-во слоев на gpu (-1 значит грузить все)
    chat_format - формат чата
    :return model:
    """
    model = Llama(
        model_path='./AI_PRO_MAX/model-q16_0.gguf',
        n_ctx=8192,
        n_gpu_layers=-1,
        chat_format="llama-2"

    )

    return model


def generate(question, model, context=False):
    if context:
        # КОНТЕКСТ
        if len(question) == 1 or len(question) == 2:
            # ЕСЛИ ПЕРВОЕ СООБЩЕНИЕ
            messages = [
                {"role": "system",
                 "content": "You are Aigro, an automatic assistant. You represent the Agrochem company. Use context if you need it. Use context to answer the question.<|end_of_turn|>"},
                {
                    "role": "user",
                    "content": f"Context: {context.replace(';','')} GPT4 Correct User: {question[0].replace('text:', '')}<|end_of_turn|>GPT4 Correct Assistant:"
                }
            ]
        else:
            # ЕСЛИ УЖЕ ЕСТЬ ДИАЛОГ
            messages = [
                {"role": "system",
                 "content": "You are Aigro, an automatic assistant. You represent the Agrochem company.Use context to answer the question .Use context if you need it.<|end_of_turn|>"},
                {
                    "role": "user",
                    "content": f"GPT4 Correct User: {question[0].replace('text:', '')}<|end_of_turn|>"
                },
                {
                    "role": "assistant",
                    "content": f"GPT4 Correct Assistant: {question[1].replace('text:', '')}<|end_of_turn|>"
                },
                {
                    "role": "user",
                    "content": f"Context: {context.replace(';','')} GPT4 Correct User: {question[2].replace('text:', '')}<|end_of_turn|>GPT4 Correct Assistant:"
                }
            ]
    else:
        # КОНТЕКСТА НЕТ
        if len(question) == 1 or len(question) == 2:
            # ЕСЛИ ПЕРВОЕ СООБЩЕНИЕ
            messages = [
                {"role": "system",
                 "content": "You are Aigro, an automatic assistant. You represent the Agrochem company. Answer me briefly.<|end_of_turn|>"},
                {
                    "role": "user",
                    "content": f"GPT4 Correct User: {question[0].replace('text:', '')}<|end_of_turn|>GPT4 Correct Assistant:"
                }
            ]
        else:
            # ЕСЛИ УЖЕ ЕСТЬ ДИАЛОГ
            messages = [
                {"role": "system",
                 "content": "You are Aigro, an automatic assistant. You represent the Agrochem company. Answer me briefly.<|end_of_turn|>"},
                {
                    "role": "user",
                    "content": f"GPT4 Correct User: {question[0].replace('text:', '')}<|end_of_turn|>"
                },
                {
                    "role": "assistant",
                    "content": f"GPT4 Assistant: {question[1].replace('text:', '')}<|end_of_turn|>"
                },
                {
                    "role": "user",
                    "content": f"GPT4 Correct User: {question[2].replace('text:', '')}<|end_of_turn|>GPT4 Correct Assistant:"
                }
            ]
    answer = model.create_chat_completion(temperature=0, top_p=0.85, top_k=30, messages=messages,)
    print(answer)
    return answer["choices"][0]["message"]["content"]
