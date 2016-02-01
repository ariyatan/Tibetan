#! /usr/bin/env python
# -*- coding: utf-8 -*-


import csv
from syllable import gsyllables
import os

def tibetan_to_wylie(tibetan):
    #takes raw tibetan text in utf-8 and returns it in form of string (or list)
    transliteration_dict = {}
    with open(os.path.dirname(__file__) + os.sep + 'Tibetan_Wylie_no_vowel.csv', 'rb') as table:
        table_reader = csv.reader(table, delimiter=',', quotechar='"')
        for line in table_reader:
            key = line[0].decode('unicode-escape')
            try:
                transliteration_dict[key] = (line[1], line[2])
                #line[1] contains transliteration, line[2] contains type an can be: 1 - regular, 3 -subjoined, 4-subjoined r, y, w, 5 - vowel
            except IndexError:
                transliteration_dict[key] = line[1]


    stoplist = [u'\xa0', u'\u0f0b', u'\u0f01\u0f14', u'\u0f04', u'\u0f05', u'\u0f07', u'\u0f08', u'\u0f0d', u'\u0f0e', u'\u0f14', u'\u0f20', u'\u0f21', u'\u0f22', u'\u0f23', u'\u0f24', u'\u0f25', u'\u0f26', u'\u0f27', u'\u0f28', u'\u0f29']
    translit = []

    for syllable in gsyllables(tibetan):

        if syllable in stoplist and syllable in transliteration_dict.keys():
            #punctuation marks, digitals and other separate tokens
            if syllable in [u'\u0f20', u'\u0f21', u'\u0f22', u'\u0f23', u'\u0f24', u'\u0f25', u'\u0f26', u'\u0f27', u'\u0f28', u'\u0f29'] and len(translit) != 0 and translit[-1] == u'\xa0':
                translit[-1] = '_'
                translit.append(transliteration_dict[syllable][0])
            else:
                translit.append(transliteration_dict[syllable][0])
        elif len(syllable) == 1 and syllable in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, '<', '>', '[', ']', '/', '(', ')', '"']:
            translit.append(syllable)
        elif syllable == u'\xa0' and translit[-1] in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]:
            translit.append(' ')
        elif syllable in stoplist and not syllable in transliteration_dict.keys():
            translit.append(syllable.encode('utf-8)'))
        elif syllable == '':
            pass
        else:
            root = 0        #number of letter after which to place "a" if there is no vowel sign
            vowel_list = [] #list to count vowels if any
            counter = 0     #number of current letter
            templist = []   #list of wylie transliterations of each Tibetan glyph in order of appearance
            for item in syllable:

                tibetan_vowels = [u'\u0f72', u'\u0f74', u'\u0f7a', u'\u0f7c', u'\u0f71', u'\u0f73', u'\u0f75', u'\u0f76', u'\u0f77', u'\u0f78', u'\u0f79', u'\u0f7b', u'\u0f7d', u'\u0f80']
                if item in transliteration_dict.keys():
                    #some special cases
                    if item in tibetan_vowels:
                        if item in [u'\u0f72', u'\u0f74'] and templist[-1] == 'A':
                            long_vowels_dict = {u'\u0f72': 'I', u'\u0f74':'U'}
                            templist[-1] = long_vowels_dict[item]
                            vowel_list[-1] = long_vowels_dict[item]
                        elif templist[-1] == 'a':
                            templist[-1] = transliteration_dict[item][0]
                            vowel_list.append(transliteration_dict[item][0])
                        else:
                            vowel_list.append(transliteration_dict[item][0])
                            templist.append(transliteration_dict[item][0])
                        #vowel mark is present in Tibetan syllable and added to transliteration directly without further a-do

                    elif transliteration_dict[item][1] == str(3):
                        #only vowel can follow a subjoined consonant
                        root = counter
                        templist.append(transliteration_dict[item][0])
                    elif item == u'\u0f39':
                        #Tibetan compound transcription of Chinese sounds
                        if templist[-1] == u'ph':
                            templist[-1] = 'f'
                        elif templist[-1] == u'b':
                            templist[-1] = 'v'
                    elif item == u'\u0f60' and len(vowel_list) == 0 and len(templist) != 0:
                        #a chung
                        vowel_list.append('a')
                        templist.append('a')
                        templist.append(transliteration_dict[item][0])

                    else:
                        templist.append(transliteration_dict[item][0])
                else:
                    if item == u'\xa0':
                        pass
                    else:
                        templist.append(item)
                counter += 1


            is_word = True
            length = 0
            for item in templist:
                if item in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, '<', '>', '[', ']', '/', '(', ')', '"']:
                    length += 1
            if length == len(templist):
                is_word = False

            if is_word:
                temp = templist
                #temp is representation of syllable without tshegs used to count position of vowel ('root' of syllable)
                if templist[-1] == ' ':
                    temp = templist[:-1]

                syll_length = len(temp)
                if syll_length == 1:
                    #one tibetan letter
                    root = 0
                elif syll_length == 2 and temp[0] == temp[1]:
                    root = 0
                    #if two same letters, vowel is inserted after the first one
                elif temp[0] == 'g' and temp[1] == 'y':
                    if syllable[1] == u'\u0f61':
                        templist[1] = '.y'
                        root = 1
                    #rare case when ya is not subjoined (usually after 'g' letter 'ya' is in subjoined form)
                elif len(vowel_list) == 0 and root == 0 and templist[0] in ['b', "'", 'd', 'm', 'g']:

                    postglyphs = ['s', 'g', 'l', 'd', 'ng', 'n', 'r', 'm', 'b']
                    #consonants that may close a syllable
                    if temp[1] in postglyphs and syll_length == 2:
                        root = 0
                    elif syll_length >= 3 and temp[-1] == 's' and temp[-2] in ['g', 'ng', 'm', 'b']:
                        root = syll_length - 3
                        #second affix 's'
                    elif syll_length >= 3 and temp[-1] == 'd' and temp[-2] in ['r', 'n', 'l']:
                        root = syll_length - 3
                        #second affix 'd'
                    elif temp[-1] in postglyphs:
                        root = syll_length - 2
                    else:
                        root = 1

                if len(vowel_list) == 0 and len(templist) > 0 and templist[root] != 'a':
                    templist.insert(root + 1, 'a')


            wylie = ''.join(templist)
            translit.append(wylie)
    return ''.join(translit)    #uncomment to return transliteration as a single string
    #return translit    #uncomment to receive list, not string

