from transformers import T5ForConditionalGeneration, GPT2Tokenizer
from torch import device

def load_interpreter(model_name='Den4ikAI/FRED-T5-Large-interpreter'):
    model_name = 'Den4ikAI/FRED-T5-Large-interpreter'
    tokenizer = GPT2Tokenizer.from_pretrained(model_name, )
    model = T5ForConditionalGeneration.from_pretrained(model_name)
    model.to('cuda')  # cpu-cuda
    model.eval()
    return model, tokenizer


def load_data():
    with open('tmp.txt', 'r', encoding='utf-8') as f:
        line = f.readlines()
    line[-1] = line[-1] + '\n'
    line = '-'.join(line)
    return line


# sex = "-чем полить кукурузу?\n-Биостим кукуруза подойдет для полива кукурузы\n-сколько он стоит?"

def generate_intr(model, tokenizer, message_text: str):
    t5_input = f'<SC1> {message_text}\n Развернутый ответ:<extra_id_0>#'
    input_ids = tokenizer(t5_input, return_tensors='pt').input_ids.to('cuda')  # cpu-cuda
    out_ids = model.generate(input_ids=input_ids, max_length=40, eos_token_id=tokenizer.eos_token_id,
                             early_stopping=True)
    t5_output = tokenizer.decode(out_ids[0][1:])
    return t5_output


def interpritator_with_history(dialog):
    text = load_data() + f"-{dialog.lower()}"
    model, tokenizer = load_interpreter()
    result = generate_intr(model, tokenizer, text)
    print('Текст', text, '\n Вывод: ', result)
    return result
