# -*- coding: utf-8 -*-
from syllable import syllables

def tokenize_tib_string(input, vocabulary):
    '''The function 'tokenize_tib_string' takes a lexicon and a tibetan text in form of utf8-encoded string,
    and returns it as a list of separate tokens. Vocabulary is simple list (or better, frozenset - it's hashable and fast).
    Entries of vocabulary should have no tshegs on end, or at least any item should have its 'tsheg-less' form'''
    
    text = input.decode('utf-8-sig')
    
    #parsing to searcheable elements    
    parsed = syllables(text)
    clean = []
    for item in parsed:
        if item == u'\u0f0b':
            clean.append(item)
        elif len(item) > 3 and item[-3:] in [u'འི\u0f0b', u'འོ\u0f0b']:
            clean. extend([item[:-3], item[-3:]])
        elif len(item) > 2 and item[-2:] in [u'འི', u'འོ']:
            clean.extend([item[:-2], item[-2:]])

        elif item == u'\xa0':
            pass
        elif len(item) > 2 and item[-2:] in [u'\u0f62\u0f0b', u'\u0f66\u0f0b']:
            clean.extend([item[:-2], item[-2:], u'*'])
        elif len(item) > 1 and item[-1] in [u'\u0f62', u'\u0f66']:
            clean.extend([item[:-1], item[-1:], u'*'])

        else:
            clean.append(item)

    tokenized_text = []
    counter = 0
    morpheme_dict = {u'\u0f62': u'རུ', u'\u0f66': u'ཡིས'} #dict of morphemes that can be represented in text in short form

    def search(sintagm, tokenized):

        #place to insert rules - base cases to stop recursion
        possible_word = ''.join([a for a in sintagm if a != u'*']).strip(u'\u0f0b')
        if sintagm[0] == u"འི\u0f0b":
            tokenized.append(sintagm[0].strip(u'\u0f0b'))
            return 1
        elif len(sintagm) > 1 and sintagm[1] == u'*':
            #special artificial items followed by marker '*'
            tokenized.append(morpheme_dict[sintagm[0].strip(u'\u0f0b')])
            return 2
        elif sintagm[0] == u'*':
            #pass the marker
            return 1
        elif possible_word in vocabulary:
            #if possible word of any length is found in reference vocabulary, it is added to list of tokens
            tokenized.append(possible_word)
            l = len(sintagm)
            return l
        elif len(sintagm) == 1 and possible_word not in vocabulary:
            #if possible word of any length not found in reference vocabulary, the first syllable is added to list of tokens
            tokenized.append(possible_word)
            return 1

        elif len(sintagm) == 3 and possible_word[-3:] in [u'\u0f0b\u0f54\u0f62',  u'\u0f0b\u0f56\u0f62', u'\u0f0b\u0f54\u0f66', u'\u0f0b\u0f56\u0f66', u'\u0f0b\u0f53\u0f66']:
            #2-item grammar affixes (ending in 's' or 'r')
            #comment this condition out to separate these affixes from preceeding word
            tokenized.append(possible_word)
            return 3
        elif len(sintagm) == 2 and sintagm[1].strip(u'\u0f0b') in [u'\u0f54', u'\u0f56', u'\u0f40\u0fb1\u0f44', u'\u0f61\u0f44', u'\u0f60\u0f44', u'\u0f66\u0f9f\u0f7a', u'\u0f4f\u0f7a', u'\u0f5e\u0f72\u0f44', u'\u0f45\u0f72\u0f44', u'\u0f64\u0f72\u0f44', u'\u0f64\u0f72\u0f42', u'\u0f5e\u0f72\u0f42', u'\u0f45\u0f72\u0f42']: #and lexicon[sintagm[0]][1] == 'V' or lexicon[sintagm[0]][1] == 'N ~ V':
            #nominalized verbs and grammar particles such as shig (one list item each, not ending in 'r' or 's')
            ##comment this condition out to separate these affixes from preceeding word
            tokenized.append(possible_word)
            return 2

        else:
            #recursion
            return search(sintagm[:-1], tokenized)

    length = len(clean)
    if length <= 40:
        while counter < length:
            counter += search(clean[counter:], tokenized_text)
    else:
        def resample(long):
            '''Resample is a help generator function that divides too long sequences into smaller ones'''
            separators = [u'\u0f0d', u'\u0f0e', u'\u0f08', u'\u0f0f', u'\u0f11', u'\u0f14'] #symbols that can separate sequences, shads by default
            new = []
            for value in long:
                if value in separators:
                    new.append(value)
                    yield new
                    new = []
                else:
                    new.append(value)
        for sentence in resample(clean):
            counter = 0
            short = len(sentence)
            while counter < short:
                counter += search(sentence[counter:], tokenized_text)

    return tokenized_text