import praw
from prawoauth2 import PrawOAuth2Mini

import time

from tokens import app_key, app_secret, access_token, refresh_token
from settings import scopes, user_agent

from book_data import BookResponse
from character_data import CharacterResponse
from house_data import HouseResponse

class BotController:


    def __init__(self, file, subreddit):
        self._logFile = file
        self._subreddit = subreddit

        self.reddit = praw.Reddit(user_agent=user_agent)
        self.oauth_helper = PrawOAuth2Mini(self.reddit, app_key=app_key, app_secret=app_secret, access_token=access_token, scopes=scopes, refresh_token=refresh_token)
        self.already_checked_posts = []

    def read_log(self):
        file = open(self._logFile, 'r')
        self.already_checked_posts = []
        for line in file:
            self.already_checked_posts.append(line)
        file.close()

    def write_to_log(self, id):
        file = open(self._logFile, 'a')
        file.write(id + '\n')
        file.close()

    def _contains_bot_text(self, c):
        tokens = c.body.split()
        return tokens[0] == 'ARefBotOfIceAndFire!'

    def get_data(self, raw_text):
        tokens = raw_text.split()
        query_type = tokens[1]

        if query_type == 'Characters':
            CR = CharacterResponse(raw_text)
            return CR.create_response()
        elif query_type == 'Book':
            BR = BookResponse(raw_text)
            return BR.create_response()
        else:
            HR = HouseResponse(raw_text)
            return HR.create_response()

    def comment_feed_loop(self):
        self.oauth_helper.refresh()
        print("--------------New GET_COMMENTS()-------------------------")
        for c in praw.helpers.comment_stream(self.reddit, self._subreddit):
            if c.id not in self.already_checked_posts and self._contains_bot_text(c):
                print("\n\n\n\n\n\n")
                print(c.submission)
                print(c.author)
                print(c.body)
                response = self.get_data(c.body)
                c.reply(response)
                self.already_checked_posts.append(c.id)
                self.write_to_log(c.id)
                print('Request satisfied. Sleeping for 11 minutes starting at ' + time.ctime())
                time.sleep(660)

    def start_bot(self):
        self.read_log()
        i = 0
        while True:
            try:
                self.comment_feed_loop()
            except praw.errors.OAuthInvalidToken:
                # token expired, refresh 'em!
                self.oauth_helper.refresh()
            time.sleep(600)

bot = BotController('log.txt', 'circlejerk')
bot.start_bot()
