from transformers import AutoModelForQuestionAnswering, AutoTokenizer, pipeline, TrainingArguments, Trainer
from datasets import load_dataset
from txtai.pipeline import HFTrainer

ds = load_dataset("xtreme", "XQuAD.ru")



# Load model directly
# Use a pipeline as a high-level helper
model_name_ru = "timpal0l/mdeberta-v3-base-squad2"
trainer = HFTrainer()

model = AutoModelForQuestionAnswering.from_pretrained(model_name_ru)

model, tokenizer = trainer(model, ds, task="question-answering", num_train_epochs=10)

from transformers import pipeline

questions = pipeline("question-answering", model=model, tokenizer=tokenizer)
questions("Чем удобрять кукурузу?", """Биостим Зерновой - жидкое аминокислотное удобрение-биостимулятор для листовых подкормок зерновых культур;
Биостим Кукуруза - жидкое аминокислотное удобрение-биостимулятор для листовых подкормок кукурузы;
Биостим Масличный - жидкое аминокислотное удобрение-биостимулятор для листовых подкормок масличных и бобовых культур;""")