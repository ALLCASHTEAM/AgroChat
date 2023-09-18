from transformers import T5ForConditionalGeneration, GPT2Tokenizer


def load_interpreter(model_name='Den4ikAI/FRED-T5-Large-interpreter'):
    model_name = 'Den4ikAI/FRED-T5-Large-interpreter'
    tokenizer = GPT2Tokenizer.from_pretrained(model_name, )
    model = T5ForConditionalGeneration.from_pretrained(model_name)
    model.to('cpu')#cpu-cuda
    model.eval()
    return model, tokenizer

#sex = "-чем полить кукурузу?\n-Биостим кукуруза подойдет для полива кукурузы\n-сколько он стоит?"

def generate_intr(model, tokenizer, message_text: str):
    t5_input = f'<SC1> {message_text}\n Развернутый ответ:<extra_id_0>#'
    input_ids = tokenizer(t5_input, return_tensors='pt').input_ids.to('cpu')#cpu-cuda
    out_ids = model.generate(input_ids=input_ids, max_length=40, eos_token_id=tokenizer.eos_token_id,
                             early_stopping=True)
    t5_output = tokenizer.decode(out_ids[0][1:])
    return t5_output


def interpritator_with_history(dialog):
    text = dialog.lower()
    model, tokenizer = load_interpreter()
    result = generate_intr(model, tokenizer, text)
    print('Текст', text ,'\n Вывод: ', result)
    return result

