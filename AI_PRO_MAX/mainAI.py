from AI_PRO_MAX import ident_prod, iterpritator, KBQA, take_question, gen_engine
from llama_cpp import Llama

model, tokens = gen_engine.interact()


def AI_COMPIL(dialog, question):
    try:
        processed_question = iterpritator.interpritator_with_history(dialog + question).replace("<extra_id_0> ",  "").replace("?</s>", "")
    except:
        try:
            processed_question = iterpritator.interpritator_with_history(question).replace("<extra_id_0> ", "").replace(
                "?</s>", "")
        except:
            return None
    file_name = ident_prod.product_identification(processed_question)

    print("\n\n\nУ нас есть: \n", processed_question)
    print(file_name)
    answer = KBQA.KBQA_search(processed_question, file_name)
    answer = gen_engine.generate(processed_question, tokens, model, answer)
    answer = answer.replace("Agrochat: ", "")
    print(answer)
    return answer
