from transformers import PreTrainedTokenizerFast, AutoTokenizer
from auto_gptq import AutoGPTQForCausalLM

# Задаем составные названия
composite_names = ["Биостим Свекл", "Другое Составное Название"]

# Загружаем токенизатор
tokenizer = AutoTokenizer.from_pretrained('fffrrt/ruGPT-3.5-13B-GPTQ')

# Добавляем составные названия в словарь токенизатора
tokenizer.add_tokens(composite_names, special_tokens=True)

# Загружаем квантованную модель
model_name = 'fffrrt/ruGPT-3.5-13B-GPTQ'
model_basename = 'gptq_model-4bit-128g'
model = AutoGPTQForCausalLM.from_quantized(model_name, model_basename=model_basename, use_safetensors=True, trust_remote_code=True, device="cuda:0", use_triton=False, quantize_config=None)

# Функция для получения ответа на вопрос
def get_answer(question, context):
    prompt = f"Вопрос: {question} Контекст: {context} Ответ:"
    encoded_input = tokenizer(prompt, return_tensors='pt', padding=True).to('cuda:0')
    output = model.generate(**encoded_input, num_beams=4, max_new_tokens=40, no_repeat_ngram_size=2)
    answer = tokenizer.decode(output[0], skip_special_tokens=True).replace(prompt, "").strip()
    return answer

# Простой цикл для демонстрации работы системы
while True:
    user_question = input("Задайте вопрос ('exit' для выхода): ")
    if user_question.lower() == "exit":
        break
    else:
        user_context = "Название товара: Биостим Свекл, Тип Биостим Свекл: аминокислоты, полисахариды, макро- и микроэлементы Жидкое аминокислотное удобрение-биостимулятор для листовых подкормок сахарной свеклы, Достоинства Биостим Свекл перед другими удобрениями: Удобрение-биостимулятор с микроэлементами для сахарной, столовой свеклы Стимулирует обмен веществ в растениях, Поддерживает баланс питательных веществ в период вегетации, Защищает от воздействия абиотических стрессов, Восстанавливает продуктивность культур после действия стресс-факторов, Повышает устойчивость растений к болезням, Улучшает количественные и качественные параметры урожая"
        answer = get_answer(user_question, user_context)
        print(f"Ответ: {answer}")
