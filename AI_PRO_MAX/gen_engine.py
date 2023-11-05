import fire
from llama_cpp import Llama

SYSTEM_PROMPT = "You are an Aigro, a Russian—speaking automatic assistant. Always answer in Russian. You're company is AgroHim. Don't translate product names."
SYSTEM_TOKEN = 1788
USER_TOKEN = 1404
BOT_TOKEN = 9225
LINEBREAK_TOKEN = 13

ROLE_TOKENS = {
    "user": USER_TOKEN,
    "bot": BOT_TOKEN,
    "system": SYSTEM_TOKEN
}
model_path = './AI_PRO_MAX/model-q8_0.gguf'
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


def interact():
    model = Llama(
        model_path=model_path,
        n_ctx=2000,
        n_parts=1,
    )

    system_tokens = get_system_tokens(model)
    tokens = system_tokens
    model.eval(tokens)
    return model, tokens


def generate(question, tokens, model, context=False):
    print(question, context)
    while True:
        if context:
            user_message = f"User: Context{context} Question:{question}"
        else:
            print(question)
            user_message = f"User: Question:{question}"
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
