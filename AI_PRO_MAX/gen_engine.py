import logging
from llama_cpp import Llama
import torch
logging.basicConfig(level=logging.INFO, filename="gen_log.log", filemode="w")
print(torch.cuda.is_available())
def accumulate_tokens(generator, model):
    answer = ''
    tokens = []
    for token in generator:
        answer += model.detokenize([token]).decode("utf-8", errors="ignore")
        tokens.append(token)
        if token == model.token_eos():
            break
    return answer, tokens


def get_message_tokens(tokenize_func, token_eos_func, content: str):
    message_tokens = tokenize_func(content.encode("utf-8"))
    message_tokens.append(token_eos_func())
    return message_tokens


def get_system_tokens(model):
    system_message = "System Promt: You are Aigro, an automatic assistant. You represent the Агрохим company.<|end_of_turn|>"
    return get_message_tokens(model.tokenize, model.token_eos, system_message)


def interact():
    model = Llama(
        model_path='./AI_PRO_MAX/model-q8_0.gguf',
        n_ctx=8192,
	n_threads=8,
        n_gpu_layers=-1,
    )
    tokens = get_system_tokens(model)
    model.eval(tokens)
    return model, tokens


def generate(question: str, tokens, model, context=False):
    user_message = f"GPT4 Correct Context:{context} <|end_of_turn|>GPT4 Correct User:{question}<|end_of_turn|>GPT4 Correct Assistant:" if context else f"GPT4 Correct User:{question}<|end_of_turn|>GPT4 Correct Assistant:"
    tokens += get_message_tokens(model.tokenize, model.token_eos, user_message)
    generator = model.generate(tokens)

    
    #    return accumulate_tokens(generator, model)
    # Exception as e:

   # logging.error(e)
   # print(f"ERROR!. Ошибка в генераторе. Очистка контекста и новая попытка.")
   # tokens = get_message_tokens(model.tokenize, model.token_eos, user_message)
   # generator = model.generate(token)
    return accumulate_tokens(generator, model)


if __name__ == '__main__':
    model, tokens = interact()
    question = "Your question here"
    answer, _ = generate(question, tokens, model)
    print(answer)
