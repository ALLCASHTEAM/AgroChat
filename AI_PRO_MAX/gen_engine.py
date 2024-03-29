from llama_cpp import Llama


def interact():
    model = Llama(
        model_path='./AI_PRO_MAX/model-q16_0.gguf',
        n_ctx=8192,
        n_gpu_layers=-1,
        chat_format="llama-2"

    )

    return model


def generate(question, model, context=False):
    if context:
        if len(question) == 1 or len(question) == 2:
            messages = [
                {"role": "system",
                 "content": "You are Aigro, an automatic assistant. You represent the Agrochem company. Use context to answer the question. <|end_of_turn|>"},
                {
                    "role": "user",
                    "content": f"Context:{context.replace(';','')} GPT4 User:{question[0].replace('text:', '')}<|end_of_turn|>GPT4 Assistant:"
                }
            ]
        else:
            messages = [
                {"role": "system",
                 "content": "You are Aigro, an automatic assistant. You represent the Agrochem company. Use context to answer the question <|end_of_turn|>"},
                {
                    "role": "user",
                    "content": f"GPT4 User:{question[0].replace('text:', '')}<|end_of_turn|>GPT4 Assistant:"
                },
                {
                    "role": "assistant",
                    "content": f"GPT4 Assistant:{question[1].replace('text:', '')}<|end_of_turn|>"
                },
                {
                    "role": "user",
                    "content": f"Context:{context.replace(';','')} GPT4 User:{question[2].replace('text:', '')}<|end_of_turn|>GPT4 Assistant:"
                }
            ]
    else:
        if len(question) == 1 or len(question) == 2:
            messages = [
                {"role": "system",
                 "content": "You are Aigro, an automatic assistant. You represent the Agrochem company. Answer me briefly. <|end_of_turn|>"},
                {
                    "role": "user",
                    "content": f"GPT4 User:{question[0].replace('text:', '')}<|end_of_turn|>GPT4 Assistant:"
                }
            ]
        else:
            messages = [
                {"role": "system",
                 "content": "You are Aigro, an automatic assistant. You represent the Agrochem company. Answer me briefly. <|end_of_turn|>"},
                {
                    "role": "user",
                    "content": f"GPT4 User:{question[0].replace('text:', '')}<|end_of_turn|>GPT4 Assistant:"
                },
                {
                    "role": "assistant",
                    "content": f"GPT4 Assistant:{question[1].replace('text:', '')}<|end_of_turn|>"
                },
                {
                    "role": "user",
                    "content": f"GPT4 User:{question[2].replace('text:', '')}<|end_of_turn|>GPT4 Assistant:"
                }
            ]
    answer = model.create_chat_completion(temperature=0.3, top_p=0.8, top_k=35, messages=messages,)
    print(answer)
    return answer["choices"][0]["message"]["content"]
