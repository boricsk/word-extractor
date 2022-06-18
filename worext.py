from curses import savetty
from operator import le
import requests
import re
from bs4 import BeautifulSoup, Comment
import click
from traitlets import default
from xcffib import wrap
import sys

def get_html_of(url):
    resp = requests.get(url)

    if resp.status_code !=200:
        print(f'Http status code : {resp.status_code} Exiting....')
        exit(1)
        
    return resp.content.decode()

def count_occurrences_in(word_list, min_length):
    word_count = {}
    for word in word_list:
        if len(word) < min_length:
            continue
        if word not in word_count:
            word_count[word] = 1
        else:
            current_count = word_count.get(word)
            word_count[word] = current_count + 1

    return word_count

def get_all_words_from(url):
    html = get_html_of(url)
    soup = BeautifulSoup(html, 'html.parser')
    raw_text = soup.get_text()
    return re.findall(r'\w+', raw_text)
    
def get_comments(url, IsSave, FileName):
    html = get_html_of(url)
    soup = BeautifulSoup(html, 'html.parser')
    comments = soup.find_all(string=lambda text: isinstance(text, Comment))
    
    if IsSave:
        CommentFile = open(FileName,'w')
        CommentFile.write(f"Comments of {url}\n")
        for c in comments:
            print(c)
            CommentFile.write(c+'\n')
            c.extract()
        CommentFile.close
    else:
        for c in comments:
            print(c)
    
def get_top_words_from(all_words, min_length):
    occurrences = count_occurrences_in(all_words, min_length)
    return sorted(occurrences.items(), key = lambda item: item[1], reverse=True)

def WriteData(FileName, WData):
    with open(FileName,'w') as wr:
        wr.write('\n' .join('%s %s' % x for x in WData))
    
    wr.close

@click.command()
@click.option('--url', '-u', prompt='Web URL', help='URL of webpage to extract from')
@click.option('--length', '-l', default=0, help='Minimum lenght of word (Default 0=no limit)')
@click.option('--outfile', '-o', help='Write outpot to file')
@click.option('--comments', '-c', help='Extract comments line from target', is_flag=True)

def main(url, length, outfile, comments):
    """Word Extractor V 1.0.0\n"""
    print("Word Extractor V 1.0.0 by\n")
    the_words = get_all_words_from(url)
    top_words = get_top_words_from(the_words, length)
    
    if comments:
        if outfile:
            print(f"Comments of {url}\n")
            print(get_comments(url, True, outfile))
        else:
            print(f"Comments of {url}\n")
            print(get_comments(url, False, outfile))
    else:
        if len(top_words) == 0:
            print("Given lenghth is too long...")
            exit(1)
            
        elif len(top_words) < 10:
            print("We have found less than 10 words")
            for i in range(len(top_words)):
                print(top_words[i][0], top_words[i][1])
            if outfile:
                WriteData(outfile, top_words)

        elif len(top_words) >= 10:
            print("We have found more than 10 words, here is the top words")
            for i in range(10):
                print(top_words[i][0])
            if outfile:
                WriteData(outfile, top_words)

if __name__ == '__main__':
    main()