input_filename = 'qaByGPTWithOutDots.txt'
output_filename = 'rofls/qa_replased.txt'

with open(input_filename, 'r', encoding='utf-8') as input_file:
    lines = input_file.readlines()

output_lines = []
for line in lines:
    question, answer = line.strip().split(' - ')
    output_lines.append(f'Вопрос: {question}\nОтвет: {answer}.\n\n')

with open(output_filename, 'w', encoding='utf-8') as output_file:
    output_file.writelines(output_lines)