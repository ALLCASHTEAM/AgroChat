from llama_cpp import Llama
import torch

def interact():
    model = Llama(
        model_path='./AI_PRO_MAX/model-q16_0.gguf',
        n_ctx=8192,
        n_gpu_layers=35,
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

    return answer["choices"][0]["message"]["content"]



