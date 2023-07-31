
from transformers import AutoTokenizer, AutoModelForCausalLM

tokenizerr = AutoTokenizer.from_pretrained("ai-forever/ruGPT-3.5-13B")
model = AutoModelForCausalLM.from_pretrained("ai-forever/ruGPT-3.5-13B")
model.to('cuda:0')
model.half()

def IdentProd(text):
    file_path = './boosters.txt'

    with open(file_path, 'r') as file:
        content = file.read()

    promt = "Представим что ты агроном-продавецконсультант, вот так выглядит твой каталог: "+content+"а покупатель спрашивает это: "+text+" "#cюда еще добавлять диалог этот, например из 20 сообщений предидущих и тогда заебися будет пахнуть наша пися
    tokenizer = tokenizerr(promt, return_tensors='pt', add_special_tokens=False).to('cuda:0')
    encoded_input = tokenizerr(promt, return_tensors='pt').to('cuda:0')
    output = model.generate(
        **encoded_input,
        max_split_size_mb=11264,
        num_beams=4,
        do_sample=True,
        max_new_tokens=60
        )

    print(tokenizer.decode(output[0], skip_special_tokens=True))

IdentProd("Чем мне удобрить кукурузу")