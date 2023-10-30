import os

def hash_creator():
    # Путь к рофликам
    project_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    rofls_directory = os.path.join(project_directory, "rofls")

    # проверка правильно ли определился путь(ну на всякий)
    print(rofls_directory)


    # Создание пустого словаря
    prods_tab= {}

    # Получение списка файлов в папке "rofls"
    files_in_rofls = os.listdir(rofls_directory)

    for file_name in files_in_rofls:
        file_path = os.path.join(rofls_directory, file_name)
        if os.path.isfile(file_path):
            # Чтение содержания файла построчно
            with open(file_path, 'r', encoding='utf-8') as file:
                lines = file.readlines()
                # Каждая строка файла становится элементом в списке значений словаря
                prods_tab[file_name] = lines

    return prods_tab

