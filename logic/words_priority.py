import pymorphy2

morph = pymorphy2.MorphAnalyzer()


def get_repeated_words(phrases):
    words = {}
    for phrase in phrases:
        for word in phrase.split():
            p = morph.parse(word)[0].normal_form
            if p in words:
                words[p] += 1
            else:
                words[p] = 1
    to_view = []
    for key in words.keys():
        if words[key] > 1:
            to_view.append(key)
    return to_view


def clusterize(phrase, order):
    for o in order:
        for word in phrase.split():
            p = morph.parse(word)[0].normal_form
            if p in o:
                return o

    return "Underfined"


def cluster_words(phrases, order):
    res = {"Underfined": []}
    for phrase in phrases:
        o = clusterize(phrase, order)
        if o in res.keys():
            res[o].append(phrase)
        else:
            res[o] = [phrase]
    if len(res['Underfined']) == 0:
        del res['Underfined']
    return res


#ph = ['потолочная люстра металлическая', 'купить потолочную люстру металлическую', 'потолочная люстра недорого',
#      'потолочная люстра недорого купить', 'купить потолочную металлическую люстру недорого']
#print(get_repeated_words(ph))
#print(cluster_words(ph, ['металлический', 'недорого']))
