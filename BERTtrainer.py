from transformers import AutoModelForQuestionAnswering, AutoTokenizer, Trainer, TrainingArguments
from datasets import load_dataset
from transformers.data.data_collator import default_data_collator

# Загрузите датасет XQuAD для русского языка
dataset = load_dataset('xquad', 'xquad.ru', split='validation')

print("Number of examples in the dataset:", len(dataset))

model_name_ru = "timpal0l/mdeberta-v3-base-squad2"

# Загрузите токенизатор и конфигурацию модели
tokenizer = AutoTokenizer.from_pretrained(model_name_ru)
model = AutoModelForQuestionAnswering.from_pretrained(model_name_ru)

# Определите функцию для обработки данных и конфигурацию обучения
data_collator = default_data_collator
training_args = TrainingArguments(
    output_dir="./models",  # Укажите путь к сохранению модели и результатов
    num_train_epochs=5,          # Количество эпох для обучения (можете увеличить для лучших результатов)
    per_device_train_batch_size=1,
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
    train_dataset=dataset,       # Используйте загруженный датасет
    tokenizer=tokenizer,
)

# Запустите обучение
trainer.train()

# Сохраните дообученную модель
trainer.save_model("./fine_tuned_model")
