import pymorphy2

from pymorphy2 import MorphAnalyzer
from pymorphy2.units.by_analogy import KnownPrefixAnalyzer, UnknownPrefixAnalyzer

morph = MorphAnalyzer()



"""
phrases = [
    "агенство переводов в Москва"
]


import pymorphy2

morph = pymorphy2.MorphAnalyzer()

for phrase in phrases:
    parsed_word = morph.parse(phrase)[0]
    plural_word = parsed_word.make_agree_with_number(2).word
    print(plural_word)
"""
"""
from natasha import MorphVocab, Doc, Segmenter
word = "придорожный"
normal_form = morph.parse(word)[0].normal_form
morph_vocab = MorphVocab()
segmenter = Segmenter()
print(normal_form)
segments = Segmenter()
segments = segments.sentenize(normal_form)
print(segments)
# получаем морфологический разбор каждой морфемы
for segment in segments:
    print(morph_vocab.parse(segment.text))
    #morph_info = morph_vocab.get(segment.text)
    #if morph_info:
        # получаем корень слова без приставки
    #    root = morph_info.normal_form
    #    print(root)
"""
"""
exit(0)
"""
source_word = "придорожн"
from nltk.stem.snowball import SnowballStemmer

stemmer = SnowballStemmer("russian")
root = stemmer.stem(source_word)
from natasha import MorphVocab, Doc, Segmenter
from natasha import (
    NewsEmbedding, NewsMorphTagger, NewsSyntaxParser, NewsNERTagger,
    PER, NamesExtractor,
    Doc
)

# загружаем встроенные модели
emb = NewsEmbedding()
morph_tagger = NewsMorphTagger(emb)
syntax_parser = NewsSyntaxParser(emb)
ner_tagger = NewsNERTagger(emb)

# создаем объект словаря для лемматизации
morph_vocab = MorphVocab()
print('Найденный корень:', root)
to_proccessing = root[:-3]
if len(to_proccessing) < 3:
    pass
to_proccessing = root[3::]
print('На обработку пошло', to_proccessing)
words = set()
for i in morph_vocab.iter_known_word_parses("бег"):
    words.add(i.normal)
for i in words:
    print(i)
exit(0)
