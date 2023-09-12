from transformers import AutoTokenizer, AutoModel
from sentence_transformers import SentenceTransformer, util

# Загрузка русскоязычной модели Sentence Transformers
model_name = "paraphrase-MiniLM-L6-v2"
model = SentenceTransformer(model_name)

# Две русскоязычные строки для сравнения
text1 = "Как пользоваться биостим кукуруз?"
print("Вопрос: ",text1, "\n Варианты: ")
# Получение эмбеддингов для первой строки
embeddings1 = model.encode(text1, convert_to_tensor=True)

matches = []

with open("C://Users//Ирина//Documents//GitHub//AgroChat//rofls//Биостим Кукуруза.txt", 'r', encoding='utf-8') as file:
    lines = file.readlines()
    for line in lines:
        part = line.strip().split("|")[0]
        embeddings2 = model.encode(part, convert_to_tensor=True)
        # Вычисление косинусного расстояния между эмбеддингами
        cosine_score = util.pytorch_cos_sim(embeddings1, embeddings2)
        #print(str(part), "имеет схожесть ", str(cosine_score).replace("tensor([[","").replace("]])",""))
        match = str(part) +  str(cosine_score).replace("tensor([["," ").replace("]])","")
        matches.append(match)

result_arr = sorted(matches, key=lambda line: float(line.split()[-1]), reverse=True)

result_arr = result_arr[:5]
# Выводим отсортированные строки
#print(result_arr)
for i in range(5):
    print(result_arr[i])
