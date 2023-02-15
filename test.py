import pymorphy2

phrases = [
    "агенство переводов в Москва"
]


import pymorphy2

morph = pymorphy2.MorphAnalyzer()

for phrase in phrases:
    parsed_word = morph.parse(phrase)[0]
    plural_word = parsed_word.make_agree_with_number(2).word
    print(plural_word)