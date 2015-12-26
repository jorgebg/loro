import os
import re
import unicodedata

import tweepy
import requests


URL_LENGTH = 22
TWEET_LENGTH = 140
ELLIPSIS = '…'


class Handler:
    def __init__(self, title, keywords, description, url):
      self.description = description
      self.url = url

      self.matchers = []
      for k in keywords + [title]:
          k_1 = k.replace(' ', '\s*')
          for k_2 in [k_1, self.strip_accents(k_1)]:
              self.matchers.append(re.compile(k_2, re.IGNORECASE))

    def match(self, status):
        for matcher in self.matchers:
            if matcher.search(status.text):
                mentions = status.entities['user_mentions']
                reply = ' '.join(map(lambda m: '@' + m['screen_name'], mentions)) + ' '

                if len(reply+self.description) <= TWEET_LENGTH:
                    reply += self.description
                if len(reply)+URL_LENGTH+1 <= TWEET_LENGTH:
                    reply += ' ' + self.url

                return reply

    def strip_accents(self, s):
       return ''.join(c for c in unicodedata.normalize('NFD', s)
                      if unicodedata.category(c) != 'Mn')


def main(event=None, context=None):
    handlers_url = os.environ['HANDLERS_URL']
    consumer_key = os.environ['CONSUMER_KEY']
    consumer_secret = os.environ['CONSUMER_SECRET']
    access_token = os.environ['ACCESS_TOKEN']
    access_token_secret = os.environ['ACCESS_TOKEN_SECRET']

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)


    response = requests.get(handlers_url)
    handlers = map(lambda h: Handler(**h), response.json())


    since_id = api.favorites(page=-1)[0].id
    for mention in api.mentions_timeline(since_id=since_id):
        for handler in handlers:
            reply = handler.match(mention)
            if reply:
                print('reply', reply, mention.id)
                api.update_status(status=reply, in_reply_to_status_id=mention.id)
                break
        print('fav', mention.id)
        api.create_favorite(mention.id)


if __name__ == '__main__':
    main()
