REDDIT_USERAGENT = ""
REDDIT_OAUTH_SCOPES = {"identity", "privatemessages"}

SOCIAL_AUTH_REDDIT_KEY = ""
SOCIAL_AUTH_REDDIT_SECRET = ""
SOCIAL_AUTH_REDDIT_AUTH_EXTRA_ARGUMENTS = {"duration": "permanent", "scope": ",".join(REDDIT_OAUTH_SCOPES)}
SOCIAL_AUTH_REDDIT_REDIRECT = "http://localhost:8000/complete/reddit/"
