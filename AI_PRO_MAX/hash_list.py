from pathlib import Path


def hash_creator():
    # Путь к рофликам
    rofls_directory = Path(__file__).resolve().parent.parent / "rofls"

    # Создание словаря, ключи которого - имена файлов, а значения - содержимое файлов
    prods_tab = {
        file.name: file.read_text(encoding='utf-8').splitlines()
        for file in rofls_directory.glob('*')
        if file.is_file()
    }


    return prods_tab

# hachik = hash_creator()
#
# print(hachik['Поларис Кватро, СМЭ.txt'][0])
