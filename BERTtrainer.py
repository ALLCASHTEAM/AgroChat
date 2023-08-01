from transformers import AutoModelForQuestionAnswering, AutoTokenizer, TrainingArguments, Trainer, default_data_collator
from datasets import load_dataset
model_name = "timpal0l/mdeberta-v3-base-squad2"

# Загрузим модель и токенизатор
model = AutoModelForQuestionAnswering.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)

# Загрузим датасет
datasets = load_dataset("juletxara/xquad_xtreme", 'ru')

# Функция для предобработки данных
def prepare_train_features(examples):
    # Токенизация вопросов и контекстов
    encodings = tokenizer(
        examples["question"], examples["context"], truncation=True, padding="max_length", max_length=383, return_offsets_mapping=True
    )
    # Списки для начальных и конечных позиций ответов
    start_positions = []
    end_positions = []
    for i in range(len(examples["answers"])):
        # Получим позиции начала и конца ответа
        tmp = examples["answers"][i]
        # Получаем позиции начала и конца ответа
        start_pos = encodings.char_to_token(i, tmp['answer_start'][0])
        end_pos = encodings.char_to_token(i, tmp['answer_start'][0] + len(tmp['text']))
        # Если позиция None, это означает, что она была обрезана при токенизации контекста,
        # поэтому мы присваиваем позицию последнему токену контекста.
        if start_pos is None:
            start_positions.append(len(encodings['input_ids'][i]) - 1)
        else:
            start_positions.append(start_pos)
        if end_pos is None:
            end_positions.append(len(encodings['input_ids'][i]) - 1)
        else:
            end_positions.append(end_pos)
    # Обновляем кодировки для добавления позиций начала и конца
    encodings.update({'start_positions': start_positions, 'end_positions': end_positions})
    return encodings

# Применяем предобработку данных
tokenized_datasets = datasets.map(prepare_train_features, batched=True, remove_columns=datasets["translate_train"].column_names)

# Создаем функцию для вычисления потерь


# Устанавливаем аргументы обучения
training_args = TrainingArguments(
    output_dir="mnt/data/training",
    per_device_train_batch_size=8,
    per_device_eval_batch_size=8,
    learning_rate=2e-5,
    num_train_epochs=10,
    logging_steps=10
)

# Создаем тренер
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_datasets["translate_train"],
    eval_dataset=tokenized_datasets["translate_test"],
    data_collator=default_data_collator,

)

# Запускаем обучение
trainer.train()

