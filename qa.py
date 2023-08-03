from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
import torch
model_name = "ai-forever/FRED-T5-1.7B"  # Используем базовую модель T5, вы можете заменить ее на любую другую модель T5

# Загрузка модели и токенизатора
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name,eos_token='</s>')

with open('boosters.txt', 'r', encoding='utf-8') as f:
    context = f.read().replace(',', '').replace(';', '. ').replace('..', '.')
# Задайте вопрос и контекст
question = "Чем мне удобрять кукурузу?"

print(context)
# T5 ожидает, что задача будет указана во входном тексте, в формате "task: input"
input_text = f"вопрос: {question}  контекст: {context}"

# Токенизируем входной текст
inputs = tokenizer.encode(input_text, return_tensors='pt')

# Получаем ответ от модели
input_ids=torch.tensor([tokenizer.encode(input_text)])
outputs = model.generate(input_ids, eos_token_id=tokenizer.eos_token_id, early_stopping=True, max_length=4096)

# Декодируем ответ
answer = tokenizer.decode(outputs[0][1:])

print(answer)
