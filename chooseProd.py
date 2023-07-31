# import os
# from transformers import GPT2Tokenizer, GPT2LMHeadModel
#
# os.environ['TF_ENABLE_ONEDNN_OPTS=0']
#
# tokenizer = GPT2Tokenizer.from_pretrained("ai-forever/ruGPT-3.5-13B")
# model = GPT2LMHeadModel.from_pretrained("ai-forever/ruGPT-3.5-13B")
# model.half()
# model.to('cuda:0')
#
# def IdentProd(text):
#     file_path = './boosters.txt'
#
#     with open(file_path, 'r') as file:
#         content = file.read()
#
#     promt = "Представим что ты агроном-продавецконсультант, вот так выглядит твой каталог: "+content+"а покупатель спрашивает это: "+text+" "#cюда еще добавлять диалог этот, например из 20 сообщений предидущих и тогда заебися будет пахнуть наша пися
#     encoded_input = tokenizer(promt, return_tensors='pt', add_special_tokens=False).to('cuda:0')
#     output = model.generate(
#         **encoded_input,
#         num_beams=2,
#         do_sample=True,
#         max_new_tokens=60
#         )
#
#     print(tokenizer.decode(output[0], skip_special_tokens=True))
#
# IdentProd("Чем мне удобрить кукурузу")
import tensorflow as tf
import os


def get_mkl_enabled_flag():
    mkl_enabled = False
    major_version = int(tf.__version__.split(".")[0])
    minor_version = int(tf.__version__.split(".")[1])
    if major_version >= 2:
        if minor_version < 5:
            from tensorflow.python import _pywrap_util_port
        elif minor_version >= 9:

            from tensorflow.python.util import _pywrap_util_port
            onednn_enabled = int(os.environ.get('TF_ENABLE_ONEDNN_OPTS', '1'))
            os.environ.setdefault('TF_ENABLE_ONEDNN_OPTS', '1')

        else:
            from tensorflow.python.util import _pywrap_util_port
            onednn_enabled = int(os.environ.get('TF_ENABLE_ONEDNN_OPTS', '0'))
        mkl_enabled = _pywrap_util_port.IsMklEnabled() or (onednn_enabled == 1)
    else:
        mkl_enabled = tf.pywrap_tensorflow.IsMklEnabled()
    return mkl_enabled, onednn_enabled


print("We are using Tensorflow version", tf.__version__)
print("MKL enabled:", get_mkl_enabled_flag())
