from nltk.stem.porter import *
import os
import string
exclude = set(string.punctuation)
stemmer = PorterStemmer()

def norm_word(word):
    # v1
    #word = word.lower().strip('?').strip('.').strip(',').strip('!').strip(':').strip(';').strip('\"').strip('\'').strip()
    # v2
    word = ''.join(ch for ch in word.lower() if ch not in exclude)
    return word
    '''
    # Not work based on experiment 10004 and 10008.
    try:
        word = stemmer.stem(word.lower().strip('?').strip('.').strip(',').strip('!'))
    except:
        word = word.lower().strip('?').strip('.').strip(',').strip('!')
    return word
    '''
def get_sentence(dir):
    lst_sentence = []
    for path in os.listdir(dir):
        path = dir + path
        for line in open(path):
            lst = line.strip('\n').split(' ')
            lst_norm = [norm_word(word) for word in lst]
            lst_sentence.append(lst_norm)
    return lst_sentence

def get_d_word_count_train_question():
    path_train = 'data/training_set.tsv'
    d_word_count = {}
    for line in open(path_train):
        lst = line.strip('\n').split('\t')
        for word in lst[1].split(' '):
            word = norm_word(word)
            d_word_count.setdefault(word, 0)
            d_word_count[word] += 1
    return d_word_count

def get_d_word_count_train_choice():
    path_train = 'data/training_set.tsv'
    d_word_count = {}
    for line in open(path_train):
        lst = line.strip('\n').split('\t')
        for choice in lst[3:]:
            for word in choice.split(' '):
                word = norm_word(word)
                d_word_count.setdefault(word, 0)
                d_word_count[word] += 1
    return d_word_count

def get_d_word_count_validation_question():
    path_validation = 'data/validation_set.tsv'
    d_word_count = {}
    for line in open(path_validation):
        lst = line.strip('\n').split('\t')
        for word in lst[1].split(' '):
            word = norm_word(word)
            d_word_count.setdefault(word, 0)
            d_word_count[word] += 1
    return d_word_count

def get_d_word_count_validation_choice():
    path_validation = 'data/validation_set.tsv'
    d_word_count = {}
    for line in open(path_validation):
        lst = line.strip('\n').split('\t')
        for choice in lst[2:]:
            for word in choice.split(' '):
                word = norm_word(word)
                d_word_count.setdefault(word, 0)
                d_word_count[word] += 1
    return d_word_count
