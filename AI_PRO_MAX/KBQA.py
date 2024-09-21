from typing import Optional, List, Tuple
from AI_PRO_MAX.faiss_py import list_return
from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer('intfloat/multilingual-e5-large')


def find_best_matches(user_query: str, sentence_model: SentenceTransformer, top_k: int = 8):
    """
    :return Tuple[Optional[List[Tuple[str, float, int]]], Optional[List[Tuple[str, str]]]]
    """
    try:
        candidates = list_return(user_query)
        if not candidates:
            print("No candidates found in the index.")
            return None, None

        questions_answers = candidates
        questions = [qa[0].lower().strip() for qa in questions_answers]

        user_query_prefixed = f"query: {user_query.lower().strip()}"
        passages_prefixed = [f"passage: {q}" for q in questions]

        user_query_encoded = sentence_model.encode(user_query_prefixed, normalize_embeddings=True)
        passages_encoded = sentence_model.encode(passages_prefixed, normalize_embeddings=True)

        similarities = util.cos_sim(user_query_encoded, passages_encoded)[0]

        matches = [(questions[i], similarities[i].item(), i) for i in range(len(questions))]

        matches.sort(key=lambda x: x[1], reverse=True)

        return matches[:top_k], questions_answers

    except Exception as e:
        print(f"Error in find_best_matches: {e}")
        return None, None


def KBQA_search(user_query: str):
    print("INFO: База запущенна")
    matches, questions_answers = find_best_matches(user_query, model)
    if not matches or not questions_answers:
        print("Warning: Совпадения не найдены или во время поиска произошла ошибка.")
        return None
    try:
        top_matched_questions = {match[0] for match in matches}

        answers = [
            f"{qa[0].strip()} - {qa[1].strip()}"
            for qa in questions_answers
            if qa[0].lower().strip() in top_matched_questions
        ]

        if not answers:
            print("Warning: Ни один ответ не совпал с самыми популярными вопросами.")
            return None

        answer = " ".join(answers)
        print(f"INFO: Found {len(answers)} answers.")
        print(f"ANSWER: {answer}")
        return answer

    except Exception as e:
        print(f"Warning: Не удалось построить ответ. Ошибка: {e}")
        return None


if __name__ == "__main__":
    user_query = "что такое биостим кукуруза"
    KBQA_search(user_query)