def wylie_to_tibetan(transliteration):
    #takes Wylie transliteration in utf-8 as input text and returns tibetan unicode in form of string (or list)
    transliteration_dict = {}
    with open(os.path.dirname(__file__) + os.sep + 'Tibetan_Wylie_no_vowel.csv', 'rb') as table:
        table_reader = csv.reader(table, delimiter=',', quotechar='"')
        for line in table_reader:
            key = (line[1], line[2])
            transliteration_dict[key] = line[0].decode('unicode-escape')
        extra = {(u'_', str(1)): u'\xa0',
                (u'.y', str(1)): u'\u0f61',
                (u'.r', str(1)): u'\u0f62',
                (u'.l', str(1)): u'\u0f63',
                (u'W', str(3)): u'\u0fba',
                (u'Y', str(3)): u'\u0fbb',
                (u'R', str(3)): u'\u0fbc',
                (u'R', str(1)): u'\u0f6a',
                (u'I', str(5)): u'\u0f71\u0f72',
                (u'U', str(5)): u'\u0f71\u0f74',
                (u'.a', str(1)): u'\u0f68',
                (u'f', str(1)): u'ཕ༹',
                (u'v', str(1)): u'\u0f56\u0f39'}
        transliteration_dict.update(extra)

    tr_keys = transliteration_dict.keys()

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
            #parse transliteration:
            #distinguish initial and final parts of syllable, join compound codes
            if item in ['a', 'u', 'i', 'o',  'e', 'I', 'U', 'au', 'A', 'ai', 'M', "~M'", '~M', '?'] and to_write == 'initial':
                if index == 0:
                    tib_syllable.append(u'\u0f68')
                    to_write = 'final'
                    if item == 'a':
                        pass

                    else:
                        final.append(item)
                else:
                    to_write = 'final'
                    final.append(item)

            else:
                if to_write == 'initial':
                    if len(initial) > 0:
                        if initial[-1] == '+':
                            initial[-1] = ''.join(['+', item])
                        elif item == '-':
                            v = initial.pop(-1)
                            final.append(''.join([v, '-']))
                            to_write = 'final'
                        elif item == '/' and initial[-1] == '/':
                            initial[-1] = '//'
                        else:
                            symbols = {('/', '/'): '//', ('k','h'): 'kh', ('p','h'): 'ph', ('c','h'): 'ch',
                                       ('n','g'): 'ng', ('t', 'h'): 'th', ('ts', 'h'): 'tsh', ('z', 'h'):'zh',
                                       ('s', 'h'): 'sh', ('S', 'h'): 'Sh', ('+S', 'h'): '+Sh', ('T', 'h'): 'Th',
                                       ('.', 'y'): '.y', ('.', 'l'): '.l', ('.', 'r'): '.r', ('t', 's'): 'ts', ('n', 'y'): 'ny'}
                            key = (initial[-1], item)
                            try:
                                initial[-1] = symbols[key]
                            except KeyError:
                                initial.append(item)
                    else:
                        initial.append(item)
                else:
                    if len(final) >= 1:
                        compound = {('/', '/'): '//', ('k','h'): 'kh', ('p','h'): 'ph', ('c','h'): 'ch', ('n','g'): 'ng',
                                    ('t', 'h'): 'th', ('ts', 'h'): 'tsh', ('z', 'h'):'zh', ('s', 'h'): 'sh',
                                    ('S', 'h'): 'Sh', ('+S', 'h'): '+Sh', ('T', 'h'): 'Th', ('.', 'y'): '.y',
                                    ('.', 'l'): '.l', ('.', 'r'): '.r', ('t', 's'): 'ts', ('n', 'y'): 'ny',
                            ('a', 'i'): 'ai', ('a', 'u'): 'au', ('l-', 'i'): 'l-i' , ('r-', 'i'): 'r-i',
                            ('l-', 'I'): 'l-I' , ('r-', 'I'): 'r-I' , ('.', 'a'): '.a', ('-', 'r'): '-r', ('-', 'l'): '-l',
                            ('~', 'M'): '~M', ("'", '~M'): '~M'}
                        compound_keys = compound.keys()
                        key = (final[-1], item)
                        try:
                            final[-1] = compound[key]
                        except KeyError:
                            if final[-1] == '+':
                                final[-1] = ''.join(['+', item])
                            else:
                                final.append(item)
                    else:
                        final.append(item)
            index += 1

        if len(initial) == 1 and (initial[0], str(1)) in tr_keys:
            tib_syllable.append(transliteration_dict[(initial[0], str(1))])
        else:
            for item in initial:
                ind = initial.index(item)
                root_length = len(initial)
                if item == ' ':
                    if tib_syllable[-1] in [u'\u0f04', u'\u0f05', u'\u0f06', u'\u0f07', u'\u0f08', u'\u0f0b', u'\u0f0c', u'\u0f0d', u'\u0f0e', u'\u0f0f', u'\u0f11', u'\u0f14']:
                        tib_syllable.append(u' ')
                    else:
                        tib_syllable.append(u'\u0f0b')
                elif item in ['b', "'", 'd', 'm', 'g'] and ind == 0:
                    tib_syllable.append(transliteration_dict[(item, str(1))])
                elif item[0] == '+':
                    tib_syllable.append(transliteration_dict[(item[1:], str(3))])
                elif ind > 0 and initial[ind - 1] in ['r', 'l', 's']:
                    tib_syllable.append(transliteration_dict[(item, str(3))])
                elif item == 'l' and ind == root_length - 1 and ind >=1 and initial[ind-1] in ['k', 'g', 'b', 'z','r', 's']:
                    tib_syllable.append(u'\u0fb3')
                elif item == 'y' and (ind == root_length - 1 or (ind == root_length - 2 and initial[-1] == 'w')) and ind >=1 and initial[ind-1] in ['k', 'g', 'kh', 'p', 'ph', 'b', 'm', 'h']:
                     tib_syllable.append(u'\u0fb1')
                elif item == 'r' and (ind == root_length - 1 or (ind == root_length - 2 and initial[-1]in  ['y', 'w'])) and ind >=1 and initial[ind-1] in ['k', 'g', 'kh', 't', 'th', 'd', 'n', 'p','ph', 'b', 'm', 's','h']:
                     tib_syllable.append(u'\u0fb2')
                elif item in ['w', "'"] and ind > 0 and ind == root_length - 1:
                    tib_syllable.append(transliteration_dict[(item, str(3))])
                else:
                    key = (item, str(1))
                    if key in tr_keys:
                        tib_syllable.append(transliteration_dict[key])
                    else:
                        tib_syllable.append(item)

        for item in final:
            if item in ['u', 'i', 'o',  'e', 'I', 'U', 'au', 'A', 'ai', 'M', "~M'", '~M', '?', 'r-i', 'l-i', 'r-I', 'l-I']:
                tib_syllable.append(transliteration_dict[(item, str(5))])
            elif item == 'a':
                pass
            elif item[0] == '+':
                    tib_syllable.append(transliteration_dict[(item[1:], str(3))])
            else:
                tib_syllable.append(transliteration_dict[(item, str(1))])

        bod_skad.append(''.join(tib_syllable))

    return ''.join(bod_skad) #uncomment to return string
    #return bod_skad   #uncomment to return list






