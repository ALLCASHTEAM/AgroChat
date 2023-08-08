from deeppavlov import configs, train_model

# Путь к вашему текстовому файлу
data_path = 'qaByGPTWithOutDots.txt'

# Загрузка конфигурации модели DeepPavlov/rubert-case-based
config = configs.classifiers.rusentiment.rusentiment_bert

# Изменение параметров конфигурации
config['dataset_reader']['data_path'] = data_path
config['metadata']['variables']['DATA_PATH'] = data_path
config['train']['batch_size'] = 8
config['train']['epochs'] = 5

# Загрузка и обучение модели
model = train_model(config)

# Обучение с выводом логов каждые 0.1 эпохи
for epoch in range(1, config['train']['epochs'] + 1):
    model.fit()
    if epoch % 0.1 == 0:
        metrics = model.evaluate()
        print(f"Метрики после {epoch} эпохи:", metrics)

# Сохранение обученной модели
model.save()

print("Обучение завершено и модель сохранена.")
