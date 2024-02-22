from AI_PRO_MAX import classify_personal_questions
from sentence_transformers import SentenceTransformer, util
from AI_PRO_MAX.faiss_py import model, list_return


def find_best_matches(user_query, sentence_model):
    try:
        liness = list_return(user_query)
        lines = list(zip(*liness))[0]
        user_query_prefixed = "query: " + user_query.lower()

        # Добавление префикса "passage:" к каждой строке из lines
        lines_prefixed = ["passage: " + line.lower() for line in lines]
        similarities = util.pytorch_cos_sim(sentence_model.encode(user_query_prefixed),
                                            sentence_model.encode(lines_prefixed))[0]

        # Создание списка совпадений и их оценок вместе с исходными индексами строк
        matches = [(lines[i], similarities[i], i) for i in range(len(lines))]

        # Сортировка списка совпадений по оценкам в убывающем порядке
        matches.sort(key=lambda x: x[1], reverse=True)
        return matches[:8], liness
    except:
        return None, None


def KBQA_search(user_query):
    print("INFO: База запущенна")
    if not classify_personal_questions.is_personal(user_query):
        matches, liness = find_best_matches(user_query, model)
        if matches is not None:
            try:
                answer = ""
                for line in liness:
                    if line[0].replace('?', '').lower().strip() in list(map(lambda x: x.lower().strip(), list(map(
                            lambda x: str(x).replace("('", "").split("?")[0], matches)))):
                        answer += line[0].replace('?', '').lower().strip() + " - " + line[1]

                print("INFO: Ответ от базы", answer)
                return answer
            except Exception as e:
                print(f"Waring: Ответ от базы пуст. Ошибка: {e}")
                return None
        else:
            print("Waring: Ошибка при поиске совпадений")
            return None
    else:
        print("INFO: Чит-чат режим (без базы)")
        return None


if __name__ == "__main__":
    user_query = "Чем обрабатывать кукурузу?"
    KBQA_search(user_query)
