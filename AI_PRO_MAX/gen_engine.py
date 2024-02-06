from llama_cpp import Llama
import torch
max_tokens = 1999
def interact():
    model = Llama(
        model_path='./AI_PRO_MAX/model-q16_0.gguf',
        n_ctx=8192,
        n_gpu_layers=33,
        chat_format="llama-2",

    )

    return model


def generate(question, model, context=False):

    if context:
        answer = model.create_chat_completion(temperature=0.25, top_p=0.8, top_k=30,
            messages=[
                {"role": "system", "content": "You are Aigro, an automatic assistant. You represent the Agrochem company. Answer me briefly. <|end_of_turn|>"},
                {
                    "role": "user",
                    "content": f"Context:{context} GPT4 User:{question}<|end_of_turn|>GPT4 Assistant:"
                }
            ]
        )
    else:
        answer = model.create_chat_completion(temperature=0.25, top_p=0.8, top_k=30,
            messages=[
                {"role": "system",
                 "content": "You are Aigro, an automatic assistant. You represent the Agrochem company. Answer me briefly.<|end_of_turn|>"},
                {
                    "role": "user",
                    "content": f"GPT4 User:{question}<|end_of_turn|>GPT4 Assistant:"
                }
            ]
        )
    user_req = ["user", question, answer["promt_tokens"]]
    assistant_req = ["assistant", answer["choices"][0]["message"]["content"], answer["completion_tokens"]]
    print(user_req, '\n')
    print(assistant_req, '\n')
    dialog_history = []  # !!!#
    # Указываем максимальное количество токенов на историю
    # Дальнейший дрочreqs_sum = user_req[2] + assistant_req[2]
    sum_third_column = sum(int(row[2]) for row in dialog_history if isinstance(row[2], (int, float)))
    # Чистка истории диалога что бы новые смски вмещалисьwhile reqs_sum + sum_third_column >= max_tokens:
    dialog_history.pop(0)
    sum_third_column = sum(int(row[2]) for row in dialog_history if isinstance(row[2], (int, float)))

    # добавление после всего говна в историю
    dialog_history.append(user_req)
    dialog_history.append(assistant_req)
    #
    # Сохранение истории диалога в локал стораге#!!!
#
    return answer["choices"][0]["message"]["content"]



