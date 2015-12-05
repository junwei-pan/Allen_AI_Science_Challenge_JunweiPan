import wikipedia as wiki
import util

def get_word_count_train_validation():
    d_word_count_t_q = util.get_d_word_count_train_question()
    d_word_count_t_c = util.get_d_word_count_train_choice()
    d_word_count_v_q = util.get_d_word_count_validation_question()
    d_word_count_v_c = util.get_d_word_count_validation_choice()
    d_word_count = {}
    for word in d_word_count_t_q.keys():
        d_word_count.setdefault(word, 0)
        d_word_count[word] += d_word_count_t_q[word]
    for word in d_word_count_t_c.keys():
        d_word_count.setdefault(word, 0)
        d_word_count[word] += d_word_count_t_c[word]
    for word in d_word_count_v_q.keys():
        d_word_count.setdefault(word, 0)
        d_word_count[word] += d_word_count_v_q[word]
    for word in d_word_count_v_c.keys():
        d_word_count.setdefault(word, 0)
        d_word_count[word] += d_word_count_v_c[word]
    return d_word_count
    '''
    sort = sorted(d_word_count.iteritems(), key = lambda dd : dd[1])
    for s in sort:
        print "%s\t%d" % (s[0], s[1])
    '''

def get_wikipedia_content_based_on_word_count_train_validation(d_word_count):
    file = open('data/wikipedia_content_v1.txt', 'w')
    n_word = len(d_word_count.keys())
    n_current = 0
    for word in d_word_count.keys():
        n_current += 1
        print word, n_current, n_word, n_current * 1.0 / n_word
        if not word:
            continue
        lst_title = wiki.search(word)
        if len(lst_title) >= 1:
            for title in lst_title:
                title = title.encode('ascii', 'ignore')
                print 'title', title
                try:
                    content = wiki.page(title).content.encode('ascii', 'ignore')
                except wiki.exceptions.DisambiguationError as e:
                    print 'DisambiguationError', word
                    '''
                    for title_disambiguation in e.options:
                        title_disambiguation = title_disambiguation.encode('ascii', 'ignore')
                        print 'title_disambiguation', title_disambiguation
                        try:
                            content = wiki.page(title_disambiguation).content.encode('ascii', 'ignore')
                        except:
                            pass
                    '''
                except:
                    pass
                for line in content.split('\n'):
                    line = ' '.join(map(util.norm_word, line.split()))
                    if line:
                        file.write(line + '\n')
    file.close()

def get_wikipedia_content_based_on_ck_12_keyword():
    path_keyword = 'data/ck12_list_keyword.txt'
    lst_keyword = open(path_keyword).readlines()
    n_total = len(lst_keyword)
    file = open('data/wikipedia_content_based_on_ck_12_keyword_v1.txt', 'w')
    for index, line in enumerate(lst_keyword):
        keyword = line.strip('\n').lower()
        print index, n_total, index * 1.0 / n_total, keyword
        try:
            content = wiki.page(keyword).content.encode('ascii', 'ignore')
        except wiki.exceptions.DisambiguationError as e:
            print 'DisambiguationError', keyword
        except:
            print 'Error', keyword
        if not content:
            continue
        for line in content.split('\n'):
            line = ' '.join(map(util.norm_word, line.split()))
            if line:
                file.write(line + '\n')
    file.close()

def get_wikipedia_content_based_on_ck_12_keyword_one_file_per_keyword():
    '''
    Get wikipedia page content based on the keywords crawled from the ck-12 website.
    '''
    path_keyword = 'data/ck12_list_keyword.txt'
    dir_output = 'data/wikipedia_content_based_on_ck_12_keyword_one_file_per_keyword/'
    #path_keyword = 'data/training_set_question.tsv'
    #dir_output = 'data/wikipedia_content_based_on_train_question_one_file_per_keyword/'
    #path_keyword = 'data/validation_set_question.tsv'
    #dir_output = 'data/wikipedia_content_based_on_validation_question_one_file_per_keyword/'
    path_meta = path_keyword[:-4] + '_wiki_meta.tsv'
    file_meta = open(path_meta, 'w')
    lst_keyword = open(path_keyword).readlines()
    n_total = len(lst_keyword)
    for index, line in enumerate(lst_keyword):
        keyword = line.strip('\n').lower()
        print index, n_total, index * 1.0 / n_total, keyword
        content = None
        title = None
        try:
            content = wiki.page(keyword).content.encode('ascii', 'ignore')
            url = wiki.page(keyword).url.encode('ascii', 'ignore')
            title = wiki.page(keyword).title.encode('ascii', 'ignore')
        except wiki.exceptions.DisambiguationError as e:
            print 'DisambiguationError', keyword
        except:
            print 'Error', keyword
        if not content or not title:
            continue
        file_meta.write("%s\t%s\t%s\n" % (keyword, title, url))
        #file = open('data/wikipedia_content_based_on_ck_12_keyword_one_file_per_keyword/' + '_'.join(keyword.split()) + '.txt', 'w')
        path_output = dir_output + '/' + '_'.join(title.replace('/', '__').split()) + '.txt'
        file = open(path_output, 'w')
        for line in content.split('\n'):
            line = ' '.join(map(util.norm_word, line.split()))
            if line:
                file.write(line + '\n')
        file.close()

def get_wikipedia_meta_based_on_ck_12_keyword_one_file_per_keyword():
    '''
    Get wikipedia title, url information for the wikipedia page of the keywords
    '''
    path_keyword = 'data/ck12_list_keyword.txt'
    file = open(path_keyword[:-4] + '_meta.tsv', 'w')
    lst_keyword = open(path_keyword).readlines()
    n_total = len(lst_keyword)
    for index, line in enumerate(lst_keyword):
        keyword = line.strip('\n').lower()
        print index, n_total, index * 1.0 / n_total, keyword
        try:
            url = wiki.page(keyword).url.encode('ascii', 'ignore')
            title = wiki.page(keyword).title.encode('ascii', 'ignore')
            #content = wiki.page(keyword).content.encode('ascii', 'ignore')
        except wiki.exceptions.DisambiguationError as e:
            print 'DisambiguationError', keyword
        except:
            print 'Error', keyword
        res = "%s\t%s\t%s\n" % (keyword, title, url)
        file.write(res)
    file.close()

#get_wikipedia_meta_based_on_ck_12_keyword_one_file_per_keyword()
get_wikipedia_content_based_on_ck_12_keyword_one_file_per_keyword()
#get_wikipedia_content_based_on_ck_12_keyword()
'''
d = get_word_count_train_validation()
get_wikipedia_content_based_on_word_count_train_validation(d)
'''
