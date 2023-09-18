import fire

from llama_cpp import Llama

SYSTEM_PROMPT = "You are an Agrochat, a Russian—speaking automatic assistant. You talk to people and help them. You're name is Agrochat."
SYSTEM_TOKEN = 1788
USER_TOKEN = 1404
BOT_TOKEN = 9225
LINEBREAK_TOKEN = 13

ROLE_TOKENS = {
    "user": USER_TOKEN,
    "bot": BOT_TOKEN,
    "system": SYSTEM_TOKEN
}

top_k = 30
top_p = 0.9
temperature = 0.2
repeat_penalty = 1.1

def get_message_tokens(model, role, content):
    message_tokens = model.tokenize(content.encode("utf-8"))
    message_tokens.insert(1, ROLE_TOKENS[role])
    message_tokens.insert(2, LINEBREAK_TOKEN)
    message_tokens.append(model.token_eos())
    return message_tokens


def get_system_tokens(model):
    system_message = {
        "role": "system",
        "content": SYSTEM_PROMPT
    }
    return get_message_tokens(model, **system_message)


def interact(
        model_path='./model-q8_0.gguf',
        n_ctx=2000,
        top_k=30,
        top_p=0.9,
        temperature=0.2,
        repeat_penalty=1.1,

):
    model = Llama(
        model_path=model_path,
        n_ctx=n_ctx,
        n_parts=1,
    )

    system_tokens = get_system_tokens(model)
    tokens = system_tokens
    model.eval(tokens)
    return model, tokens

def generate(question, tokens, model, context=False):

    if context:
        user_message = f"User: Context{context} Question:{question}"
    else:
        user_message = f"User: {question}"
    message_tokens = get_message_tokens(model=model, role="user", content=user_message)
    role_tokens = [model.token_bos(), BOT_TOKEN, LINEBREAK_TOKEN]
    tokens += message_tokens + role_tokens
    generator = model.generate(
        tokens,
        top_k=top_k,
        top_p=top_p,
        temp=temperature,
        repeat_penalty=repeat_penalty
    )
    for token in generator:
        token_str = model.detokenize([token]).decode("utf-8", errors="ignore")
        tokens.append(token)
        if token == model.token_eos():
            break
        print(token_str, end="", flush=True)
    print()


if __name__ == "__main__":
    model, tokens = interact()
    fire.Fire(generate(input("Question"), tokens, model))
