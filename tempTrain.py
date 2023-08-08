from deeppavlov import train_model

# Путь к JSON-файлу с конфигурациями
config_path = './cfg.json'

# Загрузка и обучение модели с использованием конфигураций из JSON-файла
model = train_model(config_path)

# Обучение с выводом логов каждые 0.1 эпохи
for epoch in range(1, model.config['train']['epochs'] + 1):
    model.fit()
    if epoch % 0.1 == 0:
        metrics = model.evaluate()
        print(f"Метрики после {epoch} эпохи:", metrics)

# Сохранение обученной модели
model.save()

print("Обучение завершено и модель сохранена.")
