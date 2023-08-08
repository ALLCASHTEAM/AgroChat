import torch
from transformers import BertForSequenceClassification, BertTokenizer, AutoTokenizer, TrainingArguments, Trainer, default_data_collator

# Загружаем токенизатор
tokenizer = AutoTokenizer.from_pretrained('DeepPavlov/rubert-base-cased')

# Загружаем данные
data = []
with open('qaByGPTWithOutDots.txt', 'r') as f:
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

print(data,text,label)

# Создаем модель
model = BertForSequenceClassification.from_pretrained('DeepPavlov/rubert-base-cased')

training_args = TrainingArguments(
    output_dir="/mnt/data/training",
    overwrite_output_dir=True,
    per_device_train_batch_size=8,
    per_device_eval_batch_size=8,
    gradient_accumulation_steps=16,
    warmup_steps=100,
    num_train_epochs=3,
    logging_steps=10,


)

# Создаем тренер
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=data,
    data_collator=default_data_collator,
    optimizers = (torch.optim.AdamW(model.parameters(),lr=1e-5),None),

)


# Обучаем модель
model.train(input_ids, attention_masks, labels, epochs=10)

# Сохраняем модель
model.save_pretrained('model')
