import praw, requests
from requests.auth import HTTPBasicAuth
import re
from time import time

# Initialization

_oauth_scopes = {"identity", "privatemessages", "mysubreddits", "read"}
_oauth_start = 0
_oauth_length = 3300

def init_reddit_session():
	global _oauth_start, _oauth_length
	
	try:
		import bot_config as config
		
		print("Connecting to reddit...", end=" ")
		r = praw.Reddit(user_agent=config.useragent, api_request_delay=1.0, cache_timeout=20)
		
		print("logging in...", end=" ")
		if config.username is None or config.password is None:
			return None
		
		client_auth = HTTPBasicAuth(config.oauth_id, config.oauth_secret)
		headers = {"User-Agent": config.useragent}
		data = {"grant_type": "password", "username": config.username, "password": config.password}
		response = requests.post("https://www.reddit.com/api/v1/access_token", auth=client_auth, headers=headers, data=data)
		if response.status_code != 200:
			print("failed!\nResponse code = {}".format(response.status_code))
			return None
		
		response_content = response.json()
		if "error" in response_content and response_content["error"] != 200:
			print("failed!\nResponse code = {}".format(response_content["error"]))
			return None
		
		token = response_content["access_token"]
		if response_content["token_type"] != "bearer":
			return None
		_oauth_start = time()
		_oauth_length = response_content["expires_in"] - 300
		r.set_oauth_app_info(config.oauth_id, config.oauth_secret, "http://example.com/unused/redirect/uri")
		r.set_access_credentials(_oauth_scopes, access_token=token)
		
		print("done!")
		return r
	
	except Exception as e:
		print("failed! Couldn't connect: {}".format(e))
		raise e

def destroy_reddit_session(r):
	r.clear_authentication()

def renew_reddit_session(r):
	if time() - _oauth_start >= _oauth_length:
		print("Renewing oauth token")
		return init_reddit_session()
	return r

# Thing doing

def send_modmail(r, subreddit, title, body):
	r.send_message("/r/"+subreddit, title, body)

def send_pm(r, user, title, body, from_sr=None):
	r.send_message(user, title, body, from_sr=from_sr)

def reply_to(thing, body):
	if isinstance(thing, praw.objects.Inboxable):
		thing.reply(body)
	elif isinstance(thing, praw.objects.Submission):
		thing.add_comment(body)

# Utilities

_reddit_reduction_pattern = re.compile("https?://(?:.+\.)?(?:reddit\.com(?:(/r/\w+/comments/\w+/?)(?:(?:\w+/?)(.*))?|(?:(/(?:u|user|m|message|r/\w+)/.+)))|(redd.it/\w+))")

def reduce_reddit_link(link, include_prefix=False):
	global _reddit_reduction_pattern
	
	match = _reddit_reduction_pattern.match(link)
	if match:
		prefix = ("http://reddit.com" if include_prefix else "")
		
		#Normal comment page permalink, uses two groups (one optional)
		if match.group(1) is not None:
			return prefix+match.group(1)+("-/"+match.group(2) if match.group(2) is not None and len(match.group(2)) > 0 else "")
		#Other (user pages, messages, 
		if match.group(4) is not None:
			return prefix+match.group(4)
		#Shortlink
		if match.group(6) is not None:
			return prefix+match.group(6)
	
	return link

def is_post(thing):
	return isinstance(thing, praw.objects.Submission)

def is_comment(thing):
	return isinstance(thing, praw.objects.Comment)

def is_message(thing):
	return isinstance(thing, praw.objects.Message)
