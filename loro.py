import os
import re
import unicodedata

import requests
import tweepy

try:
    from settings import (
        CONSUMER_KEY,
        CONSUMER_SECRET,
        ACCESS_TOKEN,
        ACCESS_TOKEN_SECRET,
        HANDLERS_URL,
        SCREEN_NAME
    )
except ImportError:
    raise ImportError('Please run "cp settings.example.py settings.py" and edit the new file.')


URL_LENGTH = 22
TWEET_LENGTH = 140


class Handler:
    def __init__(self, title, keywords, description, url):
      self.title = title
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
                mentions = self.get_mentions(status)

                reply = ' '.join(map(lambda m: '@' + m, mentions)) + ' '

                if len(reply+self.description) <= TWEET_LENGTH:
                    reply += self.description
                if len(reply)+URL_LENGTH+1 <= TWEET_LENGTH:
                    reply += ' ' + self.url

                return reply

    def get_mentions(self, status):
        mentions = list(map(lambda m: m['screen_name'], status.entities['user_mentions']))
        mentions.remove(SCREEN_NAME)
        mentions.append(status.author.screen_name)
        return mentions

    def strip_accents(self, s):
        return ''.join(c for c in unicodedata.normalize('NFD', s)
                      if unicodedata.category(c) != 'Mn')

    def __str__(self):
        return self.title


def main(event=None, context=None):
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth)


    response = requests.get(HANDLERS_URL)
    handlers = list(map(lambda h: Handler(**h), response.json()))


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
