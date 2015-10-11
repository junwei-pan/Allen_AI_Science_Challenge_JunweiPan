from HTMLParser import HTMLParser
from urllib2 import urlopen
#from BeautifulSoup import BeautifulSoup as BS
from bs4 import BeautifulSoup

def get_url_lesson_from_url_topic(url_topic):
    # Topic includes: Earth Science, Life Science, Physical Science, Biology, Chemestry and Physics
    lst_url = []
    html = urlopen(url_topic).read()
    soup = BeautifulSoup(html, 'html.parser')
    for tag_h3 in soup.find_all('h3'):
        r_url =  tag_h3.li.a.get('href')
        lst_url.append(url_topic + r_url.strip('/').split('/')[1])
    return lst_url

def get_read_url_from_url_lesson(url_lesson):
    s_lesson = url_lesson.strip('/').split('/')[-1]
    return "%s/lesson/%s/?referrer=content_details" % (url_lesson, s_lesson)
 
def crawl_text_from_read_url(url_read):
    html = urlopen(url_topic).read()
    print html
    soup = BeautifulSoup(html, 'html.parser')
    print soup.find_all('div', id = 'modality_content')
    
def get_keyword_from_url_topic(url_topic):
    # Topic includes: Earth Science, Life Science, Physical Science, Biology, Chemestry and Physics
    lst_url = []
    html = urlopen(url_topic).read()
    soup = BeautifulSoup(html, 'html.parser')
    for tag_h3 in soup.find_all('h3'):
        url_res =  ' '.join(tag_h3.li.a.get('href').strip('/').split('/')[-1].split('-'))
        lst_url.append(url_res)
    return lst_url

lst_url_topic = ['https://www.ck12.org/earth-science/', 'http://www.ck12.org/life-science/', 'http://www.ck12.org/physical-science/', 'http://www.ck12.org/biology/', 'http://www.ck12.org/chemistry/', 'http://www.ck12.org/physics/']

set_keyword = set()
for url_topic in lst_url_topic:
    lst_keyword = get_keyword_from_url_topic(url_topic)
    for keyword in lst_keyword:
        set_keyword.add(keyword)
for keyword in set_keyword:
    print keyword
'''
for url in get_url_lesson_from_url_topic(url_topic_earth):
    print url
    get_read_url_from_url_lesson(url)
'''
#url_topic = 'https://www.ck12.org/earth-science/Development-of-Hypotheses'
#url_read =  get_read_url_from_url_lesson(url_topic)
#crawl_text_from_read_url(url_read)
