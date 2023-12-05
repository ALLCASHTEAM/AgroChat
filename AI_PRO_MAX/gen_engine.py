import logging
from llama_cpp import Llama

logging.basicConfig(level=logging.INFO, filename="gen_log.log", filemode="w")

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
    system_message = "You are Aigro, an automatic assistant who speaks Russian. Always answer questions in Russian. You represent the Agrochem company. Do not translate the product names. Use only those products names that are in the context."
    return get_message_tokens(model.tokenize, model.token_eos, system_message)


def interact():
    model = Llama(
        model_path='./AI_PRO_MAX/model-q8_0.gguf',
        n_ctx=8192,
        n_gpu_layers=35,
    )
    tokens = get_system_tokens(model)
    model.eval(tokens)
    return model, tokens


def generate(question: str, tokens, model, context=False):
    user_message = f"Context:{context} GPT4 User:{question}GPT4 Assistant:" if context else f"GPT4 User:{question}GPT4 Assistant:"
    tokens += get_message_tokens(model.tokenize, model.token_eos, user_message)
    generator = model.generate(tokens, top_k=30, top_p=0.9, temp=0.2, repeat_penalty=1.1)

    try:
        return accumulate_tokens(generator, model)
    except Exception as e:
        logging.error(e)
        print(f"ERROR!. Ошибка в генераторе. Очистка контекста и новая попытка.")
        tokens = get_message_tokens(model.tokenize, model.token_eos, user_message)
        generator = model.generate(tokens, top_k=30, top_p=0.9, temp=0.2, repeat_penalty=1.1)
        return accumulate_tokens(generator, model)


if __name__ == '__main__':
    model, tokens = interact()
    question = "Your question here"
    answer, _ = generate(question, tokens, model)
    print(answer)
