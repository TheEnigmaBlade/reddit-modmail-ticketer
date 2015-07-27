from collections import deque, Iterable
from abc import ABCMeta, abstractmethod
import bz2, pickle, os
from time import sleep

os.chdir(os.path.dirname(os.path.abspath(__file__)))

def load_thing_cache(cache_file, default_size=1000):
	if cache_file is not None and os.path.exists(cache_file):
		print("Loading thing cache: {0}".format(cache_file))
		with bz2.open(cache_file, "rb") as file:
			try:
				cache = pickle.load(file)
				return cache
			except pickle.PickleError and EOFError:
				return None
	return ThingCache(cache_size=default_size, file=cache_file)

def load_message_cache(cache_file, default_size=1000):
	if cache_file is not None and os.path.exists(cache_file):
		print("Loading message cache: {0}".format(cache_file))
		with bz2.open(cache_file, "rb") as file:
			try:
				cache = pickle.load(file)
				return cache
			except pickle.PickleError and EOFError:
				return None
	return MessageCache(cache_size=default_size, file=cache_file)

class Cache(Iterable, metaclass=ABCMeta):
	def __init__(self, cache_file):
		self.cache_file = cache_file
	
	def __setitem__(self, key, value):
		pass
	
	@abstractmethod
	def __iter__(self):
		return None
	
	@abstractmethod
	def data(self):
		return None
	
	def save(self):
		if self.cache_file is not None:
			with bz2.open(self.cache_file, "wb") as file:
				pickle.dump(self, file)

class ThingCache(Cache):
	def __init__(self, cache_size=1000, file=None):
		super().__init__(file)
		
		self._post_ids = deque()
		self._post_ids_max = cache_size
	
	def _add_post_ids(self, post_ids):
		#Remove old posts
		new_len = len(self._post_ids) + len(post_ids)
		if new_len > self._post_ids_max:
			for n in range(0, new_len - self._post_ids_max):
				self._post_ids.popleft()
		#Add new posts
		for postID in post_ids:
			self._post_ids.append(postID)
		
		self.save()
	
	def get_diff(self, posts):
		posts = list(posts)
				
		#Get IDs not in the cache
		new_post_ids = [post.id for post in posts]
		new_post_ids = list(set(new_post_ids).difference(set(self._post_ids)))
				
		#Get new posts from IDs
		new_posts = []
		for postID in new_post_ids:
			for post in posts:
				if post.id == postID:
					new_posts.append(post)
		
		#Update cache
		self._add_post_ids(new_post_ids)
		
		return new_posts
	
	@property
	def data(self):
		return self._post_ids
	
	def __iter__(self):
		return self._post_ids.__iter__()

class MessageCache(ThingCache):
	def __init__(self, cache_size=1000, file=None):
		super().__init__(cache_size=cache_size, file=file)
	
	def get_diff(self, posts):
		# Retrieve post listing from server, make sure new messages don't get lost
		tries = 0
		while type(posts) != list and tries < 6:
			try:
				posts = list(posts)
			except:
				tries += 1
				sleep(5)
		if type(posts) != list:
			return list()
		
		# Process posts
		new_posts = list()
		new_post_ids = list()
		for post in posts:
			new_post_id = post.id
			new_post_replies = len(post.replies)
			
			found = False
			for old_post_id, old_post_replies in self._post_ids:
				if new_post_id == old_post_id:
					if new_post_replies == old_post_replies:
						found = True
			
			if not found:
				new_posts.append(post)
				new_post_ids.append((new_post_id, new_post_replies))
		
		self._add_post_ids(new_post_ids)
		
		return new_posts
