import os

folder_path = './rofls'  # Путь к нашей папке

# Получаем список файлов в папке "rofls"
files = os.listdir(folder_path)

# Проходим по каждому файлу в папке
for filename in files:
    file_path = os.path.join(folder_path, filename)

    # Проверяем, что это текстовый файл
    if filename.endswith('.txt'):
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()

        # Создаем новый список для измененных строк
        new_lines = []

        # Применяем замены и обработку для каждой строки
        for line in lines:
            if 'Вопрос:' in line or 'Ответ:' in line:
                line = line.replace('"', '').replace('Эко Плюс ', '').replace('Эко плюс', '').replace('Новинка ', '').replace('Эко Плюс', '').replace('Новинка', '')
            new_lines.append(line)

        # Записываем измененные строки обратно в тот же файл
        with open(file_path, 'w', encoding='utf-8') as file:
            file.writelines(new_lines)
