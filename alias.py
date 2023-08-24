import os

folder_path = "rofls"
files_without_question = []
fileses=0
# Перебираем все файлы в папке
for filename in os.listdir(folder_path):
    if filename.endswith(".txt"):  # Предполагаем, что это текстовые файлы
        file_path = os.path.join(folder_path, filename)
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            if "Вопрос:" not in content:
                fileses=fileses + 1
                files_without_question.append(filename)

print("Файлы без строки 'Вопрос:' в содержимом:")
for filename in files_without_question:
    print(filename)
print(fileses)
