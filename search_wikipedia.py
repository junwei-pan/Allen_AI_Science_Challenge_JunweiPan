import wikipedia as wiki
import util

def get_wiki_summary_of_questions():
    path = 'data/training_set.tsv'
    data = open(path).readlines()
    n_total = len(data)
    n_current = 0
    for line in data:
        n_current += 1
        print n_current, n_total, n_current * 1.0 / n_total
        lst = line.strip('\n').split('\t')
        id = lst[0]
        question = lst[1]
        try:
            summary = wiki.summary(question).encode('ascii', 'ignore')
            file = open('data/wiki_summary/' + id + '.txt', 'w')
            file.write(summary)
            file.close()
        except:
            pass
        

def maaaain():
    path_trian = ''
    n_correct = 0
    n_current = 0
    for line in open(path_train):
        lst = line.strip('\n').split('\t')
        lst_word = map(util.norm_word, summary.split())
        question = lst[1]
        answer = lst[2].lower()
        n_match_max = 0
        answer_p = 'c'
        try:
            summary = wiki.summary(question).encode('ascii', 'ignore')
            d = {}
            for word in lst_word:
                d.setdefault(word, 0.0)
                d[word] += 1
            for index, choice in lst[3:]:
                n_match = 0
                for word in map(util.norm_word, choice.split(' ')):
                    if d.has_key(word):
                        n_match += d[word]
                    else:
                        pass
                if n_match > n_match_max:
                    n_match_max = n_match
                    if index == 0:
                        answer_p = 'a'
                    elif index == 1:
                        answer_p = 'b'
                    elif index == 2:
                        answer_p = 'c'
                    elif index == 3:
                        answer_p = 'd'
        except:
            pass
        if answer_p == answer:
            n_correct += 1
        print ' '.join(lst_word)
        print 'Answer: ' + answer
        print 'Answer_p' + answer_p

def get_cooccurence(lst_set_sentence, lst_word_question, lst_word_choice):
    res = 0
    for sentence in lst_set_sentence:
        flag = True
        for word in lst_word_question:
            if not word in sentence:
                flag = False
        for word in lst_word_choice:
            if not word in sentence:
                flag = False
        if flag == True:
            res += 1
    return res


def get_max_occurence(lst_set_sentence, question, lst_choice, d_word_count, set_stopword, n_word_question, n_combination_question, n_combination_answer):
    answer_p = ''
    MAX = -1
    lst_word_focus_q = []
    lst_word_focus_c = []
    lst_word_question_u = list(set(map(util.norm_word, question.split())))
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
    lst_com_q = util.combination_index(len(lst_word_question_u), n_combination_question)
    for com_q in lst_com_q:
        lst_word_question = [lst_word_question_u[i] for i in com_q]
        for index_c, choice in enumerate(lst_choice):
            # Filter stop words in choice in order to prevent them from calculating cooccurence.
            lst_word_choice_u = list(set(map(util.norm_word, choice.split())).difference(set_stopword))
            lst_com_c = util.combination_index(len(lst_word_choice_u), n_combination_answer)
            for com_c in lst_com_c:
                lst_word_choice = [lst_word_choice_u[i] for i in com_c]
                n_cooccurence = get_cooccurence(lst_set_sentence, lst_word_question, lst_word_choice)
                if n_cooccurence > MAX :
                    MAX = n_cooccurence
                    lst_word_focus_q = lst_word_question
                    lst_word_focus_c = lst_word_choice
                    if index_c == 0:
                        answer_p = 'A'
                    elif index_c == 1:
                        answer_p = 'B'
                    elif index_c == 2:
                        answer_p = 'C'
                    elif index_c == 3:
                        answer_p = 'D'

    return answer_p, MAX, lst_word_focus_q, lst_word_focus_c


def search_train(): # Too Slow
    set_stopword = ('a', 'an', 'the', 'are', 'is', 'that', 'this', 'will', 'is', 'are', 'was', 'were', 'of', 'for')
    path = 'data/training_set.tsv'
    d_word_count = util.load_d_word_count()
    n_word_question = 5
    n_combination_question = 3
    n_combination_answer = 3
    n_correct = 0
    lst_set_sentence = []
    path_data = 'data/wikipedia_content_based_on_ck_12_keyword_v1/wikipedia_content_based_on_ck_12_keyword_v1.txt'
    print 'Begin load all sentences'
    for line in open(path_data):
        set_sentence = set(map(util.norm_word, line.strip('\n').split()))
        if len(set_sentence) >= 5:
            lst_set_sentence.append(set_sentence)
    print 'End load all sentences'
    print len(lst_set_sentence)
    for index, line in enumerate(open(path)):
        if index == 0:
            continue
        lst = line.strip('\n').split('\t')
        id = lst[0]
        question = lst[1]
        answer = lst[2]
        lst_choice = lst[3:]
        answer_p, MAX, lst_word_focus_q, lst_word_focus_c  = get_max_occurence(lst_set_sentence, question, lst_choice, d_word_count, set_stopword, n_word_question, n_combination_question, n_combination_answer)
        if answer_p == answer:
            n_correct += 1
        print ' '.join(lst)
        print 'Answer: ' + answer
        print 'Answer_p: ', answer_p
        print n_correct, index + 1, n_correct * 1.0 / (index + 1)


search_train()
#get_wiki_summary_of_questions()
