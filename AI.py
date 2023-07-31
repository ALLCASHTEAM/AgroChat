'''
Модель берты которая по контексту должна отвечать
но так как контекст очень хуевый, нам нечего делать кроме как обосраться
'''
import torch
import numpy as np
from transformers import AutoTokenizer, AutoModelForQuestionAnswering

# Используем токенизатор и модель
tokenizer = AutoTokenizer.from_pretrained("timpal0l/mdeberta-v3-base-squad2")
model = AutoModelForQuestionAnswering.from_pretrained("timpal0l/mdeberta-v3-base-squad2")

# Задаем текст с товарами, разделенными символом ';'
file_path = './boosters.txt'

with open(file_path, 'r', encoding='utf-8') as file:
    content = file.read()
# Ввод вопроса пользователем
question = "Чем мне удобрить кукурузу?"

# Токенизируем вопрос и текст товаров
tokenized = tokenizer.encode_plus(question, content, add_special_tokens=False, return_tensors="pt")

# Получаем токены
tokens = tokenizer.convert_ids_to_tokens(tokenized['input_ids'][0])

# Запускаем модель для получения ответа
outputs = model(**tokenized)

# Получаем позиции начала и конца ответа в токенах
# Получаем позиции начала и конца ответа в токенах
start_index = torch.argmax(outputs.start_logits)
end_index = torch.argmax(outputs.end_logits)

# Получаем текст ответа из токенов
answer = tokenizer.decode(tokenized['input_ids'][0][start_index:end_index + 1], skip_special_tokens=True)

# Разделяем текст на строки товаров
items = content.split(";")

# Функция для поиска ответа в строке товара
def find_answer_in_item(item, question):
    if question.lower() in item.lower():
        return item.strip()
    return None

# Ищем ответ среди строк товаров
found_answer = None
for item in items:
    found_answer = find_answer_in_item(item, question)
    if found_answer:
        break

# Выводим результат
if found_answer:
    print('Вопрос:', question)
    print('Ответ:', found_answer)
else:
    print('Ответ не найден.')
