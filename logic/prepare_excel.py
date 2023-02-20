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
    a = ' + '.join(mask.split()) + ' + ' + key
    return a.title()

def start(clustered_words, mask):
    print(mask)
    res = [['Номер группы', 'Название группы', 'Фраза', "Соответствие"]]
    index = 0
    anothers = clustered_words['Остальное']
    phrases = []
    for key in clustered_words.keys():
        if key == 'Остальное':
            pass
        elif key != 'Остальное' and len(clustered_words[key]) == 1:
            if clustered_words[key][0] not in phrases:
                anothers.append(clustered_words[key][0])
                phrases.append(clustered_words[key][0])
        else:
            index += 1
            for phrase in clustered_words[key]:
                if phrase not in phrases:
                    phrases.append(phrase)
                    res.append([index, f"{get_repeated_words(clustered_words[key], phrase, key, mask)}", phrase, key])
    for phrase in anothers:
        if phrase not in phrases:
            res.append([index + 1, f"{get_repeated_words(clustered_words['Остальное'], phrase, 'Остальное', mask)}", phrase,
                    'Остальное'])
    print(res)
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
