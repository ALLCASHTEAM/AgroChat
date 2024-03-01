from AI_PRO_MAX import classify_personal_questions
from AI_PRO_MAX.faiss_py import model, list_return
from sentence_transformers import SentenceTransformer, util



def find_best_matches(user_query, sentence_model):
    try:
        liness = list_return(user_query)
        lines = [line[0].lower() for line in liness]
        user_query_prefixed = "query: " + user_query.lower()

        # Предварительное кодирование запроса пользователя и текстов для сравнения
        user_query_encoded = sentence_model.encode(user_query_prefixed)
        lines_encoded = sentence_model.encode(["passage: " + line for line in lines])

        similarities = util.pytorch_cos_sim(user_query_encoded, lines_encoded)[0]

        # Создание списка совпадений и их оценок вместе с исходными индексами строк
        matches = [(lines[i], similarities[i], i) for i in range(len(lines))]

        # Сортировка списка совпадений по оценкам в убывающем порядке
        matches.sort(key=lambda x: x[1], reverse=True)

        return matches[:8], liness
    except:
        return None, None


def KBQA_search(user_query: str):
    print("INFO: База запущенна")
    if  user_query.strip() == "привет":
        matches, liness = find_best_matches(user_query, model)
        if matches:
            try:
                answer = ""
                for line in liness:
                    if line[0].replace('?', '').lower().strip() in list(map(lambda x: x.lower().strip(), list(map(
                            lambda x: str(x).replace("('", "").split("?")[0], matches)))):
                        answer += line[0].replace('?', '').lower().strip() + " - " + line[1]

                if answer:
                    print("INFO: Ответ от базы", answer)
                    return answer
                else:
                    print("Warning: Нет подходящих ответов.")
                    return None
            except Exception as e:
                print(f"Warning: Ответ от базы пуст. Ошибка: {e}")
                return None
        else:
            print("Warning: Ошибка при поиске совпадений")
            return None
    else:
        print("INFO: Чит-чат режим (без базы)")
        return None

if __name__ == "__main__":
    user_query = "Чем обрабатывать кукурузу?"
    KBQA_search(user_query)
