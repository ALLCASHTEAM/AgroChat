from transformers import AutoTokenizer
from auto_gptq import AutoGPTQForCausalLM


model_name = 'fffrrt/ruGPT-3.5-13B-GPTQ'
model_basename = 'gptq_model-4bit-128g'

tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoGPTQForCausalLM.from_quantized(model_name,
        model_basename = model_basename,
        use_safetensors=True,
        trust_remote_code=True,
        device="cuda:0",
        use_triton=False,
        quantize_config=None)

text = "Чтобы подружиться с осьминогом, нужно: \n1."

encoded_input = tokenizer(text, return_tensors='pt').to('cuda:0')
output = model.generate(
    **encoded_input,
    num_beams=8,
    max_new_tokens=200,
    no_repeat_ngram_size=2,
    num_return_sequences=5,
    do_sample=True
)

print(tokenizer.decode(output[0], skip_special_tokens=True))