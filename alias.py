# Открываем файл на чтение
with open('Биостим Кукуруза.txt', 'r', encoding='utf-8') as file:
    # Читаем содержимое файла
    lines = file.readlines()

# Открываем файл для записи с замененными строками
with open('Биостим Кукуруза1.txt', 'w', encoding='utf-8') as output_file:
    for line in lines:
        # Заменяем "Ответ:" на пустую строку и записываем в новый файл
        modified_line = line.replace('Ответ:', '')
        output_file.write(modified_line)