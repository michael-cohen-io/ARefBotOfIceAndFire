import praw
from prawoauth2 import PrawOAuth2Server

from tokens import app_key, app_secret, access_token, refresh_token
from settings import scopes, user_agent


reddit_client = praw.Reddit(user_agent=user_agent)
oauthserver = PrawOAuth2Server(reddit_client, app_key, app_secret, state=user_agent, scopes=scopes)
oauthserver.start()

tokens = oauthserver.get_access_codes()
pprint(tokens)
