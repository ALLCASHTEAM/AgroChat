from transformers import T5ForConditionalGeneration, GPT2Tokenizer

tokenizer = GPT2Tokenizer.from_pretrained('Den4ikAI/FRED-T5-XL-interpreter', )
model = T5ForConditionalGeneration.from_pretrained('Den4ikAI/FRED-T5-XL-interpreter') # cpu-cuda
model.eval()


def load_data() -> str:
    with open('tmp.txt', 'r', encoding='utf-8') as f:
        line = f.readlines()
    line[-1] = line[-1] + '\n'
    line = '-'.join(line)
    return line


def generate_intr(model, tokenizer, message_text: str) -> str:
    t5_input = f'<SC1> {message_text}\n Развернутый ответ:<extra_id_0>#'
    input_ids = tokenizer(t5_input, return_tensors='pt').input_ids  # cpu-cuda
    out_ids = model.generate(input_ids=input_ids, max_length=40, eos_token_id=tokenizer.eos_token_id,
                             early_stopping=True)
    t5_output = tokenizer.decode(out_ids[0][1:])
    return t5_output


def interpritator_with_history(dialog: str) -> str:
    text = load_data() + f"-{dialog.lower()}"
    result = generate_intr(model, tokenizer, text)
    return result


if __name__ == '__main__':
    sex = "-чем полить кукурузу?\n-Биостим кукуруза подойдет для полива кукурузы\n-сколько он стоит?"
    print(interpritator_with_history(sex))
