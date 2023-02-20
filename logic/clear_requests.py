import pymorphy2

morph = pymorphy2.MorphAnalyzer()


def start(minus_phrases, phrases):
    to_delete = set()
    for phrase in phrases:
        for word_index, word in enumerate(phrase.split()):
            for minus_phrase in minus_phrases:
                if '"' == minus_phrase[0] and '"' == minus_phrase[-1] and len(minus_phrase.split()) != len(
                        phrase.split()):
                    to_delete.add(phrase)

                if '(' in minus_phrase:
                    start_index = minus_phrase.index('(')
                    end_index = minus_phrase.index(')')
                    seq_phrase = minus_phrase[start_index + 1:end_index].split('|')
                    fl = False
                    for seq_word in seq_phrase:
                        if seq_word in phrase:
                            fl = True
                    if not fl:
                        to_delete.add(phrase)

                if '[' in minus_phrase:
                    try:
                        start_index = minus_phrase.index('[')
                        end_index = minus_phrase.index(']')
                        seq_phrase = minus_phrase[start_index + 1:end_index]
                        if seq_phrase not in phrase:
                            to_delete.add(phrase)
                    except:
                        to_delete.add(phrase)

                for minus_word_index, minus_word in enumerate(minus_phrase.split()):
                    if '!' == minus_word[0] and minus_word[1::] in phrase.split():
                        to_delete.add(phrase)
                    try:
                        if '+' == minus_word[0] and phrase.split().index(minus_word[1::]) != minus_word_index:
                            print(word_index, minus_word_index)
                            print('+', phrase)
                            to_delete.add(phrase)
                    except:
                        to_delete.add(phrase)
                    if '+' not in minus_phrase and '!' not in minus_phrase and '"' not in minus_phrase \
                            and '[' not in minus_phrase and '(' not in minus_phrase:
                        p = morph.parse(word)[0].normal_form
                        if p.lower() == minus_word.lower():
                            print('!=', phrase)
                            to_delete.add(phrase)
                            break

    return list(to_delete)


def get_updated_list(phrases, to_delete):
    result = []
    for phrase in phrases:
        if phrase not in to_delete:
            result.append(phrase)

    return result

#start(['купить !собаку'], ['купить собаку', 'купить корм для собак', 'купить собак'])
#start(['купить !вазу'], ['купить вазу', 'купить ваз'])
#start(['работа +на дому'], ['работа на дому', 'работа по дому', 'работа дома'])
#start(['+если выключился компьютер'], ['если выключился компьютер', 'чтобы выключился компьютер'])
#start(['"купить автомобиль"'], ['купить автомобиль', 'автомобиль купить', 'купить красный автомобиль'])
#start(['билеты [из москвы в париж]'], ['билеты из москвы в париж', 'билеты на самолет из москвы в париж', 'билеты из парижа в москву', 'билеты москва париж', 'билеты из москвы недорого в париж'])
#print(start(['купить машину (недорого|ваз)'], ['купить машину недорого', 'купить машину ваз']))
