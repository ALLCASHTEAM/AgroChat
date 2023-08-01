from transformers import AutoModelForQuestionAnswering, AutoTokenizer, pipeline

with open('boosters.txt', 'r', encoding='utf-8') as f:
    boostrap = f.read()

QA_input = [
{
    'question': 'Чем удобрять кукурузу?',
    'context': boostrap.replace('\n', '').replace(';', '. ').replace('..', '.').replace(',', '')
}
]

# Load model directly
# Use a pipeline as a high-level helper
model_name_ru = "timpal0l/mdeberta-v3-base-squad2"

tokenizer = AutoTokenizer.from_pretrained(model_name_ru)
model = AutoModelForQuestionAnswering.from_pretrained(model_name_ru)

# Use a pipeline as a high-level helper

pipe = pipeline("question-answering", model=model, tokenizer=tokenizer)

print(model_name_ru, " :")
for i in range(100):
    for el in QA_input:
        print(pipe(el))


