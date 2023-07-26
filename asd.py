from transformers import AutoTokenizer, PreTrainedTokenizerFast
from auto_gptq import AutoGPTQForCausalLM
import torch
import datetime

# Задаем составные названия
composite_names = ["Биостим Свекл", "Другое Составное Название"]

model_name = 'fffrrt/ruGPT-3.5-13B-GPTQ'
model_basename = 'gptq_model-4bit-128g'
tokenizer = AutoTokenizer.from_pretrained(model_name, use_fast=True)

model = AutoGPTQForCausalLM.from_quantized(model_name, model_basename=model_basename, use_safetensors=True, trust_remote_code=True, device="cuda:0", use_triton=False, quantize_config=None)

context = "Название товара: БиостимСвекл, БиостимСвекл это специализированное, листовое, комплексное удобрение-биостимулятор для сахарной, столовой свеклы. Для поддержания баланса питательных веществ в период вегетации, защиты от воздействия абиотических стрессов, восстановления продуктивности после действия стрессов, повышения устойчивости к болезням, улучшения количественных и качественных параметров урожая.Тип БиостимСвекл: полисахариды, макро- и микроэлементы Жидкое аминокислотное удобрение-биостимулятор для листовых подкормок сахарной свеклы, Достоинства Биостим Свекл перед другими удобрениями: Удобрение-биостимулятор с микроэлементами для сахарной, столовой свеклы Стимулирует обмен веществ в растениях, Поддерживает баланс питательных веществ в период вегетации, Защищает от воздействия абиотических стрессов, Восстанавливает продуктивность культур после действия стресс-факторов, Повышает устойчивость растений к болезням, Улучшает количественные и качественные параметры урожая"

# Ваш вопрос
user_question = "Что такое БиостимСвекл?"

# Формируем полный запрос, включая контекст и вопрос
prompt = f"{context}\nВопрос: {user_question}"

# Токенизируем запрос
input_ids = tokenizer.encode(prompt, return_tensors="pt")

# Генерируем ответы от модели
with torch.no_grad():
    output = model.generate(input_ids=input_ids, max_length=200, num_beams=4, pad_token_id=tokenizer.eos_token_id)

# Декодируем токены в текстовый ответ
answer = tokenizer.decode(output[0], skip_special_tokens=True)

# Выводим ответ
print(f"Ответ: {answer}")