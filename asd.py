from transformers import AutoTokenizer
from auto_gptq import AutoGPTQForCausalLM


model_name = 'fffrrt/ruGPT-3.5-13B-GPTQ'
model_basename = 'gptq_model-4bit-128g'

tokenizer = AutoTokenizer.from_pretrained(model_name, use_fast=True)
model = AutoGPTQForCausalLM.from_quantized(model_name,
        model_basename = model_basename,
        use_safetensors=True,
        trust_remote_code=True,
        device="cuda:0",
        use_triton=False,
        quantize_config=None)
user_context = "Название товара: Биостим Свекл, Биостим Свекл это специализированное, листовое, комплексное удобрение-биостимулятор для сахарной, столовой свеклы. Для поддержания баланса питательных веществ в период вегетации, защиты от воздействия абиотических стрессов, восстановления продуктивности после действия стрессов, повышения устойчивости к болезням, улучшения количественных и качественных параметров урожая.Тип Биостим Свекл: аминокислоты, полисахариды, макро- и микроэлементы Жидкое аминокислотное удобрение-биостимулятор для листовых подкормок сахарной свеклы, Достоинства Биостим Свекл перед другими удобрениями: Удобрение-биостимулятор с микроэлементами для сахарной, столовой свеклы Стимулирует обмен веществ в растениях, Поддерживает баланс питательных веществ в период вегетации, Защищает от воздействия абиотических стрессов, Восстанавливает продуктивность культур после действия стресс-факторов, Повышает устойчивость растений к болезням, Улучшает количественные и качественные параметры урожая"

text = f"Зная что {user_context} то на вопрос Что такое Биостим Свекл можно ответить что это"

encoded_input = tokenizer(text, return_tensors='pt').to('cuda:0')
output = model.generate(
    **encoded_input,
    num_beams=4,
    max_new_tokens=160,
    no_repeat_ngram_size=2,
    # num_return_sequences=5,
    # do_sample=True
)

print(tokenizer.decode(output[0], skip_special_tokens=True))