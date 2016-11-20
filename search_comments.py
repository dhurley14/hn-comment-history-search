"""
takes in arguments to search for comments made by author or
full text search
"""
import argparse
import json
import elasticsearch

ES = elasticsearch.Elasticsearch()  # use default of localhost, port 9200

# search via comment_author
def comment_author_search(author):
    """ search for comment given comment author"""
    res = ES.search(index='saved_comments', body={"query": {
        "prefix": {
            "comment_author": str(author)
            }
        }})
    print json.dumps(res, indent=2)

# full comment search via keyword
def full_comment_keyword_search(keyword):
    """ search all comments for given keyword"""
    res = ES.search(index='saved_comments', body={"query": {
        "prefix": {
            "comment": str(keyword)
            }
        }})
    print json.dumps(res, indent=2)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Search your index!')
    parser.add_argument('-a', '--author', help='search for all comments made by \
        an author, `python search_comments.py -a patio11`', required=False)
    parser.add_argument('-f', '--full-text', help='do a full text search on the \
        comment field, `python search_comments.py -f twitter`', required=False)

    args = vars(parser.parse_args())
    if args['author'] is None and args['full_text'] is None:
        parser.print_help()
    if args['author'] is not None:
        comment_author_search(str(args['author']))
    if args['full_text'] is not None:
        full_comment_keyword_search(str(args['full_text']))
