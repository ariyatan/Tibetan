#! /usr/bin/env python
# -*- coding: utf-8 -*-


import csv
from syllable import gsyllables

def wylie(tibetan):
    #takes raw tibetan text in utf-8 and returns it in form of string (or list)
    transliteration_dict = {}
    with open('Tibetan_Wylie_no_vowel.csv', 'rb') as table:
        table_reader = csv.reader(table, delimiter=',', quotechar='"')
        for line in table_reader:
            key = line[0].decode('unicode-escape')
            try:
                transliteration_dict[key] = (line[1], line[2])
            except IndexError:
                transliteration_dict[key] = line[1]

    stoplist = [u'\xa0', u'\u0f0b', u'\u0f01\u0f14', u'\u0f04', u'\u0f05', u'\u0f07', u'\u0f08', u'\u0f0d', u'\u0f0e', u'\u0f14', u'\u0f20', u'\u0f21', u'\u0f22', u'\u0f23', u'\u0f24', u'\u0f25', u'\u0f26', u'\u0f27', u'\u0f28', u'\u0f29']
    translit = []

    for syllable in gsyllables(tibetan):

        if syllable in stoplist and syllable in transliteration_dict.keys():
            #punctuation marks, digitals and other separate tokens
            if syllable in [u'\u0f20', u'\u0f21', u'\u0f22', u'\u0f23', u'\u0f24', u'\u0f25', u'\u0f26', u'\u0f27', u'\u0f28', u'\u0f29'] and translit[-1] == u'\xa0':
                translit[-1] = '_'
                translit.append(transliteration_dict[syllable][0])
            else:
                translit.append(transliteration_dict[syllable][0])
        elif syllable == u'\xa0' and translit[-1] in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]:
            translit.append(' ')
        elif syllable in stoplist and not syllable in transliteration_dict.keys():
            translit.append(syllable.encode('utf-8)'))
        elif syllable == '':
            pass
        else:
            root = 0
            vowel_list = []
            counter = 0
            templist = []
            for item in syllable:
                if item in transliteration_dict.keys():
                    if transliteration_dict[item][1] == str(5):
                        vowel_list.append(transliteration_dict[item][0])
                        templist.append(transliteration_dict[item][0])
                    elif transliteration_dict[item][1] == str(3):
                        root = counter
                        templist.append(transliteration_dict[item][0])
                    elif transliteration_dict[item][1] == str(4):
                        root = counter
                        templist.append(transliteration_dict[item][0])
                    elif transliteration_dict[item][0] == "'" and len(vowel_list) == 0 and len(templist) != 0:
                        vowel_list.append('a')
                        templist.append('a')
                        templist.append(transliteration_dict[item][0])
                    else:
                        templist.append(transliteration_dict[item][0])
                else:
                    if item == u'\xa0':
                        pass
                    else:
                        templist.append(transliteration_dict[item][0])
                counter += 1

            syll_length = len(templist)
            if syll_length == 1:
                root = 0
            elif syll_length == 2 and templist[1] == ' ':
                root = 0
            elif templist[0] == 'g' and templist[1] == 'y':
                if syllable[1] == u'\u0f61':
                    templist[1] = '.y'
                    root = 1
            elif syll_length > 1 and len(vowel_list) == 0 and root == 0 and templist[0] in ['b', "'", 'd', 'm', 'g']:
                postglyphs = ['s', 'g', 'l', 'd', 'ng', 'n', 'r', 'm', 'b']
                if templist[0] == templist[1]:
                    root = 0
                elif templist[1] in postglyphs and syll_length == 2:
                    root = 0
                elif templist[1] in postglyphs and syll_length == 3 and templist[2] == ' ':
                    root = 0
                elif syll_length < 3 and templist[2] == 's' and templist[1] in ['g', 'ng', 'm', 'b']:
                    root = 0
                else:
                    root = 1

            if len(vowel_list) == 0 and len(templist) > 0 and templist[root] != 'a':
                templist.insert(root + 1, 'a')


            wylie = ''.join(templist)
            translit.append(wylie)
    return ''.join(translit)    #uncomment to return transliteration as a single string
    #return translit    #uncomment to receive list, not string

