import pprint
import time
import praw
from prawoauth2 import PrawOAuth2Mini


from tokens import app_key, app_secret, access_token, refresh_token
from settings import scopes, user_agent


reddit_client = praw.Reddit(user_agent=user_agent)
oauth_helper = PrawOAuth2Mini(reddit_client, app_key=app_key, app_secret=app_secret, access_token=access_token, scopes=scopes, refresh_token=refresh_token)

subreddit = reddit_client.get_subreddit('circlejerk')

already_checked = []

logFile = "log"

def writeToLog(fileName, id):
    file = open(fileName, 'a')
    file.write(id)
    file.close()

def readLog(fileName):
    file = open(fileName, 'r')
    del already_checked[:]
    for line in file:
        already_checked.append(line)
    file.close()

def contains_bot_text(c):
    text = c.body
    tokens = text.split()
    if "ARefOfIceAndFire" in tokens:
        return True

def print_api_info(c):
    c.reply("Jon Snuu")
    print("something happened!\n")


def inner_loop():
    oauth_helper.refresh()
    print("--------------New GET_COMMENTS()-------------------------")
    for c in praw.helpers.comment_stream(reddit_client, 'circlejerk'):
        if c.id not in already_checked and contains_bot_text(c):
            print("\n\n\n\n\n\n")
            print(c.author)
            print(c.submission)
            print(c.body)
            print_api_info(c)
            already_checked.append(c.id)
            writeToLog(logFile, c.id)
            time.sleep(540)




readLog(logFile)
i = 0
while True:
    try:
        inner_loop()
        string = "Iteration "
        string += str(i)
        print(string)
        i += 1
    except praw.errors.OAuthInvalidToken:
        # token expired, refresh 'em!
        oauth_helper.refresh()
    time.sleep(600)
