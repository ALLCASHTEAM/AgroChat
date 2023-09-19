'''import os

# Функция для обработки одного текстового файла и записи результата обратно в файл
def process_and_write_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # Список для хранения пар вопрос-ответ
    qa_pairs = []

    current_question = None
    current_answer = None

    for line in lines:
        line = line.strip()

        if line.startswith('Вопрос: '):
            current_question = line[len('Вопрос: '):]
        elif line.startswith('Ответ: '):
            current_answer = line[len('Ответ: '):]
        else:
            continue

        if current_question and current_answer:
            qa_pairs.append(current_question + ' | ' + current_answer)
            current_question = None
            current_answer = None

    # Записываем результаты обратно в файл
    with open(file_path, 'w', encoding='utf-8') as file:
        for qa_pair in qa_pairs:
            file.write(qa_pair + '\n')

# Директория, в которой находятся текстовые файлы
directory_path = './rofls'

# Список всех файлов в директории
file_list = os.listdir(directory_path)

# Обрабатываем каждый текстовый файл и перезаписываем его
for filename in file_list:
    if filename.endswith('.txt'):
        file_path = os.path.join(directory_path, filename)
        process_and_write_file(file_path)
        print(f"Файл {filename} был обработан и перезаписан.")'''



import os

# Функция для обработки одного текстового файла и удаления "Вопрос:" и "Ответ:"
def process_and_remove_labels(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # Список для хранения обновленных строк
    updated_lines = []

    for line in lines:
        # Удаляем "Вопрос:" и "Ответ:" из строки, если они есть
        line = line.replace('Вопрос:', '').replace('Ответ:', '').strip()
        updated_lines.append(line)

    # Записываем обновленные строки обратно в файл
    with open(file_path, 'w', encoding='utf-8') as file:
        for updated_line in updated_lines:
            file.write(updated_line + '\n')

# Директория, в которой находятся текстовые файлы
directory_path = './rofls'

# Список всех файлов в директории
file_list = os.listdir(directory_path)

# Обрабатываем каждый текстовый файл и удаляем метки
for filename in file_list:
    if filename.endswith('.txt'):
        file_path = os.path.join(directory_path, filename)
        process_and_remove_labels(file_path)
        print(f"Метки удалены из файла {filename}.")
