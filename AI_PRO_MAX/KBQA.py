from AI_PRO_MAX.faiss_py import list_return
from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer('intfloat/multilingual-e5-large')


def find_best_matches(user_query, sentence_model):
    try:
        liness = list_return(user_query)
        lines = [line[0].lower() for line in liness]
        user_query_prefixed = "query: " + user_query.lower()

        # Предварительное кодирование запроса пользователя и текстов для сравнения
        model.eval()
        user_query_encoded = sentence_model.encode(user_query_prefixed, normalize_embeddings=True)
        lines_encoded = sentence_model.encode(["passage: " + line for line in lines], normalize_embeddings=True)

        similarities = util.pytorch_cos_sim(user_query_encoded, lines_encoded)[0]

        # Создание списка совпадений и их оценок вместе с исходными индексами строк
        matches = [(lines[i], similarities[i], i) for i in range(len(lines))]

        # Сортировка списка совпадений по оценкам в убывающем порядке
        matches.sort(key=lambda x: x[1], reverse=True)
        return matches[:8], liness
    except Exception as e:
        print(e)
        return None, None



def KBQA_search(user_query: str):
    print("INFO: База запущенна")
    matches, liness = find_best_matches(user_query, model)
    if matches:
        print(len(matches))
        try:
            answer = ""
            for line in liness:
                if line[0].replace('?', '').lower().strip() in list(map(lambda x: x.lower().strip(), list(map(
                        lambda x: str(x).replace("('", "").split("?")[0], matches)))):
                    answer += line[0].replace('?', '').lower().strip() + " - " + line[1].lower().strip() + " "
            print(answer)
            return answer
        except Exception as e:
            print(f"Warning: Ответ от базы пуст. Ошибка: {e}")
            return None
    else:
        print("Warning: Ошибка при поиске совпадений")
        return None


if __name__ == "__main__":
    user_query = "что такое биостим кукуруза"
    KBQA_search(user_query)
