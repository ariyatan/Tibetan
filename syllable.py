#! /usr/bin/env python
# -*- coding: utf-8 -*-

#closing tsheg is included in syllable
u_tokens = [u'\u0f01\u0f14', u'\u0f04', u'\u0f05', u'\u0f07', u'\u0f08', u'\u0f0d', u'\u0f0e', u'\u0f14', u'\u0f20', u'\u0f21', u'\u0f22', u'\u0f23', u'\u0f24', u'\u0f25', u'\u0f26', u'\u0f27', u'\u0f28', u'\u0f29', u'\xa0']

def gsyllables(input_txt):
    '''syllable GENERATOR'''
    countdown = len(input_txt)
    new_syllable = []
    symbol = u'\u0f0b'
    #symbol = '\xe0\xbc\x8b'
    for item in input_txt:
        countdown -= 1
        if item in u_tokens:
            yield ''.join(new_syllable)
            yield item
            new_syllable = []
        elif item != symbol:
            new_syllable.append(item)
            if countdown == 0:
                yield ''.join(new_syllable)
        elif item == symbol:
            new_syllable.append(item)
            yield ''.join(new_syllable)
            new_syllable = []

def syllables(input_txt):
    '''returns syllable list'''
    countdown = len(input_txt)
    all_syllables = []
    new_syllable = []
    symbol = u'\u0f0b'
    for item in input_txt:
        countdown -= 1
        if item in u_tokens:
            all_syllables.append(''.join(new_syllable))
            new_syllable = []
            all_syllables.append(item)
        elif item != symbol:
            new_syllable.append(item)
            if countdown == 0:
                all_syllables.append(''.join(new_syllable))
        elif item == symbol:
            new_syllable.append(item)
            all_syllables.append(''.join(new_syllable))
            new_syllable = []
    return all_syllables



