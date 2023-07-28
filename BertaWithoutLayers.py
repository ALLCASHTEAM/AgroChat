import torch
import numpy as np
from transformers import AutoTokenizer, AutoModelForQuestionAnswering

tokenizer = AutoTokenizer.from_pretrained("timpal0l/mdeberta-v3-base-squad2")
model = AutoModelForQuestionAnswering.from_pretrained("timpal0l/mdeberta-v3-base-squad2")

text = """Название товара: Биостим Свекл; Тип Биостим Свекл: аминокислоты, полисахариды, макро- и микроэлементы; Биостим Свекл - это Жидкое аминокислотное удобрение-биостимулятор для листовых подкормок сахарной свеклы; Достоинства Биостим Свекл: Удобрение-биостимулятор с микроэлементами для сахарной и столовой свеклы, Стимулирует обмен веществ в растениях, Поддерживает баланс питательных веществ в период вегетации, Защищает от воздействия абиотических стрессов, Восстанавливает продуктивность культур после действия стресс-факторов, Повышает устойчивость растений к болезням, Улучшает количественные и качественные параметры урожая;
Название товара: Биостим Стар; Тип Биостим Стар: аминокислоты, полисахариды, макро- и микроэлементы; Биостим Стар - это Жидкое аминокислотное удобрение-биостимулятор для предпосевной обработки семян и посадочного материала, а также для корневых подкормок рассады; Достоинства Биостим Стар: Активатор энергии и стимулятор прорастания семян, Более ранние и дружные всходы, Ускоренное формирование корневой системы, Улучшение приживаемости рассады и минимизация послепересадочных стрессов;
Название товара: Биостим Кукуруз; Тип Биостим Кукуруз: аминокислоты, полисахариды, макро- и микроэлементы; Биостим Кукуруз это - Жидкое аминокислотное удобрение-биостимулятор для листовых подкормок кукурузы; Достоинства Биостим Кукуруз: Удобрение-биостимулятор с микроэлементами разработанное специально для кукурузы на зерно и силос, Стимулирует обмен веществ в растениях, Поддерживает баланс питательных веществ в период вегетации, Защищает от воздействия абиотических стрессов, Восстанавливает продуктивность культур после действия стресс-факторов, Повышает устойчивость растений к болезням, Улучшает количественные и качественные параметры урожая;
Название товара: Биостим Рос; Тип Биостим Рос: аминокислоты, полисахариды, макро- и микроэлементы; Биостим Рос - это Жидкое аминокислотное удобрение-биостимулятор для листовых подкормок сельскохозяйственных культур в начале вегетации: Достоинства Биостим Рос: Стимулирует вегетативный рост в начале весенней вегетации, Активирует ростовые процессы в условиях затяжной весны и других неблагоприятных погодных условиях, Восстанавливает ослабленные и поврежденные посевы после перезимовки, Защищает от воздействия абиотических стресс-факторов (возвратных заморозков весной, засухи и т.д.), Является активатором фотосинтеза, Подходит для всех культур в начале весенней вегетации;"""

question = input('Введите вопрос: ')

tokenized = tokenizer.encode_plus(
   question, text,
   add_special_tokens=False
)

# Обработка токенизированного текста
input_ids = tokenized['input_ids']
token_type_ids = tokenized['token_type_ids']
attention_mask = tokenized['attention_mask']

# Преобразование в тензоры
input_ids = torch.tensor([input_ids])
token_type_ids = torch.tensor([token_type_ids])
attention_mask = torch.tensor([attention_mask])

# Предсказание ответа
with torch.no_grad():
    outputs = model(input_ids=input_ids, token_type_ids=token_type_ids, attention_mask=attention_mask)

# Получение позиций начала и конца ответа
start_index = torch.argmax(outputs.start_logits)
end_index = torch.argmax(outputs.end_logits)

# Получение текста ответа
answer = tokenizer.decode(input_ids[0][start_index:end_index+1])

print('Вопрос:', question)
print('Ответ:', answer)
