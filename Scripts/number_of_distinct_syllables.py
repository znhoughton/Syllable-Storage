#get number of distinct syllables used in Korean
#we can use the KAIST corpus for this
import csv
#import os
import glob
import regex
import re
from itertools import islice

def is_hangul(value):
    if regex.search(r'\p{IsHangul}', value):
        return True
    return False

def isEnglish(s):
    try:
        s.encode(encoding='utf-8').decode('ascii')
    except UnicodeDecodeError:
        return False
    else:
        return True

def syllable_count_korean():
    progress = 0
    syllables_list = set()
    corpus = glob.glob("D:/Corpora/KAIST Automatically Analyzed Corpus/**/*.txt", recursive=True)
    for file in corpus:
        with open(file, 'r', encoding = 'euc_kr', errors='ignore') as corpusfile:
            corpus_reader = csv.reader(corpusfile, delimiter = '\t', skipinitialspace=True, quotechar="\x07") #had to choose a strange quotechar so that python would ignore single and double quotes and stop escaping them                 
            for line in corpus_reader:
                try: 
                    if not isEnglish(line[0]):
                        if line[0].startswith('*') or line[0].startswith('<'):
                            continue
                        for word in line:
                            syllables_in_word = list(word)
                            for i in syllables_in_word:
                                if is_hangul(i):
                                    progress += 1
                                    syllables_list.add(i)
                except IndexError:
                        continue
    return(syllables_list)

def syllable_count_english():
    eng_syllables = set()
    with open('D:/PhD Stuff/Linguistics Stuff/Syallable Storage feat. Santiago/cmudict.rep', 'r') as corpusfile:
        corpus_reader = csv.reader(corpusfile, delimiter = '\t', skipinitialspace=True, quotechar="\x07") #had to choose a strange quotechar so that python would ignore single and double quotes and stop escaping them                 
        for line in corpus_reader:
            if line[0].startswith('#'):
                continue
            syllables = line[0].split(' ', 1)
            syllables = syllables[1:]
            syllables = syllables[0].split('-')
            for syllable in syllables:
                syllable = syllable.strip()
                eng_syllables.add(syllable)
    return eng_syllables
                
def syllable_count_korean_from_dict(): #from this dict: https://github.com/Kyubyong/pron_dictionaries
    korean_syllables = set()
    with open('D:/PhD Stuff/Linguistics Stuff/Syallable Storage feat. Santiago/ko.csv', 'r', encoding = 'utf-8', errors='ignore') as corpusfile:
        corpus_reader = csv.reader(corpusfile, delimiter = '\t', skipinitialspace=True, quotechar="\x07") #had to choose a strange quotechar so that python would ignore single and double quotes and stop escaping them                 
        nheaderlines = 37
        [next(corpus_reader, None) for item in range(nheaderlines)]
        for line in corpus_reader:
            if line[0].startswith('#'):
                continue
            syllables = list(line[0].split(',')[0])
            if 'ᆞ' in syllables:
                continue
            for syllable in syllables:
                #print(syllable)
                if is_hangul(syllable):
                    korean_syllables.add(syllable)
    return korean_syllables
#{'ᆞ', 'ᄀ'}
english_syllables = syllable_count_english()
korean_syllables_from_dict = syllable_count_korean_from_dict()
KAIST_number_unique_syllables = syllable_count_korean()

with open('D:/PhD Stuff/Linguistics Stuff/Syallable Storage feat. Santiago/Syllable Dictionary for English.csv', 'w') as out:
    writer = csv.writer(out)
    for i in list(english_syllables):
        writer.writerow(i)

with open('D:/PhD Stuff/Linguistics Stuff/Syallable Storage feat. Santiago/Syllable Dictionary for Korean from Dict.csv', 'w', encoding = 'utf-8', errors='ignore') as out:
    writer = csv.writer(out)
    for i in list(korean_syllables_from_dict):
        writer.writerow(i)

with open('D:/PhD Stuff/Linguistics Stuff/Syallable Storage feat. Santiago/Syllable Dictionary for Korean from Corpus.csv', 'w', encoding = 'euc_kr', errors='ignore') as out:
    writer = csv.writer(out)
    for i in list(KAIST_number_unique_syllables):
        writer.writerow(i)

print(f'number of unique syllables in English: %s' % len(english_syllables))
print(f'number of unique syllables in Korean from dict: %s' % len(korean_syllables_from_dict))
print(f'number of unique syllables in Korean from corpus: %s' % len(KAIST_number_unique_syllables))


### let's double check the number for Korean using a pronounciation dictionary:
