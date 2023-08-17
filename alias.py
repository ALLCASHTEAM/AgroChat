import json

input_file = 'seeds.txt'
output_file = 'dataset2.jsonl'

with open(input_file, 'r', encoding="utf8") as f:
    lines = f.readlines()


with open(output_file, 'w', encoding="utf8") as f:
    for line in lines:
        # Заменяем одинарные кавычки на двойные
        line = line.replace("'", '"')
        f.write(line)

print('Замена завершена.')
