from AI_PRO_MAX import realsweg, classify_personal_questions
from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer("sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")


def find_best_matches(user_query, sentence_model):
    try:
        liness = [x.split("|") for x in realsweg.list_return(user_query)]
        lines = [line[0] for line in liness]
        query_embedding = sentence_model.encode(user_query.lower())
        line_embeddings = sentence_model.encode([line.lower() for line in lines])
        similarities = util.pytorch_cos_sim(query_embedding, line_embeddings)[0]

        matches = sorted(((lines[i], similarities[i], i) for i in range(len(lines))),
                         key=lambda x: x[1], reverse=True)
        return matches[:3], liness
    except Exception as e:
        print(f"Ошибка: {e}")
        return None, None


def KBQA_search(user_query):
    print("INFO. База запущенна")
    matches, liness = find_best_matches(user_query, model)
    if matches is not None:
        try:
            answer = ""
            matched_questions = {x.lower().strip() for x, _, _ in matches}
            for line in liness:
                question = line[0].replace('?', '').lower().strip()
                if question in matched_questions:
                    answer += line[1]

            print("INFO. Ответ от базы", answer)
            return answer
        except Exception as e:
            print(f"Waring!. Ответ от базы пуст. Ошибка: {e}")
            return None
    else:
        print("Waring!. Ошибка при поиске совпадений")
        return None


if __name__ == "__main__":
    user_query = "Чем обрабатывать кукурузу?"
    KBQA_search(user_query)
