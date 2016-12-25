import random
import requests

urls = [
    'https://reddit.com'
]


class ReddithorFetch:
    @staticmethod
    def getHomePage(subreddit = None):
        random.shuffle(urls)
        for i in urls:
            if subreddit == None or len(subreddit) == 0:
                subreddit = '/'
            else:
                subreddit = '/r/' + subreddit
            complete_url = i+subreddit+'/.json'
            r = requests.get(complete_url,  headers = {'User-agent': 'Reddithor - 1.0'}, timeout = 10)
            try:
                return r.json()["data"]["children"]
            except ValueError:
                continue