import re
import os
import util
import gensim

def word_count():
    PATTERN_TXT = re.compile(r'.*txt')
    d_word_count = {}

    dir = 'data/ck12-multi-line-txt/'
    for fn in os.listdir(dir):
        if PATTERN_TXT.match(fn):
            fn = dir + '/' + fn
            for line in open(fn):
                lst = line.strip('\n').lower().split(' ')
                for word in lst:
                    word = util.norm_word(word)
                    d_word_count.setdefault(word, 0)
                    d_word_count[word] += 1

    sort = sorted(d_word_count.iteritems(), key = lambda dd : dd[1], reverse = True)
    file = open('data/ck-12-word-count.txt', 'w')
    for kv in sort:
        file.write("%s\t%d\n" % (kv[0], kv[1]))
    file.close()
            
def statis_word2vec_coverage():
    '''
    How many words can be searched in the word2vec model ? 
    And which ones can or can not be found ?  
    This can guide us to use more and more data.
    '''
    path_model = 'model/word2vec_6.model'
    model = gensim.models.Word2Vec.load(path_model)
    d_word_count = util.get_d_word_count_validation_choice()
    n_found = 0
    n_miss = 0
    for word in d_word_count.keys():
        try:
            res = model[word]
            n_found += 1
            print "%s\t%d\tFound" % (word, d_word_count[word])
        except:
            n_miss += 1
            print "%s\t%d\tMiss" % (word, d_word_count[word])
    print "Found\t%d\tMiss\t%d" % (n_found, n_miss)

word_count()
#statis_word2vec_coverage()
