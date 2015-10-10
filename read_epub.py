import epub
import os  
import re

PATTERN_TAG = re.compile(r'<[^>]+>')
PATTERN_EPUB = re.compile(r'.+\.epub')
PATTERN_HTML = re.compile(r'.+\.html')


def remove_tags(text):
    return PATTERN_TAG.sub('', text)

def convert_epub_to_html(path_epub):
    file = open(path_epub.split('/')[0] + '/ck12-html/' + path_epub.split('/')[-1].split('.')[0] + '.html', 'w')
    book = epub.open_epub(path_epub)
    lst_item = book.opf.manifest.values()
    for item in lst_item:
        # read the content
        if PATTERN_HTML.match(item.href):
            data = book.read_item(item)
            file.write(data + '\n')
    file.close()
'''
def convert_epub_to_text_one_line(path_epub):
    file = open(path_epub.split('.')[0] + '.txt', 'w')
    book = epub.open_epub(path_epub)
    lst_item = book.opf.manifest.values()
    for item in lst_item:
        # read the content
        data = book.read_item(item)
        file.write(' '.join(remove_tags(data).split()))
    file.close()
'''
def convert_html_to_text_multiple_line(path_html):
    file = open('data/ck12-multi-line-txt/' + path_html.split('/')[-1].split('.')[0] + '.multi_line.txt', 'w')
    one_line = ''
    for line in open(path_html):
        res_tmp = ' '.join(remove_tags(line).strip('\n').split())
        if res_tmp != '' and res_tmp != '\n':
            #print res_tmp
            one_line += line.strip('\n')
    one_line = remove_tags(one_line)
    lst = one_line.split('.')
    for line in lst:
        file.write(' '.join(line.strip().split()).lower() + '\n')
    file.close()
    '''
    book = epub.open_epub(path_epub)
    lst_item = book.opf.manifest.values()
    for item in lst_item:
        # read the content
        data = book.read_item(item)
        file.write(' '.join(remove_tags(data).split()).lower() + '\n')
    file.close()
    '''

def get_item(path_epub):
    book = epub.open_epub(path_epub)
    for item in book.opf.manifest.values() :
        print item.href

def _convert_epub_to_html():
    dir = 'data/ck12-epub'
    for fn in os.listdir(dir):
        if PATTERN_EPUB.match(fn):
            fn = dir + '/' + fn
            #get_item(fn)
            convert_epub_to_html(fn)

def _convert_html_to_text_multiple_line():
    dir_html = 'data/ck12-html/'
    for path_html in os.listdir(dir_html):      
        path_html = dir_html + path_html
        convert_html_to_text_multiple_line(path_html)

_convert_html_to_text_multiple_line()
