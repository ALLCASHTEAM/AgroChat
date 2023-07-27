from transformers import pipeline

model_name = "timpal0l/mdeberta-v3-base-squad2"
model = pipeline("question-answering", model=model_name, tokenizer=model_name)

context = "Название товара: Биостим Свекл; Тип Биостим Свекл: аминокислоты, полисахариды, макро- и микроэлементы; Биостим Свекл - это Жидкое аминокислотное удобрение-биостимулятор для листовых подкормок сахарной свеклы; Достоинства Биостим Свекл перед другими удобрениями: Удобрение-биостимулятор с микроэлементами для сахарной, столовой свеклы Стимулирует обмен веществ в растениях, Поддерживает баланс питательных веществ в период вегетации, Защищает от воздействия абиотических стрессов, Восстанавливает продуктивность культур после действия стресс-факторов, Повышает устойчивость растений к болезням, Улучшает количественные и качественные параметры урожая; Название товара: Биостим Стар;Тип Биостим Стар: аминокислоты, полисахариды, макро- и микроэлементы; Биостим Стар - это Жидкое аминокислотное удобрение-биостимулятор для предпосевной обработки семян и посадочного материала, а также для корневых подкормок рассады; Достоинства Биостим Стар: Активатор энергии и стимулятор прорастания семянБолее ранние и дружные всходыУскоренное формирование корневой системыУлучшение приживаемости рассады и минимизация послепересадочных стрессов; Название товара: Биостим Кукуруз;Тип Биостим Кукуруз: аминокислоты, полисахариды, макро- и микроэлементы; Биостим Кукуруз это - Жидкое аминокислотное удобрение-биостимулятор для листовых подкормок кукурузы; Достоинства Биостим Кукуруз: 1.Удобрение-биостимулятор с микроэлементами, 2.разработанное специально для кукурузы на зерно и силос, 3.Стимулирует обмен веществ в растениях, 4.Поддерживает баланс питательных веществ в период вегетации, 5.Защищает от воздействия абиотических стрессов, 6.Восстанавливает продуктивность культур после действия стресс-факторов, 7.Повышает устойчивость растений к болезням, 8.Улучшает количественные и качественные параметры урожая; Название товара: Биостим Рос; Тип Биостим Рос: аминокислоты, полисахариды, макро- и микроэлементы; Биостим Рос - это Жидкое аминокислотное удобрение-биостимулятор для листовых подкормок сельскохозяйственных культур в начале вегетации; Достоинства Биостим Рос: Стимулирует вегетативный рост в начале весенней вегетации, Активирует ростовые процессы в условиях затяжной весны и других неблагоприятных погодных условиях, Восстанавливает ослабленные, поврежденные посевы после перезимовки, Защищает от воздействия абиотических стресс-факторов (возвратных заморозков весной, засухи и т.д.),Является активатором фотосинтеза Подходит для всех культур в начале весенней вегетации;"


question = "Какие достоинства у Биостим Кукуруз, а не у Биостим Рос?"

result = model(question=question, context=context)

print("Ответ:", result["answer"])
print("Развернутый ответ:", result["answer"], "начиная с символа", result["start"], "и заканчивая символом", result["end"])
