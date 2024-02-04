## About
I wanted the ability to search just Hacker News comments I had upvoted.  HN offers
a search api via algolia, but I wanted something more fine tuned for me my needs.. I had
read a post about someone indexing their gmail inbox with elasticsearch and
wanted to try and use elasticsearch as the search engine for my 'saved comments index'.
[This project](https://github.com/oliver006/elasticsearch-gmail) has served
as the groundwork for this repository.

HN offers a search API, yet I needed to refine my search to comments that I
already knew I had upvoted / saved.  What I needed was a way to do just this.    

The following will offer an introduction to [Elastic](https://elastic.co)
and hopefully someone out there will find this useful.  So without further
introduction...

## SECRETS
Secrets, secrets are no fun unless you share with everyone.  In order to access the comments
that you have upvoted (i.e. this link , you will need your `__cfduid`, `user` and `_ga`. 
You can access these via your cookies in your browser.  Go to news.ycombinator.com and sign in, 
then check your cookies for HN and you should see these two profiles there.
Save those into a file called `SECRETS.txt` (see `SAMPLE-SECRETS.txt`).

## Web Scraping
So the script `get_saved_comments.py` grabs all of your saved comments and
writes them (via cPickle) to a file `temp_output.txt` in this directory. 

## ElasticSearch 
Once you have ran the `get_saved_comments.py` script you will need to start elasticsearch.
Make sure you have [downloaded elasticsearch](https://www.elastic.co/downloads/elasticsearch).

I used elasticsearch-1.4.4 so if there are any issues uploading the data, let me know or 
make a pull request (?). 

Once the download is complete, `cd` into the elasticsearch directory then proceed with `./bin/elasticsearch`.  
This will begin the elasticsearch server.  Then run `elastic_uploader.py` to upload the pickled
comments to the local elasticsearch server and you will be on your way to searching through your saved comments!

## Sample Queries
I have added some basic queries in the `search_comments.py` file.  You can
do a search given an author or a full text search.  These are just samples
and in no way representative of what Elastisearch is capable of!

Given Author: `python search_comments.py -a patio11` will yield something like..
```
{
  "hits": {
    "hits": [
      {
        "_score": 1.0, 
        "_type": "comment", 
        "_id": "934", 
        "_source": {
          "comment": "A lot of his arguments are backed by the assertion that \"The majority of British math major graduates can't do X.\" As I can attest at the US polytechnic university I graduated from, graduation is not necessarily the best measure of the success of an education system. This is especially true for math majors, most of whom decide partway to disengage from the thinking part of mathematics and turn to teaching. It's no secret why: they thought math in university would be a continuation of math in high school, and when they are instead asked to think hard about linear algebra or topology or analysis, they decide they don't like math after all. Such students have special, easier courses and yet get the same degree as the top students in their department.\n", 
          "story_title_url": "item?id=9033696", 
          "age": "647 days ago", 
          "comment_author_url": "user?id=patio11", 
          "comment_author": "patio11", 
          "story_title_text": " | on: Investing in Women-led Fortune 1000 Companies"
        }, 
        "_index": "saved_comments"
      }...
    ], 
    "total": 2, 
    "max_score": 1.0
  }, 
  "_shards": {
    "successful": 5, 
    "failed": 0, 
    "total": 5
  }, 
  "took": 1, 
  "timed_out": false
}
```

And a full text search: `python search_comments.py -f twitter`
```
{
  "hits": {
    "hits": [
      {
        "_score": 1.0, 
        "_type": "comment", 
        "_id": "47", 
        "_source": {
          "comment": "Chiming in as a TWC user on the West Coast:Github out, Etsy out, Paypal out, Twitter out, Soundcloud out, Crunchbase out, Heroku out, Spotify intermittent, Netflix only loads a white page with plaintext \"who's watching\" list and no functionality.\n", 
          "story_title_url": "item?id=12759697", 
          "age": "29 days ago", 
          "comment_author_url": "user?id=shredprez", 
          "comment_author": "shredprez", 
          "story_title_text": " | on: DDoS Attack Against Dyn Managed DNS"
        }, 
        "_index": "saved_comments"
      }...
    ], 
    "total": 26, 
    "max_score": 1.0
  }, 
  "_shards": {
    "successful": 5, 
    "failed": 0, 
    "total": 5
  }, 
  "took": 2, 
  "timed_out": false
}
```

DELETE ME
