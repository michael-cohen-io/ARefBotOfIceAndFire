import pprint
import time
import anapioficeandfire
import praw
from prawoauth2 import PrawOAuth2Mini


from tokens import app_key, app_secret, access_token, refresh_token
from settings import scopes, user_agent


reddit_client = praw.Reddit(user_agent=user_agent)
oauth_helper = PrawOAuth2Mini(reddit_client, app_key=app_key, app_secret=app_secret, access_token=access_token, scopes=scopes, refresh_token=refresh_token)

already_checked = []

logFile = "log.txt"

api = anapioficeandfire.API()


def writeToLog(fileName, id):
    file = open(fileName, 'a')
    file.write(id + '\n')
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
    if tokens[0] == "ARefBotOfIceAndFire":
        return True
def get_character_data(c):
    response = ''

    #NAME
    response += '## **' + c.name + '**    \n'

    ##TTITLES
    if c.titles:
        response += '### ';
        i = 0
        while i != len(c.titles)-1:
            response += c.titles[i] + ', '
            i += 1
        response += c.titles[i]
    ##ALIASES
    if c.aliases:
        response += ', '
        i = 0
        while i != len(c.aliases)-1:
            response += c.aliases[i] + ', '
            i += 1
        response += c.aliases[i]
    response += '    \n'
    response += 'Born: ' + c.born + '    \n'
    response += 'Died: ' + c.died + '    \n'
    response += 'Father: ' + c.father + '    \n'
    response += 'Mother: ' + c.mother + '    \n'
    response += 'Spouse: ' + c.spouse + '    \n'

    ##ALLEGIANCES
    if c.allegiances:
        response += 'Allegiances: '
        for url in c.allegiances:
            tokens = url.split('/')
            id = int(tokens[-1])
            house = api.get_house(id=id)
            response += house.name + ', '
        response = response [:-2] + '    \n'

    ##BOOKS
    if c.books:
        response += "Appears in: "
        for url in c.books:
            tokens = url.split('/')
            id = int(tokens[-1])
            book = api.get_book(id=id)
            response += book.name + ', '
        response = response[:-2] + '    \n'

    if c.playedBy:
        response += "Played by: "
        for name in c.playedBy:
            response += name + ', '
        response = response[:-2] + '    \n'
    response += '***\n\n'
    return response


def get_data(characters):
    response = '# ARefBotOfIceAndFire v1.0\n\n'
    for c in characters:
        response += get_character_data(c)
    return response


def print_api_info(comment, query):
    characters = api.get_characters(name=query)
    reply = get_data(characters)
    comment.reply(reply)
    print("Comment replied: \n" + reply)

def get_query(text):
    q =  text.replace('ARefBotOfIceAndFire ', '', 1)
    return q

def inner_loop():
    oauth_helper.refresh()
    print("--------------New GET_COMMENTS()-------------------------")
    for c in praw.helpers.comment_stream(reddit_client, 'circlejerk'):
        if c.id not in already_checked and contains_bot_text(c):
            print("\n\n\n\n\n\n")
            print(c.submission)
            print(c.author)
            print(c.body)
            query = get_query(c.body)
            print_api_info(c, query)
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
