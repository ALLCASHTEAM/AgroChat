import pandas
import lzma
import _lzma
from transformers import AutoTokenizer, TextGenerationPipeline
from auto_gptq import AutoGPTQForCausalLM, BaseQuantizeConfig


repo_name = "gurgutan/ruGPT-13B-4bit"
# load tokenizer from Hugging Face Hub
tokenizer = AutoTokenizer.from_pretrained(repo_name, use_fast=True)
# download quantized model from Hugging Face Hub and load to the first GPU
model = AutoGPTQForCausalLM.from_quantized(repo_name, device="cuda:0", use_safetensors=True, use_triton=False)
# inference with model.generate
request = "AMD лучше NVIDEA так как"
print(tokenizer.decode(model.generate(**tokenizer(request, return_tensors="pt").to(model.device),max_length=1000 )[0]))
# or you can also use pipeline
pipeline = TextGenerationPipeline(model=model, tokenizer=tokenizer)
print(pipeline(request)[0]["generated_text"])