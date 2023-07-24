from transformers import AutoTokenizer
from auto_gptq import AutoGPTQForCausalLM
import datetime
# Загрузка предварительно квантованной модели и токенизатора
model_name = 'fffrrt/ruGPT-3.5-13B-GPTQ'
model_basename = 'gptq_model-4bit-128g'
tokenizer = AutoTokenizer.from_pretrained(model_name, use_fast=True)
model = AutoGPTQForCausalLM.from_quantized(model_name, model_basename=model_basename, use_safetensors=True, trust_remote_code=True, device="cuda:0", use_triton=False, quantize_config=None)

# Функция для получения ответа на вопрос
def get_answer(question, context):
    # Сочетаем вопрос с контекстом для формирования подсказки
    prompt = f"Вопрос: {question} Контекст: {context} Ответ:"
    # Преобразование текста в кодированные тензоры
    encoded_input = tokenizer(prompt, return_tensors='pt', padding=True).to('cuda:0')
    # Генерация ответа с помощью модели
    output = model.generate(**encoded_input, num_beams=4, max_new_tokens=160, no_repeat_ngram_size=2)
    # Раскодирование и печать ответа
    answer = tokenizer.decode(output[0], skip_special_tokens=True).replace(prompt, "").strip()
    return answer

# Простой цикл для демонстрации работы системы
while True:
    user_question = input("Задайте вопрос ('exit' для выхода): ")
    if user_question.lower() == "exit":
        break
    else:
        #user_context = input("Введите контекст для поиска ответа на вопрос: ")
        user_context = "Название товара: Биостим_Свекл,Тип: аминокислоты, полисахариды, макро- и микроэлементы Жидкое аминокислотное удобрение-биостимулятор для листовых подкормок сахарной свеклы, Достоинства: Удобрение-биостимулятор с микроэлементами для сахарной, столовой свеклыСтимулирует обмен веществ в растенияхПоддерживает баланс питательных веществ в период вегетацииЗащищает от воздействия абиотических стрессов Восстанавливает продуктивность культур после действия стресс-факторовПовышает устойчивость растений к болезнямУлучшает количественные и качественные параметры урожая"
        answer = get_answer(user_question, user_context)
        print(f"Ответ: {answer}")