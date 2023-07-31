import os
from transformers import GPT2Tokenizer, GPT2LMHeadModel
import torch

os.environ['PYTORCH_CUDA_ALLOC_CONF'] = '0'
torch.cuda.set_memory_allocated(torch.cuda.memory_allocated())
torch.cuda.set_memory_cached(torch.cuda.memory_cached())

tokenizer = GPT2Tokenizer.from_pretrained("ai-forever/ruGPT-3.5-13B")
model = GPT2LMHeadModel.from_pretrained("ai-forever/ruGPT-3.5-13B")
model.half()
model.to('cuda')

def IdentProd(text):
    file_path = './boosters.txt'

    with open(file_path, 'r') as file:
        content = file.read()

    promt = "Представим что ты агроном-продавецконсультант, вот так выглядит твой каталог: "+content+"а покупатель спрашивает это: "+text+" "#cюда еще добавлять диалог этот, например из 20 сообщений предидущих и тогда заебися будет пахнуть наша пися
    encoded_input = tokenizer(promt, return_tensors='pt', add_special_tokens=False).to('cuda')
    output = model.generate(
        **encoded_input,
        num_beams=2,
        do_sample=True,
        max_new_tokens=60
        )

    print(tokenizer.decode(output[0], skip_special_tokens=True))

IdentProd("Чем мне удобрить кукурузу")