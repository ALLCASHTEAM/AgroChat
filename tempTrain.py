import torch
from transformers import BertForSequenceClassification, BertTokenizer
from torch.utils.data import DataLoader, TensorDataset

# Загружаем токенизатор
tokenizer = BertTokenizer.from_pretrained('DeepPavlov/rubert-base-cased')

# Загружаем данные
data = []
with open('qaByGPTWithOutDots.txt', 'r', encoding='utf-8') as f:
    for line in f:
        text, label = line.strip().split(' - ')
        data.append((text, label))

unique_labels = set(label for _, label in data)
num_unique_labels = len(unique_labels)
print(f"Number of unique labels: {num_unique_labels}")

# Создаем словарь для преобразования текстовых меток в числовой формат
label_map = {label: i for i, (_, label) in enumerate(data)}
num_classes = len(label_map)

# Преобразуем данные в формат, понятный модели
input_ids = []
attention_masks = []
labels = []

for text, label in data:
    encoded_inputs = tokenizer(text, padding='max_length', truncation=True, return_tensors='pt', max_length=128)
    input_ids.append(encoded_inputs['input_ids'])
    attention_masks.append(encoded_inputs['attention_mask'])
    labels.append(label_map[label])  # Преобразуем текстовую метку в числовой индекс

# Преобразуем списки в тензоры
input_ids = torch.cat(input_ids, dim=0)
attention_masks = torch.cat(attention_masks, dim=0)
labels = torch.tensor(labels)
dataset = TensorDataset(input_ids, attention_masks, labels)


# Создаем датасет и загрузчик данных
dataset = TensorDataset(input_ids, attention_masks, labels)
loader = DataLoader(dataset, batch_size=16, shuffle=True)

# Создаем модель
model = BertForSequenceClassification.from_pretrained('DeepPavlov/rubert-base-cased', num_labels=num_classes)

# Определите оптимизатор и функцию потерь
optimizer = torch.optim.AdamW(model.parameters(), lr=2e-5)
criterion = torch.nn.CrossEntropyLoss()

# Обучение модели
for epoch in range(10):
    model.train()
    total_loss = 0
    for batch in loader:
        optimizer.zero_grad()
        input_ids, attention_mask, label = batch
        outputs = model(input_ids, attention_mask=attention_mask, labels=label)
        loss = outputs.loss
        loss.backward()
        optimizer.step()
        total_loss += loss.item()
    print(f"Epoch {epoch+1}, Loss: {total_loss}")

# Сохраняем модель
model.save_pretrained('model')
