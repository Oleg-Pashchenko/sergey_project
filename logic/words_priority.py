import pymorphy2

morph = pymorphy2.MorphAnalyzer()


def remove_prepositions(text):
    words = text.split()
    result = []
    for word in words:
        parsed_word = morph.parse(word)[0]
        if 'PREP' not in parsed_word.tag:
            result.append(parsed_word.normal_form)
    return ' '.join(result)


def delete_mask_words(arr, mask):
    for word in mask.split():
        p = morph.parse(word)[0].normal_form
        if p in arr:
            arr.remove(p)
    return arr


def delete_prepositions(arr):
    res = []
    for word in arr:
        p = morph.parse(word)[0]
        if 'PREP' in p.tag:
            pass
        else:
            res.append(word)
    return res


def get_repeated_words(phrases, mask):
    words = {}
    for phrase in phrases:
        phrase = remove_prepositions(phrase)
        s = set()
        for word in phrase.split():
            p = morph.parse(word)[0].normal_form
            s.add(p)
        for i in s:
            if i in words:
                words[i] += 1
            else:
                words[i] = 1
    to_view = []
    for key in words.keys():
        if words[key] > 1:
            to_view.append(key)
    to_view = delete_mask_words(to_view, mask)
    to_view = delete_prepositions(to_view)
    return to_view


def clusterize(phrase, order):
    for o in order:
        for word in phrase.split():
            p = morph.parse(word)[0].normal_form
            if p in o:
                return o

    return "Остальное"


def cluster_words(phrases, order):
    res = {"Остальное": []}
    for phrase in phrases:
        o = clusterize(phrase, order)
        if o in res.keys():
            res[o].append(phrase)
        else:
            res[o] = [phrase]

    result = {'Остальное': []}
    for key in res.keys():
        if len(res[key]) == 1:
            result['Остальное'].append(res[key][0])
        else:
            result[key] = res[key]

    if len(result['Остальное']) == 0:
        del result['Остальное']
    return res

# ph = ['потолочная люстра металлическая', 'купить потолочную люстру металлическую', 'потолочная люстра недорого',
#      'потолочная люстра недорого купить', 'купить потолочную металлическую люстру недорого']
# print(get_repeated_words(ph))
# print(cluster_words(ph, ['металлический', 'недорого']))
