from llama_cpp import Llama


def interact():
    model = Llama(
        model_path='./AI_PRO_MAX/model-f16.gguf',
        n_ctx=8192,
        n_gpu_layers=-1,
        verbose=True,
        seed=1
    )
    return model


def generate(question, model, context=False):
    if context:
        # КОНТЕКСТ
        if len(question) == 1 or len(question) == 2:
            # ЕСЛИ ПЕРВОЕ СООБЩЕНИЕ
            messages = [
                {"role": "system",
                 "content": "Ты Aigro, автоматический помощник от компании Щелково Агрохим. Используй контекст для ответа на вопросы. Отвечай на вопрос подробно."},
                {
                    "role": "context",
                    "content": f"Используй этот контекст для ответа{context.replace(';','')}"
                },
                {
                    "role": "user",
                    "content": f"{question[0].replace('text:', '')}"
                }
            ]
        else:
            # ЕСЛИ УЖЕ ЕСТЬ ДИАЛОГ
            messages = [
                {"role": "system",
                 "content": "Ты Aigro, автоматический помощник от компании Щелково Агрохим. Используй контекст для ответа на вопросы. Отвечай на вопрос подробно."},
                {
                    "role": "user",
                    "content": f"{question[0].replace('text:', '')}"
                },
                {
                    "role": "assistant",
                    "content": f"{question[1].replace('text:', '')}"
                },
                {
                    "role": "user",
                    "content": f"Context: {context.replace(';','')} Question: {question[2].replace('text:', '')}"
                }
            ]
    else:
        # КОНТЕКСТА НЕТ
        if len(question) == 1 or len(question) == 2:
            # ЕСЛИ ПЕРВОЕ СООБЩЕНИЕ
            messages = [
                {"role": "system",
                 "content": "Ты Aigro, автоматический помощник от компании Щелково Агрохим. Отвечай на вопрос подробно."},
                {
                    "role": "user",
                    "content": f"{question[0].replace('text:', '')}"
                }
            ]
        else:
            # ЕСЛИ УЖЕ ЕСТЬ ДИАЛОГ
            messages = [
                {"role": "system",
                 "content": "Ты Aigro, автоматический помощник от компании Щелково Агрохим. Отвечай на вопрос подробно."},
                {
                    "role": "user",
                    "content": f"{question[0].replace('text:', '')}"
                },
                {
                    "role": "assistant",
                    "content": f"{question[1].replace('text:', '')}"
                },
                {
                    "role": "user",
                    "content": f"{question[2].replace('text:', '')}"
                }
            ]
    answer = model.create_chat_completion(temperature=0.7, top_p=0.7, top_k=30, messages=messages)
    print(answer)
    return answer["choices"][0]["message"]["content"]
