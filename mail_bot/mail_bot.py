# Set up Django database and models

import os, django
import ModmailTicketer.settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ModmailTicketer.settings")
django.setup()

from main.models import Subreddit, Redditor, Message, Ticket

# Start bot stuff

import traceback, sys, re
from threading import Event
from time import time
from requests import HTTPError
from praw.errors import ModeratorRequired, ModeratorOrScopeRequired
import reddit_util, cache as cache_util, bot_config as config

r = None
message_caches = dict()

running = True
waitEvent = Event()

# Database management

def enable_subreddit(sub_info):
	sub_id = sub_info.id
	subs = Subreddit.objects.filter(id=sub_id)
	if subs.count() > 0:
		sub = subs[0]
		if not sub.enabled:
			sub.enabled = True
			sub.save()
		else:
			print("\tSubreddit already enabled")
	else:
		sub_name = sub_info.display_name.lower()
		sub = Subreddit(id=sub_id, name=sub_name)
		sub.save()

def disable_subreddit(sub_id):
	subs = Subreddit.objects.filter(id=sub_id)
	if subs.count() > 0:
		sub = subs[0]
		if sub.enabled:
			sub.enabled = False
			sub.save()
			del message_caches[sub.id]
		else:
			print("Subreddit already disabled")

def set_subreddit_permissions(sub, mods):
	try:
		sub_model = Subreddit.objects.get(id=sub.id)
		model_mods_dict = {mod.id: mod for mod in sub_model.moderators.all()}
		model_mods = set(model_mods_dict.keys())
		reddit_mods_dict = {mod.id: mod for mod in mods}
		reddit_mods = {mod.id for mod in mods}
		mod_diff = model_mods ^ reddit_mods
		print("\tMod diff: {}".format(mod_diff))
		
		for mod_id in mod_diff:
			# Remove old mods
			if mod_id in model_mods:
				mod = Redditor.objects.get(id=mod_id)
				sub_model.moderators.remove(mod)
				
			# Add new mods
			else:
				db_mods = Redditor.objects.filter(id=mod_id)
				# Mod already living in the database
				if db_mods.count() > 0:
					mod = db_mods[0]
				# Mod needs to be created
				else:
					mod_info = reddit_mods_dict[mod_id]
					mod = Redditor.objects.create(id=mod_id, name=mod_info.name)
				
				# Make mod a mod
				sub_model.moderators.add(mod)
		
		# Save database
		if len(mod_diff) > 0:
			sub_model.save()
			
	except:
		ex_type, ex, tb = sys.exc_info()
		print("Failed to set subreddit permissions for /r/{}: {} ({})".format(sub.display_name, ex, ex_type))
		traceback.print_tb(tb)
		del tb

def get_subreddit_messages(sub_id, sub_name):
	messages = r.get_mod_mail(sub_name)
	cache = message_caches[sub_id]
	return cache.get_diff(messages)

def create_message_model(message_info):
	return Message.objects.create(id=message_info.id, subject=message_info.subject, sender=message_info.author.name, sender_id=message_info.author.id)

def create_ticket_model(message_info, message, sub):
	ttype = get_ticket_type(message_info, sub)
	print("\tType: {}".format(repr(Ticket.Type(ttype))))
	ticket = Ticket.objects.create(message=message, subreddit=sub, type=ttype)
	
	# Special modifications
	if ttype == Ticket.Type.BAN:
		message.subject = "Ban message for /u/" + message_info.dest
		print("New subject: {}".format(message.subject))
		message.save()
	if ttype == Ticket.Type.MOD:
		ticket.status = Ticket.Status.ACTIVE
		ticket.save()
	
	return ticket

# Analysis

_ban_subject_match = re.compile("^you've been( temporarily)? banned from /r/[a-z0-9_]+", re.IGNORECASE)
_ban_body_match = re.compile("^you have been( temporarily)? banned from posting to /r/[a-z0-9_]+\.", re.IGNORECASE)

