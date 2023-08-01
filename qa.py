from transformers import AutoModelForQuestionAnswering, AutoTokenizer, AutoConfig, Trainer, TrainingArguments
from transformers.data.data_collator import DataCollatorWithPadding
import torch

# Загрузите свои данные для дообучения здесь
# Вам нужно представить данные в формате, который подходит для модели вопрос-ответ
# Пожалуйста, замените 'train_dataset' на свои данные
train_dataset = ...

model_name_ru = "timpal0l/mdeberta-v3-base-squad2"

# Загрузите токенизатор и конфигурацию модели
tokenizer = AutoTokenizer.from_pretrained(model_name_ru)
config = AutoConfig.from_pretrained(model_name_ru)
model = AutoModelForQuestionAnswering.from_pretrained(model_name_ru, config=config)

# Определите функцию для обработки данных и конфигурацию обучения
data_collator = DataCollatorWithPadding(tokenizer=tokenizer)
training_args = TrainingArguments(
    output_dir="./output_dir",  # Укажите путь к сохранению модели и результатов
    num_train_epochs=1,          # Количество эпох для обучения (можете увеличить для лучших результатов)
    per_device_train_batch_size=8,
    save_steps=1000,             # Сохранять модель каждые 1000 шагов обучения
    save_total_limit=2,          # Ограничьте количество сохраненных моделей
    evaluation_strategy="steps", # Оценивать результаты каждые 1000 шагов обучения
    eval_steps=1000,             # Частота оценивания
)

# Создайте объект Trainer для обучения модели
trainer = Trainer(
    model=model,
    args=training_args,
    data_collator=data_collator,
    train_dataset=train_dataset,
    tokenizer=tokenizer,
)

# Запустите обучение
trainer.train()

# Сохраните дообученную модель
trainer.save_model("./fine_tuned_model")