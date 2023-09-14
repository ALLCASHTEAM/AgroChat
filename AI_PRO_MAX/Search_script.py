import spacy


class Search:
    def __init__(self, mass: list[str]):
        """
        --- ЭТО ИНИТ ---
        !! ОН ВЫПОЛНЯЕТСЯ ПРИ ОБЪЯВЛЕНИИ КЛАССА И НИЧЕГО НЕ ВОЗРАЩАЕТ !!
        Получает массив данных
        *В массивах строки*
        """
        self.nlp = spacy.load("ru_core_news_lg")
        self.value_mass = list(map(lambda x: self.text_to_lemma(x)[0], mass))

    def text_to_lemma(self, message: str):
        """
        Превращение сообщения в лемму
        Подается текст и возращается массив
        """

        doc = self.nlp(f"{message}")
        return [token.lemma_ for token in doc]

    def search(self, massage: list) -> set[str]:
        """
        --- ЭТО ПОИСК ВСЕХ ВХОЖДЕНИЙ ПРОДУКТА ---
        Функция ищет все вхождения строку
        Принемает сроку сообщения
        Возвращает set с массивом, в массиве строки
        """
        context_product = []
        for item in self.text_to_lemma(massage):
            if self.value_mass.__contains__(item):
                context_product.append(item)
        return set(context_product)

    def search_gen(self, massage: str) -> set[str]:
        """
        --- ЭТО ПОИСК ПРОДУКТА (ГЕНЕРАТОР) ---
        Функция ищет все вхождения в строку
        Принемает сроку сообщения
        Возвращает по строчно
        !!! ЭТО ГЕНИРАТОР !!!
        """

        for item in self.text_to_lemma(massage):
            if self.value_mass.__contains__(self.text_to_lemma(item)):
                yield item
