from transformers import AutoTokenizer, PreTrainedTokenizerFast
from auto_gptq import AutoGPTQForCausalLM
import datetime

# Задаем составные названия
composite_names = ["Биостим Свекл", "Другое Составное Название"]

model_name = 'fffrrt/ruGPT-3.5-13B-GPTQ'
model_basename = 'gptq_model-4bit-128g'
tokenizer = AutoTokenizer.from_pretrained(model_name, use_fast=True)
model = AutoGPTQForCausalLM.from_quantized(model_name, model_basename=model_basename, use_safetensors=True, trust_remote_code=True, device="cuda:0", use_triton=False, quantize_config=None)

def get_answer(question, context):
    prompt = f"Вопрос: {question} Контекст: {context} Ответ:"
    encoded_input = tokenizer(prompt, return_tensors='pt', padding=True).to('cuda:0')
    output = model.generate(**encoded_input, num_beams=4, max_new_tokens=40, no_repeat_ngram_size=2, do_sample=False, temperature= 0.2) ##изначально 4, 160, 2
    answer = tokenizer.decode(output[0], skip_special_tokens=True).replace(prompt, "").strip()
    return answer

'''while True:
    user_question = input("Задайте вопрос ('exit' для выхода): ")
    if user_question.lower() == "exit":
        break
    else:
        user_context = "Название товара: Биостим Свекл, Биостим Свекл это специализированное, листовое, комплексное удобрение-биостимулятор для сахарной, столовой свеклы. Для поддержания баланса питательных веществ в период вегетации, защиты от воздействия абиотических стрессов, восстановления продуктивности после действия стрессов, повышения устойчивости к болезням, улучшения количественных и качественных параметров урожая.Тип Биостим Свекл: аминокислоты, полисахариды, макро- и микроэлементы Жидкое аминокислотное удобрение-биостимулятор для листовых подкормок сахарной свеклы, Достоинства Биостим Свекл перед другими удобрениями: Удобрение-биостимулятор с микроэлементами для сахарной, столовой свеклы Стимулирует обмен веществ в растениях, Поддерживает баланс питательных веществ в период вегетации, Защищает от воздействия абиотических стрессов, Восстанавливает продуктивность культур после действия стресс-факторов, Повышает устойчивость растений к болезням, Улучшает количественные и качественные параметры урожая"
        answer = get_answer(user_question, user_context)
        print(f"Ответ: {answer}")'''
#user_question = input("Задайте вопрос: ")
user_question = "Что такое биостим векл"
user_context = "Название товара: Биостим Свекл, Биостим Свекл это специализированное, листовое, комплексное удобрение-биостимулятор для сахарной, столовой свеклы. Для поддержания баланса питательных веществ в период вегетации, защиты от воздействия абиотических стрессов, восстановления продуктивности после действия стрессов, повышения устойчивости к болезням, улучшения количественных и качественных параметров урожая.Тип Биостим Свекл: полисахариды, макро- и микроэлементы Жидкое аминокислотное удобрение-биостимулятор для листовых подкормок сахарной свеклы, Достоинства Биостим Свекл перед другими удобрениями: Удобрение-биостимулятор с микроэлементами для сахарной, столовой свеклы Стимулирует обмен веществ в растениях, Поддерживает баланс питательных веществ в период вегетации, Защищает от воздействия абиотических стрессов, Восстанавливает продуктивность культур после действия стресс-факторов, Повышает устойчивость растений к болезням, Улучшает количественные и качественные параметры урожая"
answer = get_answer(user_question, user_context)
print(f"Ответ: {answer}")
answer = get_answer(user_question, user_context)
print(f"Ответ: {answer}")
answer = get_answer(user_question, user_context)
print(f"Ответ: {answer}")
answer = get_answer(user_question, user_context)
print(f"Ответ: {answer}")