def get_ticket_type(message_info, sub):
	# Check for ban message
	if _ban_subject_match.match(message_info.subject) and _ban_body_match.match(message_info.body):
		return Ticket.Type.BAN
	
	# Check for bot message
	bots = sub.bots.lower().split(",")
	if message_info.author.name.lower()in bots:
		return Ticket.Type.BOT
	
	# Check for distinguished message
	if message_info.distinguished:
		if message_info.distinguished == "moderator":
			return Ticket.Type.MOD
		if message_info.distinguished == "admin":
			return Ticket.Type.ADMIN
	
	# Just a boring ol' normal message :(
	return Ticket.Type.NORMAL

# Looping stuff

def process_loop():
	global r, running
	
	r = reddit_util.init_reddit_session()
	os.makedirs(config.cache_location, exist_ok=True)
	state_update_time = 0
	
	# Run the thing!
	while running:
		try:
			r = reddit_util.renew_reddit_session(r)
			
			if time() - state_update_time >= config.state_update_length:
				state_update_time = time()
				
				# Get moderated subreddits
				mod_subs = r.get_my_moderation()
				mod_subs = {sub.id: sub for sub in mod_subs}
				mod_sub_ids = set(mod_subs.keys())
				print("Mod subs: {}".format(mod_sub_ids))
				cache_sub_ids = set(message_caches.keys())
				print("Cache subs: {}".format(cache_sub_ids))
				
				# Add new subreddits
				new_subs = mod_sub_ids - cache_sub_ids
				print("New subs: {}".format(new_subs))
				for sub_id in new_subs:
					print("\tEnabling {}".format(sub_id))
					sub = mod_subs[sub_id]
					if "mail" in sub.mod_permissions or "all" in sub.mod_permissions:
						enable_subreddit(sub)
						cache = cache_util.load_thing_cache(config.cache_location+"/"+sub_id+".cache")
						message_caches[sub_id] = cache
						# Build initial cache
						get_subreddit_messages(sub_id, sub.display_name)
					else:
						print("\t\tError: no mail permissions")
				# Remove old subreddits
				old_subs = cache_sub_ids - mod_sub_ids
				print("Old subs: {}".format(old_subs))
				for sub_id in old_subs:
					print("\tDisabling {}".format(sub_id))
					disable_subreddit(sub_id)
					message_caches[sub_id].save()
					del message_caches[sub_id]
				
				# Check user permissions
				for sub_id in mod_sub_ids:
					sub = mod_subs[sub_id]
					print("Setting permissions on /r/{}".format(sub.display_name))
					mods = list(sub.get_moderators())
					set_subreddit_permissions(sub, mods)
			
			# Check for new messages
			for sub_id in message_caches.keys():
				sub = Subreddit.objects.get(id=sub_id)
				new_messages = get_subreddit_messages(sub.id, sub.name)
				for message_info in new_messages:
					print(vars(message_info))
					message = Message.objects.filter(id=message_info.id)
					if message.count() == 0:
						print("Is new message")
						message = create_message_model(message_info)
						create_ticket_model(message_info, message, sub)
					else:
						print("Is reply")
			
			if running and waitEvent.wait(timeout=20):
				break
			
		except (ModeratorRequired, ModeratorOrScopeRequired, HTTPError) as e:
			if not isinstance(e, HTTPError) or e.response.status_code == 403:
				print("Error: No moderator permission")
			ex_type, ex, tb = sys.exc_info()
			print("Error: {}".format(e))
			traceback.print_tb(tb)
			del tb
			if running and waitEvent.wait(timeout=30):
				break
		except KeyboardInterrupt:
			print("Stopped with keyboard interrupt")
			running = False
		except Exception as e:
			ex_type, ex, tb = sys.exc_info()
			print("Unknown error: {} ({})".format(e, ex_type))
			traceback.print_tb(tb)
			del tb
			#running = False
			
def main():
	process_loop()
	reddit_util.destroy_reddit_session(r)

if __name__ == "__main__":
	main()
