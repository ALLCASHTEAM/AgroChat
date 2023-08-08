from transformers import AutoModelForQuestionAnswering, AutoTokenizer, TrainingArguments, Trainer, default_data_collator
from datasets import Dataset
import torch

model_name = "timpal0l/mdeberta-v3-base-squad2"
data_file = "qaByGPTWithOutDots.txt"  # Имя файла

# Загрузим модель и токенизатор
model = AutoModelForQuestionAnswering.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)

# Загрузка данных из текстового файла
with open(data_file, "r", encoding="utf-8") as f:
    lines = f.readlines()

# Создание датасета
qa_data = {"question": [], "context": []}
for line in lines:
    line = line.strip()  # Убираем символ перевода строки
    if " - " in line:
        question, context = line.split(" - ")
        qa_data["question"].append(question)
        qa_data["context"].append(context)
    else:
        print(f"Ошибка в строке: {line}")

dataset = Dataset.from_dict(qa_data)

# Функция для предобработки данных
def prepare_train_features(examples):
    encodings = tokenizer(
        examples["question"], examples["context"],
        truncation=True, padding="max_length", max_length=383,
        return_offsets_mapping=True
    )
    # Ваш код для обработки позиций начала и конца ответов

    return encodings

# Применяем предобработку данных
tokenized_dataset = dataset.map(prepare_train_features, batched=True)

# Создаем аргументы для обучения
training_args = TrainingArguments(
    output_dir="./training",
    overwrite_output_dir=True,
    per_device_train_batch_size=8,
    per_device_eval_batch_size=8,
    gradient_accumulation_steps=16,
    warmup_steps=100,
    num_train_epochs=3,
    logging_steps=1000,
)

# Создаем тренер
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_dataset,
    data_collator=default_data_collator,
    optimizers=(torch.optim.AdamW(model.parameters(), lr=1e-5), None),
)

# Запускаем обучение
trainer.train()
