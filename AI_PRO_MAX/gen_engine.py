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
        if len(question) == 1:
            messages=[
                {"role": "system", "content": "You are Aigro, an automatic assistant. You represent the Agrochem company. Answer me briefly. <|end_of_turn|>"},
                {
                    "role": "user",
                    "content": f"Context:{context} GPT4 User:{question[0]}<|end_of_turn|>GPT4 Assistant:"
                }
            ]
        else:
            messages=[
                {"role": "system", "content": "You are Aigro, an automatic assistant. You represent the Agrochem company. Answer me briefly. <|end_of_turn|>"},
                {
                    "role": "user",
                    "content": f"GPT4 User:{question[0]}<|end_of_turn|>GPT4 Assistant:"
                },
                {
                    "role": "assistant",
                    "content": f"GPT4 Assistant:{question[1]}<|end_of_turn|>"
                },
                {
                    "role": "user",
                    "content": f"Context:{context} GPT4 User:{question[2]}<|end_of_turn|>GPT4 Assistant:"
                }
            ]
    else:
        if len(question) == 1:
            messages=[
                {"role": "system", "content": "You are Aigro, an automatic assistant. You represent the Agrochem company. Answer me briefly. <|end_of_turn|>"},
                {
                    "role": "user",
                    "content": f"GPT4 User:{question[0]}<|end_of_turn|>GPT4 Assistant:"
                }
            ]
        else:
            messages=[
                {"role": "system", "content": "You are Aigro, an automatic assistant. You represent the Agrochem company. Answer me briefly. <|end_of_turn|>"},
                {
                    "role": "user",
                    "content": f"GPT4 User:{question[0]}<|end_of_turn|>GPT4 Assistant:"
                },
                {
                    "role": "assistant",
                    "content": f"GPT4 Assistant:{question[1]}<|end_of_turn|>"
                },
                {
                    "role": "user",
                    "content": f"GPT4 User:{question[2]}<|end_of_turn|>GPT4 Assistant:"
                }
            ]
    answer = model.create_chat_completion(temperature=0.25, top_p=0.8, top_k=30, messages=messages)
    return answer["choices"][0]["message"]["content"]



