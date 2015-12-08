#!/usr/bin/python
import json
import urllib
import util

def hit_google(query):
    d_res = {}
    d_res['query'] = query
    d_res['lst_hits'] = []
    query = urllib.urlencode({'q': query})
    url = 'http://ajax.googleapis.com/ajax/services/search/web?v=1.0&%s' % query
    try:
        search_response = urllib.urlopen(url)
        search_results = search_response.read()
        results = json.loads(search_results)
        data = results['responseData']
        hits = data['results']
        for h in hits:
            d_res['lst_hits'].append(h['url'])
        return d_res
    except:
        return {}

def search_queries(lst_query, path):
    file = open(path, 'w')
    for index, query in enumerate(lst_query):
        print "%d\t%s" % (index, query)
        d_res = hit_google(query)
        if d_res:
            s_res = json.dumps(d_res)
            file.write(s_res + '\n')
    file.close()

lst_question = util.get_questions_train()
search_queries(lst_question, 'data/google_result_url_train.json')
#hit_google('yahoo', 'data/google_result_url_test.json')
#test('yahoo')
