# транслитератор с польского на русский
def pl_to_ru(inp_word):

    # чтобы не изменять входящее слово
    word = inp_word[:]
    word = word.lower()

    # словари и множества для проверок и изменений слова
    pl_ru = {'b': 'б', 'c': 'ц', 'd': 'д', 'f': 'ф', 'g': 'г', 'h': 'х',
             'k': 'к', 'ł': 'л', 'm': 'м', 'n': 'н', 'p': 'п', 'r': 'р',
             's': 'с', 't': 'т', 'w': 'в', 'z': 'з', 'u': 'у', 'l': 'л',
             'ć': 'ць', 'i': 'и', 'ż': 'ж', 'ó': 'у', 'a': 'а', 'e': 'е',
             'o': 'о', 'v': 'в'}

    pl_ru_d = {'szcz': 'щ', 'ch': 'х', 'cz': 'ч', 'dz': 'дз', 'dż': 'дж', 'sz': 'ш'}

    all_vowels = {'i', 'e', 'y', 'a', 'u', 'ó', 'o', 'ę', 'ą',
                  'а', 'о', 'э', 'е', 'и', 'ы', 'у', 'ё', 'ю', 'я'}

    after_j = {'a': 'я', 'e': 'е', 'o': 'ё', 'ó': 'ю', 'u': 'ю'}
    all_consonants_sibilant = {'ч', 'rz', 'ш', 'ж', 'щ'}
    all_consonants_deaf = {'х', 'k', 'p', 't', 'ц', 'п'}
    hard_consonants = {'dź': 'дз', 'ś': 'с', 'ź': 'з'}
    spec = {'ć', 'l', 'ń', 'ś', 'dź'}

    # разбираем начало слова
    if len(word) > 1:
        if word[0] == 'e':
            word = 'э' + word[1:]
        elif word[0] == 'j':
            if word[1] in after_j.keys():
                if word[1] != 'o':
                    word = after_j[word[1]] + word[2:]
                else:
                    word = 'йо' + word[2:]

    # разбираем конец слова
    if word[-1] == 'l':
        word = word[:-1] + 'ль'
    elif word[-1] == 'j':
        word = word[:-1] + 'й'

    # заменяем сложные сочетания букв, которые однозначно определяются
    for i in pl_ru_d.keys():
        word = word.replace(i, pl_ru_d[i])

    # начинаем составлять новое слово, проходясь по каждому символу первого
    new_word = ''
    added = False
    to_skip = False     # параметр, работающий при сочетании букв "dz" и ему подобных
    for i, elem in enumerate(word):
        if to_skip:
            to_skip = False
            continue

        if elem == 'j':
            if word[i + 1] in after_j.keys() and not to_skip:
                if word[i - 1] in all_vowels:
                    new_word += after_j[word[i + 1]]
                else:
                    new_word += 'ь' + after_j[word[i + 1]] if word[i + 1] != 'o' else 'ьо'
                to_skip = True
            elif word[i + 1] not in after_j.keys() and not to_skip:
                new_word += 'й'

        elif elem == 'i':
            if i + 1 < len(word):
                if word[i + 1] in after_j.keys():
                    new_word += after_j[word[i + 1]]
                    to_skip = True
                else:
                    new_word += pl_ru[elem]
            else:
                new_word += pl_ru[elem]

        elif elem in ('ą', 'ę'):
            new_word += 'о' if elem == 'ą' else 'е'
            if i + 1 < len(word):
                if word[i + 1] in ('b', 'p'):
                    new_word += 'м'
                else:
                    new_word += 'н'
            else:
                new_word += 'н'

        elif elem == 'l':
            if i + 1 < len(word):
                if word[i + 1] in after_j.keys():
                    new_word += 'л' + after_j[word[i + 1]]
                    to_skip = True
                elif word[i + 1] in all_vowels:
                    new_word += pl_ru[elem]
                else:
                    new_word += 'ль'

        elif elem == 'y':
            if i - 1 > 0:
                if word[i - 1:i] in all_consonants_sibilant:
                    new_word += 'и'
                    added = True
            if i - 2 > 0 and not added:
                if word[i - 2:i] in all_consonants_sibilant:
                    new_word += 'и'
                    added = True
            if not added:
                new_word += 'ы'

        elif elem == 'r':
            if i + 1 < len(word):
                if word[i + 1] == 'z':
                    if i + 2 < len(word) and i - 1 >= 0:
                        if word[i + 2] in all_consonants_deaf or word[i - 1] in all_consonants_deaf:
                            new_word += 'ш'
                        else:
                            new_word += 'ж'
                    to_skip = True
                else:
                    new_word += pl_ru[elem]
            else:
                new_word += pl_ru[elem]
            added = False

        elif elem in hard_consonants.keys():
            if i + 2 < len(word):
                if word[i + 1] not in all_vowels and word[i + 2] == 'i':
                    new_word += hard_consonants[elem]
                elif word[i + 1] in spec:
                    new_word += hard_consonants[elem]
                else:
                    new_word += hard_consonants[elem] + 'ь'
            else:
                new_word += hard_consonants[elem] + 'ь'

        elif elem == 'd':
            if i + 3 < len(word):
                if word[i + 1] == 'ź' and word[i + 2] not in all_vowels:
                    new_word += hard_consonants[word[i:i + 2]]
                    to_skip = True
                elif word[i + 1] == 'ź' and word[i + 2] in all_vowels:
                    new_word += hard_consonants[word[i:i + 2]] + 'ь'
                    to_skip = True
                elif word[i + 1] != 'ź':
                    new_word += pl_ru[elem]
            else:
                if i + 1 < len(word):
                    if word[i + 1] == 'ź':
                        new_word += hard_consonants[word[i:i + 2]] + 'ь'
                        to_skip = True
                    else:
                        new_word += pl_ru[elem]
                else:
                    new_word += pl_ru[elem]

        else:
            if elem in pl_ru.keys():
                new_word += pl_ru[elem]
            else:
                new_word += elem

    # возвращаем новое слово
    new_word = new_word.replace('ń', 'нь')
    return new_word
