import os
import util
d_index_ABCD = {0: 'A', 1: 'B', 2: 'C', 3: 'D'}
lst_flag_choice = ['A', 'B', 'C', 'D']
set_stopword = ('a', 'an', 'the', 'are', 'is', 'that', 'this', 'will', 'is', 'are', 'was', 'were', 'of', 'for', 'to', 'be', 'and', 'in' , 'as' , 'by' , 'with' , 'on' , 'from' , 'or' , 'it' , '===' , 'which' , 'at' , '==' , 'have' , 'has' , 'not' , 'also' , 'their' , 'can' , 'his' , 'other' , 'they' , 'he' , 'its' , 'but' , 'such' , 'one' , 'been' , 'more' , 'than' , 'when' , 'used' , 'some' , 'most' , 'into' , 'may' , 'these' , 'had' , 'first' , 'all' , 'two' , 'many' , 'between' , 'there' , 'new' , 'only' , 'after' ,  'during' , 'who' , 'about')

def build_d_word_count_on_each_document(dir_data):
    file = open(dir_data + '_wc.tsv', 'w')
    d_total = {}
    d = {}
    for path in os.listdir(dir_data):
        dd = {}
        path = dir_data + '/' + path
        for index, line in enumerate(open(path)):
            lst = map(util.norm_word, line.strip('\n').split())
            for word in lst:
                if word not in set_stopword:
                    dd.setdefault(word, 0)
                    dd[word] += 1
                    d_total.setdefault(word, 0)
                    d_total[word] += 1
        d[path] = dd
    sort = sorted(d_total.iteritems(), key = lambda item : item[1], reverse = True)
    for item in sort:
        file.write("%s\t%d\n" % (item[0], item[1]))
    file.close()
    return d

def build_d_question_choice_validation(path_validation):
    d_q_choice = {}
    d_q_id = {}
    for index, line in enumerate(open(path_validation)):
        if index == 0:
            continue
        lst = line.strip('\n').split('\t')
        print lst
        d_q_choice[lst[1]] = lst[2:]
        d_q_id[lst[1]] = lst[0]
    return d_q_choice, d_q_id

def build_d_question_choice_train(path_train):
    d_q_choice = {}
    d_q_id = {}
    d_q_groundtruth = {}
    for index, line in enumerate(open(path_train)):
        if index == 0:
            continue
        lst = line.strip('\n').split('\t')
        print lst
        d_q_choice[lst[1]] = lst[3:]
        d_q_id[lst[1]] = lst[0]
        d_q_groundtruth[lst[1]] = lst[2]
    return d_q_choice, d_q_id, d_q_groundtruth

def predict(question, lst_path, lst_choice, d_file_wc, d_q_choice, n_top):
    '''
    '''
    d_question_wc = {}
    # The d_choice_wc consists detailed information about the word count of each choice: the total word count as well as the word count of each word in each choice
    d_choice_wc = {} 
    for path in lst_path[:n_top]:
        try:
            d_wc = d_file_wc[path]
        except:
            d_wc = {}
        for word in d_wc.keys():
            d_question_wc.setdefault(word, 0)
            d_question_wc[word] += d_wc[word]
    MAX = -1
    answer_p = ''
    for index_c, choice in enumerate(d_q_choice[question]):
        n_count = 0
        lst_word = map(util.norm_word, list(set(choice.split(' ')).difference(set_stopword)))
        for word in lst_word:
            if d_question_wc.has_key(word):
                n_count += d_question_wc[word]
        flag_choice = d_index_ABCD[index_c]
        d_choice_wc[flag_choice] = {}
        d_choice_wc[flag_choice]['cnt_total'] = n_count
        d_choice_wc[flag_choice]['d_word_wc'] = {}
        d_choice_wc[flag_choice]['choice'] = choice
        for word in lst_word: 
            if d_question_wc.has_key(word):
                d_choice_wc[flag_choice]['d_word_wc'][word] =  d_question_wc[word]
        if n_count > MAX:
            MAX = n_count
            answer_p = flag_choice

    return answer_p, d_choice_wc

def predict_train():
    path_train = 'data/training_set.tsv'
    #path_lucene_search_result = 'data/lucene_search_result_train.txt'
    #dir_data = 'data/wikipedia_content_based_on_ck_12_keyword_one_file_per_keyword'
    path_lucene_search_result = 'data/lucene_search_result_train_index_wiki_2.txt'
    dir_data = 'data/wikipedia_content_based_on_ck_12_keyword_PLUS_validation_question_PLUS_train_question_one_file_per_keyword'
    path_output = 'data/predict/model_10037.txt'
    file = open(path_output, 'w')
    file_wc = open(path_output[:-4] + '_wc.txt', 'w')
    print "Begin build_d_word_count_on_each_document"
    d_file_wc = build_d_word_count_on_each_document(dir_data)
    print "Begin build_d_question_choice_train"
    d_q_choice, d_q_id, d_q_groundtruth = build_d_question_choice_train(path_train)
    for index, line in enumerate(open(path_lucene_search_result)):
        lst = line.strip('\n').strip(',').split('\t')
        question = lst[0]
        lst_path = lst[1].split(',')
        lst_choice = d_q_choice[question]
        answer_p, d_choice_wc  = predict(question, lst_path, lst_choice, d_file_wc, d_q_choice, 3)
        groundtruth = d_q_groundtruth[question]
        file_wc.write(question + '\t' + groundtruth + '\n')
        for flag_choice in lst_flag_choice:
            d = d_choice_wc[flag_choice]
            s_word_wc = ''
            for word in d['d_word_wc']:
                s_word_wc = s_word_wc + '' + word + '::' + str(d['d_word_wc'][word])
            s_word_wc = s_word_wc.strip()
            s_output = "%s\t%s\t%d\t%s\n" % (flag_choice, d['choice'], d['cnt_total'], s_word_wc)
            file_wc.write(s_output)
        file.write(d_q_id[question] + ',' + answer_p + '\n')
    file.close()

def predict_validation():
    path_validation = 'data/validation_set.tsv'
    #path_lucene_search_result = 'data/lucene_search_result_validation.txt'
    #dir_data = 'data/wikipedia_content_based_on_ck_12_keyword_one_file_per_keyword'
    path_lucene_search_result = 'data/lucene_search_result_validation_index_wiki_2.txt'
    dir_data = 'data/wikipedia_content_based_on_ck_12_keyword_PLUS_validation_question_PLUS_train_question_one_file_per_keyword'
    file = open('data/predict/model_10034_validation.txt', 'w')
    file.write('id,correctAnswer\n')
    print "Begin build_d_word_count_on_each_document"
    d_file_wc = build_d_word_count_on_each_document(dir_data)
    print "Begin build_d_question_choice_validation"
    d_q_choice, d_q_id = build_d_question_choice_validation(path_validation)
    set_id_validation = set([d_q_id[key] for key in d_q_id.keys()])
    set_id_predicted = set()
    for index, line in enumerate(open(path_lucene_search_result)):
        lst = line.strip('\n').strip(',').split('\t')
        question = lst[0]
        if question == 'question':
            continue
        id = d_q_id[question]
        set_id_predicted.add(id)
        lst_path = lst[1].split(',')
        lst_choice = d_q_choice[question]
        answer_p = predict(question, lst_path, lst_choice, d_file_wc, d_q_choice, 4)
        file.write(d_q_id[question] + ',' + answer_p + '\n')
    print 'Missing', len(set_id_validation.difference(set_id_predicted))
    for id in set_id_validation.difference(set_id_predicted):
        file.write(id + ',' + 'C\n')
    file.close()

#predict_validation()
predict_train()
