import os
import re
from collections import defaultdict
import json
# Задайте путь к вашей папке
folder_path = './'

# Получите список всех файлов и папок в директории
files_and_folders = os.listdir(folder_path)

# Отфильтруйте все, что является файлом
files = [f for f in files_and_folders if os.path.isfile(os.path.join(folder_path, f))]

# Путь к файлам
file_paths = files[1:]
file_paths.pop(1)


# Функция для чтения и предобработки текста из файла
def preprocess_text(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
        # Разделяем текст на пары вопрос-ответ
        qna_pairs = text.split('\n')
        # Удаляем лишние пробелы и разделяем вопросы и ответы
        qna_pairs = [re.split(r'\s*\|\s*', pair) for pair in qna_pairs if pair.strip() != '']
        # Нормализуем текст (приведение к нижнему регистру, удаление пунктуации)
        qna_pairs = [(re.sub(r'[^\w\s]', '', q.lower()), re.sub(r'[^\w\s]', '', a.lower())) for q, a in qna_pairs]
        return qna_pairs


# Индекс для хранения ключевых слов и связанных с ними файлов и позиций вопросов
index = defaultdict(list)

# Процесс предобработки и индексации для одного файла
for file_path in file_paths:
    # Получаем название продукта из имени файла
    product_name = os.path.splitext(os.path.basename(file_path))[0]
    # Предобработка текста файла
    qna_pairs = preprocess_text(file_path)

    # Индексация: добавляем позиции вопросов в индекс по ключевым словам
    for i, (question, _) in enumerate(qna_pairs):
        # Разбиваем вопрос на слова
        words = question.split()
        # Для каждого слова добавляем в индекс название файла и позицию вопроса
        for word in words:
            index[word].append((product_name, i))

# Проверим результат для первых 10 элементов индекса



# Конвертируем defaultdict в обычный словарь для сериализации
index_dict = {word: entries for word, entries in index.items()}

# Путь для сохранения индекса в формате JSON
index_json_path = '../AI_PRO_MAX/index.json'

# Сохраняем индекс в JSON файл
with open(index_json_path, 'w', encoding='utf-8') as f_json:
    json.dump(index_dict, f_json, ensure_ascii=False, indent=4)