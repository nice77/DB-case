# транслитератор с немецкого на русский
def de_to_ru(inp_word):
    word = inp_word[:]
    word = word.lower()

    main_letters = {'b': 'б', 'n': 'н', 't': 'т',
                    'd': 'д', 'p': 'п', 'w': 'в',
                    'f': 'ф', 'q': 'к', 'x': 'кс',
                    'g': 'г', 'r': 'р', 'y': 'и',
                    'm': 'м', 'ß': 'с', 'z': 'ц', 'k': 'к'}

    double_letters = {'zsch': 'ч', 'tsch': 'ч', 'chs': 'кс',  'sch': 'ш', 'chh': 'хг',
                      'ch': 'х', 'ph': 'ф', 'rh': 'р', 'th': 'т', 'gk': 'г'}

    all_vowels_j = {'a': 'я', 'e': 'е', 'o': 'йо', 'u': 'ю', 'ä': 'е', 'ö': 'йё', 'ü': 'йю'}
    all_vowels = {'a', 'e', 'i', 'o', 'u', 'ä', 'ö', 'ü'}
    vowels_tr = {'a': 'а', 'e': 'е', 'i': 'и', 'o': 'о', 'u': 'у', 'ä': 'е', 'ö': 'ё', 'ü': 'ю'}
    front_vowels = {'i', 'e', 'y'}

    new_word = ''

    for i in double_letters.keys():
        word = word.replace(i, double_letters[i])

    to_skip = False
    for i, elem in enumerate(word):
        added = False
        if to_skip:
            to_skip = False
            continue

        # Разбираем правила с буквой j
        if elem == 'j':

            # Стоит в начале слова в сочетании с гласной, кроме 'i'
            if i == 0 and i + 1 < len(word):
                if word[i + 1] in all_vowels and word[i + 1] != 'i':
                    new_word += all_vowels_j[word[i + 1]]
                    to_skip = True

            # Стоит в середине слова
            elif i + 1 < len(word) and i - 1 >= 0:
                # Стоит в сочетании
                if word[i + 1] in all_vowels and word[i + 1] != 'i':
                    # Стоит после гласной
                    if word[i - 1] in all_vowels:
                        new_word += all_vowels_j[word[i + 1]]
                    # Стоит после согласной
                    else:
                        if word[i + 1] in ('o', 'ö'):
                            new_word += 'ь' + all_vowels_j[word[i + 1]][1]
                        elif word[i + 1] in ('u', 'ü'):
                            new_word += 'ью'
                        else:
                            new_word += 'ь' + all_vowels_j[word[i + 1]]
                    to_skip = True
                # Стоит не в сочетании
                else:
                    if word[i + 1] not in all_vowels:
                        new_word += 'й'

        # Разбиарем сочетания гласных
        elif elem == 'e':
            if i + 1 < len(word):
                if word[i + 1] == 'u':
                    new_word += 'ой'
                    to_skip = True
                elif word[i + 1] == 'i':
                    new_word += 'ай'
                    to_skip = True
                else:
                    new_word += 'е'
                added = True
            if not added and i - 1 > 0:
                if word[i - 1] in all_vowels:
                    new_word += 'э'
            if not added:
                new_word += 'е'

        elif elem == 'i':
            if i + 1 < len(word):
                if word[i + 1] == 'e':
                    new_word += 'и'
                    to_skip = True
                else:
                    new_word += 'и'
                added = True
            if not added and i - 1 > 0:
                if word[i - 1] in all_vowels:
                    new_word += 'й'
                    added = True
            if not added:
                new_word += 'и'

        elif elem == 'ä':
            if i - 1 > 0:
                if word[i - 1] in all_vowels:
                    new_word += 'э'

        # Разбираемся с гласными переднего ряда и буквой 'c'
        elif elem == 'c':
            if i + 1 < len(word):
                if word[i + 1] in front_vowels:
                    new_word += 'ц'
                elif word[i + 1] == 'k':
                    if i + 2 < len(word) and i - 1 >= 0:
                        if word[i + 2] in all_vowels and word[i - 1] in all_vowels:
                            new_word += 'кк'
                        else:
                            new_word += 'к'
                    else:
                        new_word += 'к'
                    to_skip = True
                else:
                    new_word += 'к'
            else:
                new_word += 'к'

        # Разбираемся с буквой 's'
        elif elem == 's':
            if i + 1 < len(word):
                if word[i + 1] in all_vowels:
                    new_word += 'з'
                else:
                    new_word += 'с'

        # Разбираемся с согласной 'h'
        elif elem == 'h':
            if i - 1 >= 0 and i + 1 < len(word):
                if word[i - 1] in all_vowels and word[i + 1] not in all_vowels:
                    new_word += ''
                elif word[i - 1] in all_vowels and word[i + 1] == 'e':
                    new_word += ''
                else:
                    new_word += 'х'
            else:
                new_word += 'х'

        # Разбираемся с согласной 'l'
        elif elem == 'l':
            if i + 1 < len(word):
                if word[i + 1] == elem:
                    if i + 2 < len(word):   # Удвоенная 'l'
                        if word[i + 2] not in all_vowels:   # После 'll' стоит согласная => + 'лль'
                            new_word += 'лль'
                        else:   # Проверка, стоит ли между гласными 'll'
                            if i - 1 >= 0:
                                if word[i - 1] in all_vowels:
                                    new_word += 'лл'
                                else:
                                    new_word += 'л'
                    else:
                        new_word += 'лль'
                    to_skip = True
                else:
                    if word[i + 1] in all_vowels:
                        new_word += 'л'
                    else:
                        new_word += 'ль'
            else:
                new_word += 'ль'

        elif elem == 's':
            if i + 1 < len(word):
                if word[i + 1] in ('p', 't', 'ф', 'ц'):
                    new_word += 'ш'
                    added = True
                elif word[i + 1] in all_vowels:
                    new_word += 'з'
                else:
                    if word[i + 1] not in ('p', 't', 'ф', 'ц'):
                        new_word += 'с'
            if i == 0 and not added:
                new_word += 'ш'

        elif elem == 't':
            if i + 1 < len(word):
                if word[i + 1] == 'z':
                    if i + 2 < len(word) and i - 1 >= 0:
                        if word[i + 2] in all_vowels and word[i - 1] in all_vowels:
                            new_word += 'тц'
                        else:
                            new_word += 'ц'
                    else:
                        new_word += 'ц'
                    to_skip = True
                else:
                    new_word += 'т'
            else:
                new_word += 'т'

        elif elem in all_vowels:
            new_word += vowels_tr[elem]
            if i + 1 < len(word):
                if word[i + 1] == elem:
                    new_word += vowels_tr[elem]
                    to_skip = True

        else:
            if elem in main_letters.keys():
                new_word += main_letters[elem]
                if i + 1 < len(word):
                    if word[i + 1] == elem:
                        if i - 1 >= 0 and i + 2 < len(word):
                            if word[i - 1] in all_vowels and word[i + 2] in all_vowels:
                                new_word += main_letters[elem]
                            to_skip = True

            else:
                new_word += elem

    return new_word
