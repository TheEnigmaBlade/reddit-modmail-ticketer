from django_jinja import library
from main.models import Ticket

@library.global_function
def get_type_string(status):
	if status == Ticket.Type.NORMAL:
		return ""
	if status == Ticket.Type.BOT:
		return "BOT"
	if status == Ticket.Type.BAN:
		return "BAN"
	if status == Ticket.Type.MOD:
		return "MOD"
	if status == Ticket.Type.ADMIN:
		return "ADMIN"
	return ""

@library.global_function
def get_type_label_class(status):
	if status == Ticket.Type.NORMAL:
		return "none"
	if status == Ticket.Type.BOT:
		return "default"
	if status == Ticket.Type.BAN:
		return "info"
	if status == Ticket.Type.MOD:
		return "success"
	if status == Ticket.Type.ADMIN:
		return "danger"
	return "none"

@library.global_function
def get_status_string(status):
	if status == Ticket.Status.OPEN:
		return "Open"
	if status == Ticket.Status.ACTIVE:
		return "Active"
	if status == Ticket.Status.CLOSED:
		return "Closed"
	if status == Ticket.Status.IGNORED:
		return "Ignored"
	return ""

@library.global_function
def get_status_class(status):
	if status == Ticket.Status.OPEN:
		return "open"
	if status == Ticket.Status.ACTIVE:
		return "active"
	if status == Ticket.Status.CLOSED:
		return "closed"
	if status == Ticket.Status.IGNORED:
		return "ignored"
	return None

@library.global_function
def get_status_label_class(status):
	if status == Ticket.Status.OPEN:
		return "success"
	if status == Ticket.Status.ACTIVE:
		return "primary"
	if status == Ticket.Status.CLOSED:
		return "default"
	if status == Ticket.Status.IGNORED:
		return "danger"
	return "default"

@library.global_function
def get_message_url(message_id):
	return "http://reddit.com/message/messages/"+message_id

@library.global_function
def get_redditor_url(redditor_name):
	return "http://reddit.com/u/"+redditor_name
