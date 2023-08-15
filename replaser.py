file_path = 'C:/Users/User/Documents/GitHub/AgroChat/rofls/Азорро, КС.txt'  # Путь к вашему файлу

with open(file_path, 'r', encoding='utf-8') as file:
    lines = file.readlines()

# Применяем замены и обработку для каждой строки
for i in range(len(lines)):
    if 'Вопрос:' in lines[i] or 'Ответ:' in lines[i]:
        lines[i] = lines[i].replace('Вопрос:', '{"question":"H:').replace('\nОтвет:', '\\nB: <extra_id_0>","answer":"<extra_id_0>').replace('"', '/"')
    else:
        lines.pop(i)
with open(file_path, 'w', encoding='utf-8') as file:
    file.writelines(lines)