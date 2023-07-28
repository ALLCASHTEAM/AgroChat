from transformers import BertTokenizer, BertForQuestionAnswering, BertConfig
from transformers import AdamW
import torch
import json

# Загрузка токенизатора и предварительно обученной модели для русского языка
tokenizer = BertTokenizer.from_pretrained("bert-base-multilingual-cased")
model = BertForQuestionAnswering.from_pretrained("bert-base-multilingual-cased")

# Заморозка всех параметров модели, чтобы сохранить предварительно обученные веса
for param in model.parameters():
    param.requires_grad = False

# Загрузка датасета из JSON файла
with open("your_dataset.json", "r", encoding="utf-8") as f:
    data = json.load(f)

#количество эпох
num_epochs = 5

# Процесс дообучения модели
model.train()
optimizer = AdamW(model.parameters(), lr=1e-5)

for epoch in range(num_epochs):
    total_loss = 0.0
    for example in data:
        # Загрузка текста из файла
        with open(example["text_file"], "r", encoding="utf-8") as f:
            context = f.read()

        # Форматирование данных для вопросно-ответного форматирования
        inputs = tokenizer.encode_plus(example["question"], context, return_tensors="pt", add_special_tokens=True, max_length=512, pad_to_max_length=True)
        start_positions = tokenizer.encode(example["answer"], add_special_tokens=False)[0]
        end_positions = tokenizer.encode(example["answer"], add_special_tokens=False)[-1]

        inputs.update({'start_positions': torch.tensor([start_positions]), 'end_positions': torch.tensor([end_positions])})

        outputs = model(**inputs)
        loss = outputs.loss
        total_loss += loss.item()
        loss.backward()
        optimizer.step()
        optimizer.zero_grad()

    avg_loss = total_loss / len(data)
    print(f"Epoch {epoch + 1}/{num_epochs}, Average Loss: {avg_loss}")

# Сохранение дообученной модели
model.save_pretrained("path_to_save_model")
