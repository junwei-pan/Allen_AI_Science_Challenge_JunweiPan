import re
import gensim
import os
import itertools
import numpy as np
import util
import argparse
from util import combination_index
parser = argparse.ArgumentParser("Word2Vec")

def get_vector_from_model(model, key):
    try:
        res = model[key]
    except:
        res = np.zeros(model.vector_size)
    return res
'''
'''

def test_on_validation(path_model, n_combination_question = 3, n_combination_answer = 3, n_word_question = 5):
    model = gensim.models.Word2Vec.load(path_model)
    path_train = 'data/validation_set.tsv'
    n_combination_question = 4
    n_combination_answer = 3
    n_word_question = 5
    n_total = 0
    n_correct = 0
    #set_stopword = ('a', 'an', 'the', 'are', 'is', 'that', 'this', 'will', 'is', 'are', 'was', 'were', 'of', 'for')
    d_word_count = util.load_d_word_count()
    for index, line in enumerate(open(path_train)):
        n_total += 1
        if index == 0:
            continue
        else:
            lst = line.lower().strip('\n').split('\t')
            question = lst[1].split(' ')
            lst_choice = [l.split(' ') for l in lst[2:]]
            #question_u = list(set(question).difference(set_stopword))
            d = {}
            for word in question:
                #word = word.strip('?').strip('.').strip(',').strip('!')
                word = util.norm_word(word)
                if d_word_count.has_key(word):
                    d[word] = d_word_count[word]
                else:
                    d[word] = 0
            sort = sorted(d.iteritems(), key = lambda dd : dd[1])
            question_u = [s[0] for s in sort[:n_word_question]]
            lst_com_q = util.combination_index(len(question_u), n_combination_question)
            max = -1000000
            answer_p = ''
            for com_q in lst_com_q:
                vec_q = np.sum([get_vector_from_model(model, question_u[i]) for i in com_q], axis = 0)
                for i_choice in range(4):
                    choice_u =list(set(lst_choice[i_choice]))
                    lst_com_choice = util.combination_index(len(choice_u), n_combination_answer)
                    for com_c in lst_com_choice:
                        vec_c = np.sum([get_vector_from_model(model, choice_u[i]) for i in com_c], axis = 0)
                        score = vec_q.dot(vec_c)
                        if score > max:
                            max = score
                            if i_choice == 0:
                                answer_p = 'A'
                            elif i_choice == 1:
                                answer_p = 'B'
                            elif i_choice == 2:
                                answer_p = 'C'
                            elif i_choice == 3:
                                answer_p = 'D'
            print "%s,%s" % (lst[0], answer_p)

def test_on_train(path_model, n_combination_question = 3, n_combination_answer = 3, n_word_question = 5):
    model = gensim.models.Word2Vec.load(path_model)
    path_train = 'data/training_set.tsv'
    n_total = 0
    n_correct = 0
    set_stopword = ('a', 'an', 'the', 'are', 'is', 'that', 'this', 'will', 'is', 'are', 'was', 'were', 'of', 'for')
    d_word_count = util.load_d_word_count()
    for index, line in enumerate(open(path_train)):
        n_total += 1
        if index == 0:
            continue
        else:
            lst = line.lower().strip('\n').split('\t')
            question = lst[1].split(' ')
            answer = lst[2]
            lst_choice = [l.split(' ') for l in lst[3:]]
            #question_u = list(set(question).difference(set_stopword))
            d = {}
            for word in question:
                word = word.strip('?').strip('.').strip(',').strip('!')
                if d_word_count.has_key(word):
                    d[word] = d_word_count[word]
                else:
                    d[word] = 0
            # Only consider the word with lowest frequency.
            sort = sorted(d.iteritems(), key = lambda dd : dd[1])
            question_u = [s[0] for s in sort[:n_word_question]]
            lst_com_q = util.combination_index(len(question_u), n_combination_question)
            max = -1000000
            answer_p = ''
            words_focus_question = []
            words_focus_choice = []
            for com_q in lst_com_q:
                vec_q = np.sum([get_vector_from_model(model, question_u[i]) for i in com_q], axis = 0)
                for i_choice in range(4):
                    choice_u =list(set(lst_choice[i_choice]))
                    lst_com_choice = util.combination_index(len(choice_u), n_combination_answer)
                    for com_c in lst_com_choice:
                        vec_c = np.sum([get_vector_from_model(model, choice_u[i]) for i in com_c], axis = 0)
                        score = vec_q.dot(vec_c)
                        if score > max:
                            words_focus_question = [question_u[i] for i in com_q]
                            words_focus_choice = [choice_u[i] for i in com_c]
                            max = score
                            if i_choice == 0:
                                answer_p = 'a'
                            elif i_choice == 1:
                                answer_p = 'b'
                            elif i_choice == 2:
                                answer_p = 'c'
                            elif i_choice == 3:
                                answer_p = 'd'
            
            if answer == answer_p:
                n_correct += 1
            print ' '.join(lst) + '\n' + "Focus Words in Question: " + ' '.join(words_focus_question) + '\n' + "Focus Words in Choice: " + ' '.join(words_focus_choice)
            print 'Predicted Answer: ' + answer_p
            print str(n_correct) + ' / ' + str(n_total) + '\t' + str(n_correct * 1.0 / n_total)
    print n_correct * 1.0 / n_total


def train_model(lst_sentence, path_model, min_count_p = 5, workers_p = 4, size_p = 200, window_p = 5):
    model = gensim.models.Word2Vec(lst_sentence, min_count = min_count_p, workers = window_p, size = size_p, window = window_p, cbow_mean = 0)
    model.save(path_model)
'''
# Train word2vec model
#dir = 'data/ck12-multi-line-txt/'
dir = 'data/wikipedia_content_based_on_ck_12_keyword_v1/'
path_model = 'model/word2vec_21.model'
lst_sentence = util.get_sentence(dir)
model = gensim.models.Word2Vec(lst_sentence, min_count = 5, workers = 4, size = 300, window = 9, iter = 10)
model.save(path_model)
'''
# Test model on train data
path_model = 'model/word2vec_21.model'
#test_on_train(path_model, n_combination_question = 3, n_combination_answer = 3, n_word_question = 5)
test_on_validation(path_model, n_combination_question = 3, n_combination_answer = 3, n_word_question = 5)
#print combination_index(10, 3)
