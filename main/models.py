from django.db import models
from django.contrib.auth.models import User

import enum
from django.db.models import Q


class Redditor(models.Model):
	id = models.CharField(max_length=5, primary_key=True)
	user = models.OneToOneField(User, blank=True, null=True)
	name = models.CharField(max_length=20)
	
	def get_subreddits(self):
		return self.moderates_set.all().order_by("name")
	
	def __str__(self):
		return "/u/{}".format(self.name)

class Subreddit(models.Model):
	id = models.CharField(max_length=5, primary_key=True)
	name = models.CharField(max_length=20)
	moderators = models.ManyToManyField(Redditor, related_name="moderates_set")
	
	enabled = models.BooleanField(default=True)
	bots = models.CharField(max_length=209, default="AutoModerator", blank=True)
	hl_users = models.CharField(max_length=209, default="", blank=True)
	
	auto_respond = models.BooleanField(default=False)
	auto_respond_new = models.BooleanField(default=True)
	auto_respond_new_text = models.TextField(max_length=800, blank=True, default="")
	auto_respond_closed = models.BooleanField(default=False)
	auto_respond_closed_text = models.TextField(max_length=800, blank=True, default="")
	
	def get_status_tickets(self, status):
		if status is None:
			return self.ticket_set.none()
		return self.ticket_set.filter(status=status)
	
	def get_user_tickets(self, redditor):
		if redditor is None:
			return self.ticket_set.none()
		status_q = Q(status=Ticket.Status.ACTIVE)
		status_q |= Q(status=Ticket.Status.OPEN)
		q = Q(status_q)
		q &= Q(modified_by=redditor)
		return self.ticket_set.filter(q)
	
	def get_num_open_tickets(self):
		return self.ticket_set.filter(status=Ticket.Status.OPEN).count()
	
	def get_num_user_tickets(self, redditor):
		return self.get_user_tickets(redditor).count()
	
	def user_moderates(self, user):
		if user is None or not user.is_authenticated():
			return False
		return self.moderators.filter(user=user).count() > 0
	
	def __str__(self):
		return "/r/{}".format(self.name)

class Message(models.Model):
	id = models.CharField(max_length=6, primary_key=True)
	subject = models.CharField(max_length=100, blank=True)
	sender = models.CharField(max_length=20, blank=True)
	sender_id = models.CharField(max_length=5, blank=True)
	
	def get_num_replies(self):
		return self.replies.count()
	
	def __str__(self):
		return "Message {}".format(self.pk)

class MessageReply(models.Model):
	id = models.CharField(max_length=6, primary_key=True)
	sender = models.CharField(max_length=20, blank=True)
	sender_id = models.CharField(max_length=5, blank=True)
	
	trunk_message = models.ForeignKey(Message, related_name="replies")
	parent_reply = models.ForeignKey("self", related_name="replies", blank=True, null=True)

class Ticket(models.Model):
	message = models.OneToOneField(Message)
	subreddit = models.ForeignKey(Subreddit)
	
	date_created = models.DateTimeField(auto_now_add=True, null=True)
	date_edited = models.DateTimeField(auto_now=True, null=True)
	modified_by = models.ForeignKey(Redditor, null=True, blank=True)
	
	is_flagged = models.BooleanField(default=False)
	
	class Type(enum.IntEnum):
		NORMAL = 0
		BAN = 1
		BOT = 2
		MOD = 3
		ADMIN = 4
	type = models.PositiveSmallIntegerField(default=Type.NORMAL.value)
	
	class Status(enum.IntEnum):
		OPEN = 0
		ACTIVE = 1
		CLOSED = 2
		IGNORED = 3
	status = models.PositiveSmallIntegerField(default=Status.OPEN.value)
	
	def __str__(self):
		return "Ticket {}".format(self.pk)
