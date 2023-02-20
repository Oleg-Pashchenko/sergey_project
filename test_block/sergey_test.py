# -*- coding: utf-8 -*-
import pymorphy2


def norm(x):
    morph = pymorphy2.MorphAnalyzer()
    p = morph.parse(x)[0]
    return p.normal_form


zz = input("Введите слово: ")
print(norm(zz))