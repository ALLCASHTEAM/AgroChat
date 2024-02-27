from AI_PRO_MAX import classify_personal_questions
from AI_PRO_MAX.faiss_py import model, list_return
from sentence_transformers import SentenceTransformer, util
from typing import List, Tuple, Optional


def find_best_matches(user_query: str, sentence_model) -> Tuple[List[Tuple[str, float, int]], Optional[List]]:
    try:
        liness = list_return(user_query)
        lines = [line[0].lower() for line in liness]
        user_query_prefixed = "query: " + user_query.lower()

        # Предварительное кодирование запроса пользователя и текстов для сравнения
        user_query_encoded = sentence_model.encode(user_query_prefixed)
        lines_encoded = sentence_model.encode(["passage: " + line for line in lines])

        similarities = util.pytorch_cos_sim(user_query_encoded, lines_encoded)[0]

        # Создание списка совпадений и их оценок вместе с исходными индексами строк
        matches = [(lines[i], similarities[i].item(), i) for i in range(len(lines))]
        matches.sort(key=lambda x: x[1], reverse=True)

        return matches[:8], liness
    except Exception as e:
        print(f"Error: {e}")
        return None, None


def KBQA_search(user_query: str) -> Optional[str]:
    print("INFO: База запущенна")
    if not classify_personal_questions.is_personal(user_query) or user_query == "привет":
        matches, liness = find_best_matches(user_query, model)
        if matches:
            try:
                # Предварительное создание списка уникальных ключевых фраз из matches
                match_phrases = {match[0].replace('?', '').strip() for match in matches}
                answer = " ".join([f"{line[0].replace('?', '').strip()} - {line[1]}"
                                   for line in liness if line[0].replace('?', '').lower().strip() in match_phrases])

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
