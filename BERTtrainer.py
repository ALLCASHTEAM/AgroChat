from transformers import AutoModelForQuestionAnswering, AutoTokenizer, Trainer, TrainingArguments
from datasets import load_dataset
import torch

# Загрузите датасет XQuAD.ru для обучения
dataset = load_dataset('xtreme', 'XQuAD.ru', split="validation")

print("Number of examples in the dataset:", len(dataset))

model_name_ru = "timpal0l/mdeberta-v3-base-squad2"

# Загрузите токенизатор и конфигурацию модели
tokenizer = AutoTokenizer.from_pretrained(model_name_ru)
model = AutoModelForQuestionAnswering.from_pretrained(model_name_ru)

# Определите функцию для обработки данных и конфигурацию обучения
def custom_data_collator(features):
    batch = {}
    batch["input_ids"] = torch.stack([feature["input_ids"] for feature in features])
    batch["attention_mask"] = torch.stack([feature["attention_mask"] for feature in features])
    batch["start_positions"] = torch.stack([feature["start_positions"] for feature in features])
    batch["end_positions"] = torch.stack([feature["end_positions"] for feature in features])
    return batch

training_args = TrainingArguments(
    output_dir="./models",  # Укажите путь к сохранению модели и результатов
    num_train_epochs=5,          # Количество эпох для обучения (можете увеличить для лучших результатов)
    per_device_train_batch_size=1,
    save_steps=100,             # Сохранять модель каждые 1000 шагов обучения
    save_total_limit=2,          # Ограничьте количество сохраненных моделей
    evaluation_strategy="steps", # Оценивать результаты каждые 1000 шагов обучения
    eval_steps=100,             # Частота оценивания
)

# Создайте объект Trainer для обучения модели
trainer = Trainer(
    model=model,
    args=training_args,
    data_collator=custom_data_collator,
    train_dataset=dataset,       # Используйте загруженный датасет
    tokenizer=tokenizer,
)

# Запустите обучение
trainer.train()

# Сохраните дообученную модель
trainer.save_model("./fine_tuned_model")
