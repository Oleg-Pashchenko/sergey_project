import pandas as pd
import pymorphy2

morph = pymorphy2.MorphAnalyzer()


def get_repeated_words(arr, phrase, key):
    words_arr = set()
    for i in arr:
        for j in i.split():
            if j != phrase:
                p = morph.parse(j)[0].normal_form
                words_arr.add(p)
    res = []
    for i in phrase.split():
        if i in words_arr:
            res.append(i)
    if key in res:
        res.remove(key)
    res.append(key)
    return ' + '.join(res)


def start(clustered_words):
    res = [['Номер группы', 'Название группы', 'Фраза', "Соответствие"]]
    index = 0
    for key in clustered_words.keys():
        index += 1
        for phrase in clustered_words[key]:
            res.append([index, f"{get_repeated_words(clustered_words[key], phrase, key)}", phrase, key])
    write_file(res)


def write_file(data):
    data = pd.DataFrame(data)
    writer = pd.ExcelWriter('result.xlsx', engine='xlsxwriter')
    data.to_excel(writer, index=False, sheet_name='Sheet1')
    writer.save()

