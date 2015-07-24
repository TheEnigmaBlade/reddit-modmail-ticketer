from functools import lru_cache, wraps
from threading import Lock
from time import time, sleep
import traceback, sys, requests
from config import *
import praw
from social.apps.django_app.utils import load_strategy

r = praw.Reddit(user_agent=REDDIT_USERAGENT, api_request_delay=1.0, cache_timeout=60)

def refresh_access(user):
	if user and user.is_authenticated():
		social = user.social_auth.get(provider="reddit")
		#social.refresh_token(redirect_uri=SOCIAL_AUTH_REDDIT_REDIRECT)
		#social.refresh_token(social.extra_data["refresh_token"], redirect_uri=SOCIAL_AUTH_REDDIT_REDIRECT)
		strategy = load_strategy()
		social.refresh_token(strategy, redirect_uri=SOCIAL_AUTH_REDDIT_REDIRECT)

_method_lock = Lock()
_last_call = 0
_rate_limit = 1.0

def uses_api(function):
	@wraps(function)
	def wrapper(*args, **kwargs):
		time_diff = time() - _last_call
		if _rate_limit > time_diff > 0:
			sleep(time_diff)
		with _method_lock:
			return function(*args, **kwargs)
	return wrapper

def use_user(user):
	if not user.is_authenticated():
		return None
	social = user.social_auth.get(provider="reddit")
	token = social.extra_data["access_token"]
	#print("Access token: {}".format(token))
	
	r.set_oauth_app_info(SOCIAL_AUTH_REDDIT_KEY, SOCIAL_AUTH_REDDIT_SECRET, SOCIAL_AUTH_REDDIT_REDIRECT)
	r.set_access_credentials(REDDIT_OAUTH_SCOPES, access_token=token, update_user=False)
	return token

def get_message_body_html(user, message_id, offset=0):
	#fuckpraw
	
	access_token = use_user(user)
	if access_token:
		try:
			@lru_cache(maxsize=100)
			@uses_api
			def get_response(message_id):
				print("Getting message: {}".format(message_id))
				headers = {"Authorization": "bearer " + access_token, "User-Agent": REDDIT_USERAGENT}
				url = "https://oauth.reddit.com/message/messages/" + message_id + "?raw_json=1"
				response = requests.get(url, headers=headers)
				return response.json()
			
			messages_json = get_response(message_id)
			if "error" in messages_json and messages_json["error"] == 401:
				refresh_access(user)
				access_token = use_user(user)
				messages_json = get_response(message_id)
			
			if "data" in messages_json and len(messages_json["data"]) > 0:
				messages_json = messages_json["data"]
				if "children" in messages_json and len(messages_json["children"]) > 0:
					message_json = messages_json["children"][0]["data"]
					# If offset, check for replies
					if offset > 0 and message_json["replies"] != "":
						replies = message_json["replies"]["data"]["children"]
						if offset-1 < len(replies) > 0:
							message_json = replies[offset-1]["data"]
					
					message = praw.objects.RedditContentObject.from_api_response(r, message_json)
					return message.body_html
				else:
					print("\tNo children!")
					print(messages_json)
			else:
				print("\tNo data!")
				print(messages_json)
		
		except Exception as e:
			ex_type, ex, tb = sys.exc_info()
			print("Unknown error: {} ({})".format(e, ex_type))
			traceback.print_tb(tb)
			del tb
