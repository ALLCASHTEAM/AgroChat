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
                 "content": "Ты Aigro, автоматический помощник от компании щелково агрохим. Используй контекст для ответа на вопросы."},
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
                 "content": "You are Aigro, an automatic assistant. You represent the Agrochem company. Use context to answer the question .Use context if you need it.<|end_of_turn|>"},
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
    answer = model.create_chat_completion(temperature=1, top_p=0.99, top_k=50, messages=messages)
    print(answer)
    return answer["choices"][0]["message"]["content"]
