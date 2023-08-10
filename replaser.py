import os

# Укажите путь к папке, содержащей текстовые файлы
folder_path = 'AgroChat/rofls'


def remove_quotes_and_commas(text):
    # Убрать кавычки и запятые из текста
    text = text.replace('"', '').replace(',', '')
    return text


def process_files_in_folder(folder_path):
    for filename in os.listdir(folder_path):
        if filename.endswith('.txt'):
            file_path = os.path.join(folder_path, filename)
            with open(file_path, 'r') as file:
                content = file.read()

            processed_content = remove_quotes_and_commas(content)

            # Перезаписать файл с обработанным содержимым
            with open(file_path, 'w') as file:
                file.write(processed_content)

            print(f'Файл {filename} обработан.')


# Вызвать функцию для обработки файлов в указанной папке
process_files_in_folder(folder_path)