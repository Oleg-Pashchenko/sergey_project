import pandas as pd
import pymorphy2

morph = pymorphy2.MorphAnalyzer()


def get_repeated_words(arr, phrase, key, mask):
    words_arr = set()
    for i in arr:
        for j in i.split():
            if j != phrase:
                p = morph.parse(j)[0].normal_form
                words_arr.add(p)
    return mask.split()[0] + ' + ' + key
    res = []
    for i in phrase.split():
        if i in words_arr:
            res.append(i)
    if key in res:
        res.remove(key)
    res.append(key)
    return ' + '.join(res)


def start(clustered_words, mask):
    res = [['Номер группы', 'Название группы', 'Фраза', "Соответствие"]]
    index = 0
    anothers = clustered_words['Остальное']
    for key in clustered_words.keys():
        index += 1
        if key != 'Остальное' and len(clustered_words[key]) == 1:
            anothers.append(clustered_words[key][0])
        elif key != 'Остальное':
            for phrase in clustered_words[key]:
                res.append([index, f"{get_repeated_words(clustered_words[key], phrase, key, mask)}", phrase, key])
    for phrase in anothers:
        res.append([index, f"{get_repeated_words(clustered_words['Остальное'], phrase, 'Остальное', mask)}", phrase,
                    'Остальное'])

    write_file(res)


def write_file(data):
    a = {}

    for i in data[0]:
        a[i] = []

    for i in data[1::]:
        index = -1
        for j in a.keys():
            index += 1
            a[j].append(i[index])
    data = pd.DataFrame(a)
    writer = pd.ExcelWriter('result.xlsx', engine='xlsxwriter')
    data.to_excel(writer, sheet_name='Sheet1', index=False)
    writer.save()
