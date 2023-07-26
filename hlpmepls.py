from transformers import ViTFeatureExtractor, ViTForImageClassification
from transformers import Trainer, TrainingArguments
import torch

# Загрузка предобученного экстрактора признаков для ViT
feature_extractor = ViTFeatureExtractor.from_pretrained("google/vit-base-patch16-224-in21k")

# Загрузка предобученной модели ViT для классификации изображений
model = ViTForImageClassification.from_pretrained("google/vit-base-patch16-224-in21k")

# Загрузка и подготовка своего датасета с изображениями растений
# Вам нужно подготовить свой датасет и определить правильные классы для классификации

# Тренировка модели на своем датасете
training_args = TrainingArguments(
    output_dir="./results",
    num_train_epochs=3,
    per_device_train_batch_size=16,
    save_steps=500,
    save_total_limit=2,
    learning_rate=2e-5,
    push_to_hub=False,  # Вы можете сохранить модель на Hugging Face Hub, если нужно
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=your_train_dataset,  # Замените на свой датасет
)

trainer.train()
