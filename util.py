from nltk.stem.porter import *
import itertools
import os
import string
exclude = set(string.punctuation)
stemmer = PorterStemmer()

path_train = 'data/training_set.tsv'
path_validation = 'data/validation_set.tsv'

def load_d_word_count(path = 'data/ck-12-word-count.txt'):
    d = {}
    for line in open(path):
        lst = line.strip('\n').split('\t')
        d[lst[0]] = int(lst[1])
    return d

def combination_index(N, n_com):
    res = []
    s = ''
    for i in range(N):
        s += str(i)
    for i in range(1, n_com + 1):
        iter_com = itertools.combinations(s, i)
        for com in iter_com:
            com_tmp = [int(c) for c in com]
            res.append(com_tmp)
    return res

def norm_word(word):
    # v1
    #word = word.lower().strip('?').strip('.').strip(',').strip('!').strip(':').strip(';').strip('\"').strip('\'').strip()
    word = word.lower().strip('?').strip('.').strip(',').strip('!')
    # v2
    #word = ''.join(ch for ch in word.lower() if ch not in exclude)
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
    d_word_count = {}
    for line in open(path_train):
        lst = line.strip('\n').split('\t')
        for word in lst[1].split(' '):
            word = norm_word(word)
            d_word_count.setdefault(word, 0)
            d_word_count[word] += 1
    return d_word_count

def get_d_word_count_train_choice():
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
    d_word_count = {}
    for line in open(path_validation):
        lst = line.strip('\n').split('\t')
        for word in lst[1].split(' '):
            word = norm_word(word)
            d_word_count.setdefault(word, 0)
            d_word_count[word] += 1
    return d_word_count

def get_d_word_count_validation_choice():
    d_word_count = {}
    for line in open(path_validation):
        lst = line.strip('\n').split('\t')
        for choice in lst[2:]:
            for word in choice.split(' '):
                word = norm_word(word)
                d_word_count.setdefault(word, 0)
                d_word_count[word] += 1
    return d_word_count

def get_questions(path):
    lst_res = []
    for index, line in enumerate(open(path)):
        if index == 0:
            continue
        lst = line.strip('\n').split('\t')
        lst_res.append(lst[1])
    return lst_res

def get_questions_train():
    return get_questions(path_train)

def get_questions_validation():
    return get_questions(path_validation)
