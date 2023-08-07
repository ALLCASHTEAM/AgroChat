def remove_commas_and_periods(file_path, output_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()

    # Удаление запятых и точек
    text_without_commas_and_periods = text.replace(',', '').replace('.', '')

    with open(output_path, 'w', encoding='utf-8') as output_file:
        output_file.write(text_without_commas_and_periods)

# Пример использования
input_file_path = './qaByGPT.txt'   # Путь к исходному файлу
output_file_path = './qaByGPTWithOutDots.txt' # Путь к файлу, в котором будут результаты без запятых и точек

remove_commas_and_periods(input_file_path, output_file_path)
