"""
Download the signed-in user's upvoted comments
and save them to a text file!
"""

import cPickle as pickle
import time
import argparse
import os

import requests
from bs4 import BeautifulSoup



# Read data from SECRETS.txt file so that we don't commit our secrets to github.
__CFDUID = ''
_GA = ''
USER = '' # used for authentication
SECRETS_PATH = 'SECRETS.txt'
USERNAME = '' # used in url GET params

with open(SECRETS_PATH, 'r+b') as secrets_file:
    __CFDUID, _GA, USER = secrets_file.read().splitlines()

COOKIE_STR = ''.join([__CFDUID, _GA, USER])
print COOKIE_STR


# Headers to send with every request
REQUEST_HEADERS = {
    ':authority': 'news.ycombinator.com',
    ':method':'GET',
    ':path':'/upvoted?',
    ':scheme': 'https',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'accept-encoding':'gzip, deflate, sdch',
    'accept-language':'en-US,en;q=0.8',
    'cookie': COOKIE_STR,
    'referer':'https://news.ycombinator.com/',
    'upgrade-insecure-requests':"1",
    'user-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36',
}

URL = "https://news.ycombinator.com/upvoted?"

# create the requests
def requester(page=1):
    """ download a page of comments from the signed in user's upvoted comments page'"""
    resonse_obj = requests.get(
        URL,
        params={'id':USERNAME, 'comments':'t', 'p':page},
        headers=REQUEST_HEADERS
        )

    soup = BeautifulSoup(resonse_obj.text.encode('utf-8', 'ignore'), 'html.parser')
    comments = soup.find_all('span', 'c00')
    comment_headers = soup.find_all('span', 'comhead')
    ages = soup.find_all('span', 'age')
    story_titles = soup.find_all('span', 'storyon')

    print len(comments)
    print len(comment_headers)
    print len(ages)
    print len(story_titles)

    items = []

    # create json for the elasticsearch cluster to use
    for i in range(len(comments)):
        comment = comments[i].text
        comment_author = comment_headers[i].a.text
        comment_author_url = comment_headers[i].a.get('href')
        age = ages[i].text
        story_title_text = story_titles[i].text
        story_title_url = story_titles[i].a.get('href')
        items.append({
            "comment": comment,
            "comment_author":comment_author,
            "comment_author_url": comment_author_url,
            "age":age,
            "story_title_text":story_title_text, "story_title_url":story_title_url
        })

    #print items
    return items


def write_to_file(items, output_file_name='temp_output.txt'):
    """write the scraped data to our output file, we will use this
    output file as the source to upload data into elasticsearch """
    statinfo = os.stat(output_file_name)
    print 'prior file size.. ', statinfo.st_size
    with open(output_file_name, 'a+b') as writefile:
        pickle.dump(items, writefile)
    statinfo = os.stat(output_file_name)
    print 'post file size.. ', statinfo.st_size

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Download the user with the \
        credentials stored in your SECRETS.txt file')
    parser.add_argument('-n', '--number', help='Number of pages of saved comments\
        to download, defaults to 10 (one)',
                        required=False)
    parser.add_argument('-u', '--username', help='your username', required=True)
    parser.add_argument('-s', '--secrets-file', help='path to the SECRETS.txt file, i.e. `~/Desktop/SECRETS.txt`', required=False)
    parser.add_argument('-e', '--sleep', help='number of seconds to sleep before requesting next \
    comment page this is the nice thing to do on the net..', required=False)

    args = vars(parser.parse_args())
    print args
    USERNAME = args['username']
    NUM_PAGES = 10
    SLEEP_SECONDS = 2.0
    if args['secrets_file'] is not None:
        SECRETS_PATH = str(args['secrets_file'])
    if args['number'] is not None:
        print 'found number in args'
        NUM_PAGES = int(args['number'])
    if args['sleep'] is not None:
        SLEEP_SECONDS = args['sleep']
    i = 1
    print NUM_PAGES, i
    print SLEEP_SECONDS
    while i <= NUM_PAGES:
        print '\n*\n*\n*\n*\n*\n*\nGETTING PAGE {0}, {1}\n*\n*\n*\n*\n*\n*\n'.format(i, i <= NUM_PAGES)
        stuff = requester(page=i)
        write_to_file(stuff)
        i += 1
        print 'about to sleep for {0} cuz I\'m a good netizen..'.format(SLEEP_SECONDS)
        time.sleep(SLEEP_SECONDS)
