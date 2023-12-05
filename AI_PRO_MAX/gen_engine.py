from llama_cpp import Llama


def generator_func(generator, model, tokens, answer=''):
    for token in generator:
        answer += model.detokenize([token]).decode("utf-8", errors="ignore")
        if token == model.token_eos():
            break
        tokens.append(token)
    return answer, tokens


def get_message_tokens(model, content: str):
    message_tokens = model.tokenize(content.encode("utf-8"))
    message_tokens.append(model.token_eos())
    return message_tokens


def get_system_tokens(model):
    system_message = {
        "content": "You are Aigro, an automatic assistant who speaks Russian. Always answer questions in Russian. You represent the Agrochem company. Do not translate the product names. Use only those products names that are in the context."
    }
    return get_message_tokens(model, **system_message)


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
    if context:
        user_message = f"Context:{context} GPT4 User:{question}<|end_of_turn|>GPT4 Assistant:"
    else:
        user_message = f"GPT4 User:{question}<|end_of_turn|>GPT4 Assistant:"
    tokens += get_message_tokens(model=model, content=user_message)
    generator = model.generate(
        tokens,
        top_k=30,
        top_p=0.9,
        temp=0.2,
        repeat_penalty=1.1
    )

    try:
        answer, tokens = generator_func(generator, model, tokens)
        return answer
    except:
        print("Очистка контекста")
        tokens = get_message_tokens(model=model, content=user_message)
        generator = model.generate(
            tokens,
            top_k=30,
            top_p=0.9,
            temp=0.2,
            repeat_penalty=1.1
        )
        answer, tokens = generator_func(generator, model, tokens)
        return answer