def tibetan(transliteration):
    #takes Wylie transliteration in utf-8 as input text and returns tibetan unicode in form of string (or list)
    transliteration_dict = {}
    with open('Tibetan_Wylie_no_vowel.csv', 'rb') as table:
        table_reader = csv.reader(table, delimiter=',', quotechar='"')
        for line in table_reader:
            try:
                key = (line[1], line[2])
            except IndexError:
                key = line[1]
            transliteration_dict[key] = line[0].decode('unicode-escape')
        transliteration_dict[(u'_', str(1))] = u'\xa0'
        transliteration_dict[(u'.y', str(1))] = u'\u0f61'
        transliteration_dict[(u'.r', str(1))] = u'\u0f62'
        transliteration_dict[(u'.l', str(1))] = u'\u0f63'

    def return_seq(source):
        u_source = source.encode('utf-8')
        countdown = len(u_source)
        new_seq = []
        for item in u_source:
            countdown -= 1
            if item in [' ', '_']:
                new_seq.append(item)
                yield new_seq
                new_seq = []
            else:
                if countdown == 0:
                    new_seq.append(item)
                    yield new_seq
                else:
                    new_seq.append(item)

    bod_skad = []
    for seq in return_seq(transliteration):
        tib_syllable = [] #tibetan unicode
        initial = [] #transliteration, everything before first vowel is added here
        final = [] #transliteration: vowel and closing consonants if any
        index = 0
        to_write = 'initial'
        for item in seq:
            if item in ['a', 'A', 'u', 'U', 'o', 'au', 'i', 'ai', 'o', 'e']:
                if index == 0:
                    tib_syllable.append(u'\u0f68')
                else:
                    to_write = 'final'
                    if item == 'a':
                        pass
                    else:
                        final.append(item)
            else:
                if to_write == 'initial':
                    if len(initial) > 0:
                        if item == 'h' and initial[-1] in ['k', 'p', 'c', 't', 'ts', 'z', 's']:
                            initial[-1] = ''.join([initial[-1], 'h'])
                        elif item == 's' and initial[-1] == 't':
                            initial[-1] = 'ts'
                        elif item == 'y' and initial[-1] == 'n':
                            initial[-1] = 'ny'
                        elif item == 'z' and initial[-1] == 'd':
                            initial[-1] = 'dz'
                        elif item == 'y' and initial[-1] == '.':
                            initial[-1] = '.y'
                        elif item == 'r' and initial[-1] == '.':
                            initial[-1] = '.r'
                        elif item == 'l' and initial[-1] == '.':
                            initial[-1] = '.l'
                        elif item == 'g' and initial[-1] == 'n':
                            initial[-1] = 'ng'
                        else:
                            initial.append(item)
                    else:
                        initial.append(item)
                else:
                    if len(final) >= 1:
                        if item == 'g' and final[-1] == 'n':
                            final[-1] = 'ng'
                        else:
                            final.append(item)
                    else:
                        final.append(item)
            index += 1

        if len(initial) == 1:
            tib_syllable.append(transliteration_dict[(initial[0], str(1))])
        else:
            for item in initial:
                if item in ['b', "'", 'd', 'm', 'g'] and initial.index(item) == 0:
                    tib_syllable.append(transliteration_dict[(item, str(1))])
                elif item in['|', '/']:
                    tib_syllable.append(u'། ')
                elif initial.index(item) > 0 and initial[initial.index(item) - 1] in ['r', 'l', 's']:
                    tib_syllable.append(transliteration_dict[(item, str(3))])
                elif item in ['r', 'l', 'y', 'w', 'sh', "'"] and initial.index(item) == len(initial) - 1:
                    tib_syllable.append(transliteration_dict[(item, str(4))])
                else:
                    tib_syllable.append(transliteration_dict[(item, str(1))])

        for item in final:
            if item in ['u', 'U', 'o', 'au', 'i', 'ai', 'o', 'e']:
                tib_syllable.append(transliteration_dict[(item, str(5))])
            else:
                tib_syllable.append(transliteration_dict[(item, str(1))])

        bod_skad.append(''.join(tib_syllable))

    return ''.join(bod_skad) #uncomment to return string
    #return bod_skad   #uncomment to return list
