from deeppavlov import build_model
model = build_model('qa_squad2_bert', download=True, install=True)
model(['DeepPavlov is a library for NLP and dialog systems.'], ['What is DeepPavlov?'])