import fire
from llama_cpp import Llama

BOT_TOKEN = 12435
LINEBREAK_TOKEN = 13

ROLE_TOKENS = {
    "user": 2188,
    "bot": 12435,
    "system": 1587
}


def get_message_tokens(model, role, content):
    message_tokens = model.tokenize(content.encode("utf-8"))
    message_tokens.insert(1, ROLE_TOKENS[role])
    message_tokens.insert(2, LINEBREAK_TOKEN)
    message_tokens.append(model.token_eos())
    return message_tokens


def get_system_tokens(model):
    system_message = {
        "role": "system",
        "content": "You are Aigro, an automatic assistant who speaks Russian. Always answer questions in Russian. You represent the Agrochem company. Do not translate the product names. Recommend products based on customer requests."
    }
    return get_message_tokens(model, **system_message)


def interact():
    model = Llama(
        model_path='./AI_PRO_MAX/model-q8_0.gguf',
        n_ctx=2000,
        n_parts=1,
    )

    tokens = get_system_tokens(model)
    model.eval(tokens)
    return model, tokens


def generate(question, tokens, model, context=False):
    if context:
        user_message = f"User: Context{context} Question:{question}"
    else:
        print(question)
        user_message = f"User: Question:{question}"
    tokens += get_message_tokens(model=model, role="user", content=user_message) + [model.token_bos(), BOT_TOKEN, LINEBREAK_TOKEN]
    generator = model.generate(
        tokens,
        top_k=30,
        top_p=0.9,
        temp=0.2,
        repeat_penalty=1.1
    )
    answer = ''
    for token in generator:
        token_str = model.detokenize([token]).decode("utf-8", errors="ignore")
        answer += token_str
        if token == model.token_eos():
            break
        tokens.append(token)
    return answer


if __name__ == "__main__":
    model, tokens = interact()
    fire.Fire(generate(input("Question"), tokens, model))
