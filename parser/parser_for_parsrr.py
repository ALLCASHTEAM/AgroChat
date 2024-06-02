import os
import re


def clean_text(text):
    # Регулярное выражение для поиска всех вариантов тегов <em> и </em>
    em_pattern = re.compile(r"<\s*/?\s*em\s*/?\s*>", re.IGNORECASE)
    text = re.sub(em_pattern, '', text)

    # Удаление строк "Нет информации", ["Нет информации"] и []
    no_info_patterns = [
        r"\bНет информации\b",  # Нет информации
        r"\[\s*Нет информации\s*\]",  # ["Нет информации"]
        r"\[\s*\]"  # []
        r'\[""\]',  # [""]
        r'\["\s*"\]'  # [" "]
        r'\u00A0'
    ]

    for pattern in no_info_patterns:
        text = re.sub(pattern, '', text)

    return text


def process_files_in_folder(folder_path):
    if not os.path.exists(folder_path):
        print(f"Directory does not exist: {folder_path}")
        return

    if not os.path.isdir(folder_path):
        print(f"Path is not a directory: {folder_path}")
        return

    found_files = False
    for root, dirs, files in os.walk(folder_path):
        print(f"Processing directory: {root}")  # Сообщение о текущей директории
        for file in files:
            if file.endswith(".txt"):
                found_files = True
                file_path = os.path.join(root, file)
                print(f"Processing file: {file_path}")  # Сообщение об обрабатываемом файле
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                cleaned_content = clean_text(content)

                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(cleaned_content)

    if not found_files:
        print("No .txt files found in the specified directory.")


# Укажите путь к вашей папке 'parser'
folder_path = r"C:\Users\ignit\OneDrive\Документы\GitHub\AgroChat\parser\downloaded_images"
process_files_in_folder(folder_path)