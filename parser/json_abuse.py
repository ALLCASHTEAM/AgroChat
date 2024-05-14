import json
import requests
from bs4 import BeautifulSoup

for id in range(1, 1000):
    try:
        url = f"https://plantpad.samlab.cn/api/disease/findById/{id}"

        response = requests.get(url)

        # Проверка успешности запроса
        if response.status_code == 200:
            # Преобразование текста JSON-ответа в объект Python
            data = response.json()

            # Запись объекта в файл в формате JSON
            with open(f'{id}.json', 'w', encoding='utf-8') as file:
                json.dump(data, file, ensure_ascii=False, indent=4)
        else:
            print(f"Запрос не удался. Статус-код: {response.status_code}")

        # Load the JSON file
        with open(f'{id}.json', 'r') as file:
            data = json.load(file)

        # Extracting the required entities
        entities = {
            "definition_types": data["disease_info"].get("definition_types"),
            "structure_mode": data["disease_info"].get("structure_mode"),
            "period_environmental": data["disease_info"].get("period_environmental"),
            "overwintering": data["disease_info"].get("overwintering"),
            "chemical_control": data["disease_info"].get("chemical_control"),
            "physical_measures": data["disease_info"].get("physical_measures"),
            "biological_control": data["disease_info"].get("biological_control"),
            "agricultural_control": data["disease_info"].get("agricultural_control"),
            "symptoms": data["disease_info"].get("symptoms"),
            "signs": data["disease_info"].get("signs"),
            "resistance_level": data["disease_info"].get("resistance_level"),
            "apid_detection": data["disease_info"].get("apid_detection"),
            "infection_mechanism": data["disease_info"].get("infection_mechanism"),
            "genes_bacteria": data["disease_info"].get("genes_bacteria"),
            "name": data["disease"].get("name"),
            "crop": data["disease"].get("crop")
        }

        print(f"{id}")
        print(entities.get("crop"))
        print(entities.get("name"))

        all = entities.get('definition_types') + "\n" + entities.get('structure_mode') + "\n" + entities.get('period_environmental') + "\n" + entities.get('overwintering') + "\n" + entities.get('chemical_control') + "\n" + entities.get('physical_measures') + "\n" + entities.get('biological_control') + "\n" + entities.get('agricultural_control') + "\n" + entities.get('symptoms') + "\n" + entities.get('signs') + "\n" + entities.get('resistance_level') + "\n" + entities.get('apid_detection') + "\n" + entities.get('infection_mechanism') + "\n" + entities.get('genes_bacteria')

        context_soup = BeautifulSoup(all, 'html.parser')

        for a in context_soup.find_all('a'):
            a.unwrap()

        for p in context_soup.find_all('p'):
            p.unwrap()


        # Путь к файлу
        file_path = f'downloaded_images/{entities.get("crop")}/{entities.get("name")}.txt'

        # Открытие файла в режиме записи (write)
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(str(context_soup))
    except:
        print(f"С {id} ошибка!")


