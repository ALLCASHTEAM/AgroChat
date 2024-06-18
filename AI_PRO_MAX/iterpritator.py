from transformers import T5ForConditionalGeneration, GPT2Tokenizer

tokenizer = GPT2Tokenizer.from_pretrained('Den4ikAI/FRED-T5-Large-interpreter')
model = T5ForConditionalGeneration.from_pretrained('Den4ikAI/FRED-T5-Large-interpreter')


def generate_intr(model, tokenizer, message_text: str) -> str:
    t5_input = f'<SC1> {message_text}\n Развернутый ответ:<extra_id_0>#'
    input_ids = tokenizer(t5_input, return_tensors='pt').input_ids
    out_ids = model.generate(input_ids=input_ids, max_length=40, eos_token_id=tokenizer.eos_token_id,
                             early_stopping=True)
    return tokenizer.decode(out_ids[0][1:])


def interpretator_with_history(dialog: list[str]) -> str:
    text = '-'+("\n- ".join(dialog))
    return generate_intr(model, tokenizer, text)


if __name__ == '__main__':
    dialog = "-чем полить кукурузу?\n-Биостим кукуруза подойдет для полива кукурузы\n-сколько он стоит?"
    print(interpretator_with_history(dialog))

