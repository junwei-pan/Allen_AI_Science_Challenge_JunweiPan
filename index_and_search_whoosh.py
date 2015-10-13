from whoosh.fields import Schema, TEXT
from whoosh.index import create_in, open_dir
from whoosh.qparser import QueryParser
import os
import util

def index_wiki_documents():
    schema = Schema(title = TEXT(stored = True), content = TEXT)
    dir = 'data/wikipedia_content_based_on_ck_12_keyword_one_file_per_keyword'
    #ix = create_in("indexdir/wikipedia_contentbased_on_ck_12_keyword_one_file_per_keyword", schema)
    ix = create_in("indexdir", schema)
    writer = ix.writer()
    for path in os.listdir(dir):
        s_title = path.split('.')[0]
        print "Indexing: " + s_title
        path = dir + '/' + path
        s_content = ''
        for line in open(path):
            line = line.strip('\n')
            s_content += line
        writer.add_document(title = unicode(s_title), content = unicode(s_content))
    writer.commit()
    return ix
    '''
    query = QueryParser("content", ix.schema).parse("cell")
    res = ix.searcher().search(query)
    print len(res)
    for r in res:
        print r
    '''

def search_question(question, ix, top = 10):
    #index = open_dir('indexdir')
    query = QueryParser("content", ix.schema).parse(question)
    lst_result = ix.searcher().search(query)
    print '###lst_result###', len(lst_result)
    lst_res = []
    for result in lst_result[:top]:
        print '------Result-----', result
        try:
            lst_res.append([result['title'], result['content']])
        except:
            pass
    return lst_res

def choose_based_on_ir(ix, question, lst_choice):
    lst_res = search_question(question, ix)
    print 'len(lst_res)', len(lst_res)
    d_word_count = {}
    for res in lst_res:
        content = res[1]
        print 'content', content
        lst = map(util.norm_word, res.split())
        for word in lst:
            d_word_count.setdefault(word, 0.0)
            d_word_count[word] += 1
    MAX = -1
    answer_p = ''
    for index, choice in enumerate(lst_choice):
        n_match = 0
        lst = map(util.norm_word, choice.split())
        for word in lst:
            if d_word_count.has_key(word):
                n_match += d_word_count[word]
        if n_match > MAX:
            print 'n_match', n_match
            MAX = n_match
            if index == 0:
                answer_p = 'a'
            elif index == 1:
                answer_p = 'b'
            elif index == 2:
                answer_p = 'c'
            elif index == 3:
                answer_p = 'd'
    return answer_p, n_match

def test_on_train(ix):
    path = 'data/training_set.tsv'
    #ix = open_dir('indexdir')
    n_correct = 0
    for index, line in enumerate(open(path)):
        if index == 0:
            continue
        lst = line.strip('\n').split('\t')
        question = lst[1]
        lst_choice = lst[3:]
        answer = lst[2].lower()
        res = choose_based_on_ir(ix, question, lst_choice)
        answer_p = res[0]
        if answer == answer_p:
            n_correct += 1
        print 'Answer: ', answer
        print 'Answer_p: ', answer_p
        print n_correct, index, n_correct * 1.0 / index

ix = index_wiki_documents()
test_on_train(ix)
#search_question(u"cell")
