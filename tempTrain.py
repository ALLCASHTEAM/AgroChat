import torch
from transformers import BertForSequenceClassification, BertTokenizer

# Загружаем токенизатор
tokenizer = BertTokenizer.from_pretrained('DeepPavlov/rubert-base-cased')

# Загружаем данные
data = []
with open('qaByGPTWithOutDots.txt.txt', 'r') as f:
  for line in f:
    text, label = line.split(' - ')
    data.append((text, label))

# Преобразуем данные в формат, понятный модели
input_ids = []
attention_masks = []
labels = []
for text, label in data:
  encoded_inputs = tokenizer(text, return_tensors='pt')
  input_ids.append(encoded_inputs['input_ids'])
  attention_masks.append(encoded_inputs['attention_mask'])
  labels.append(label)

# Создаем модель
model = BertForSequenceClassification.from_pretrained('DeepPavlov/rubert-base-cased')

# Обучаем модель
model.fit(input_ids, attention_masks, labels, epochs=10)

# Сохраняем модель
model.save_pretrained('model')
