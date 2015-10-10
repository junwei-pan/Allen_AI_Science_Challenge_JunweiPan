from HTMLParser import HTMLParser
from urllib2 import urlopen
#from BeautifulSoup import BeautifulSoup as BS
from bs4 import BeautifulSoup

def get_lesson_url_from_topic_url(url_topic):
    # Topic includes: Earth Science, Life Science, Physical Science, Biology, Chemestry and Physics
    lst_url = []
    html = urlopen(url_topic).read()
    soup = BeautifulSoup(html, 'html.parser')
    for tag_h3 in soup.find_all('h3'):
        r_url =  tag_h3.li.a.get('href')
        lst_url.append(url_topic + r_url.strip('/').split('/')[1])
    return lst_url

def get_read_url_from_lesson_url(url_lesson):
    s_lesson = url_lesson.strip('/').split('/')[-1]
    return "%s/lesson/%s/?referrer=content_details" % (url_lesson, s_lesson)
 
def crawl_text_from_read_url(url_read):
    html = urlopen(url_topic).read()
    print html
    soup = BeautifulSoup(html, 'html.parser')
    print soup.find_all('div', id = 'modality_content')
    

url_topic_earth = 'https://www.ck12.org/earth-science/'
'''
for url in get_lesson_url_from_topic_url(url_topic_earth):
    print url
    get_read_url_from_lesson_url(url)
'''
url_topic = 'https://www.ck12.org/earth-science/Development-of-Hypotheses'
url_read =  get_read_url_from_lesson_url(url_topic)
crawl_text_from_read_url(url_read)
