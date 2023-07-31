from transformers import AutoTokenizer
from auto_gptq import AutoGPTQForCausalLM

model_name = 'fffrrt/ruGPT-3.5-13B-GPTQ'
model_basename = 'fffrrt/gptq_model-4bit-128g'

tokenizer = AutoTokenizer.from_pretrained(model_name, use_fast=True)
model = AutoGPTQForCausalLM.from_quantized(model_name,
                                           model_basename=model_basename,
                                           use_safetensors=True,
                                           trust_remote_code=True,
                                           device="cuda",
                                           use_triton=False,
                                           quantize_config=None)

file_path = './boosters.txt'
with open(file_path, 'r') as file:
        content = file.read()

def IdentProd(text):

    print(content)

    promt = "Представим что ты агроном-продавецконсультант, вот так выглядит твой каталог: "+content+"а покупатель спрашивает это: "+text+" "#cюда еще добавлять диалог этот, например из 20 сообщений предидущих и тогда заебися будет пахнуть наша пися
    encoded_input = tokenizer(promt, return_tensors='pt', max_length=8096).to('cuda')
    output = model.generate(
            **encoded_input,
            num_beams=4,
            no_repeat_ngram_size=2,
            # num_return_sequences=5,
            # do_sample=True
            max_length=8096
        )

    print(tokenizer.decode(output[0], skip_special_tokens=True))
