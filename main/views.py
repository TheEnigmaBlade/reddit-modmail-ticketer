from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseForbidden, HttpResponseBadRequest, Http404
from django.views.decorators.http import require_safe, require_POST, require_GET
from django.contrib import auth
from django.shortcuts import render, redirect, get_object_or_404
from main.forms import SubredditForm
from main.templatetags.stringify import get_status_class, get_status_label_class, get_status_string

from .models import Subreddit, Redditor, Ticket
from .func import reddit_util

@require_safe
def index(request):
	return render_main_page(request)

@require_safe
def help(request):
	raise Http404()

@require_safe
def subreddit_all(request, subreddit):
	return render_main_page(request, subreddit)

@require_safe
def subreddit_open(request, subreddit):
	return render_main_page(request, subreddit, status_filter=Ticket.Status.OPEN)

@require_safe
def subreddit_active(request, subreddit):
	return render_main_page(request, subreddit, status_filter=Ticket.Status.ACTIVE)

@require_safe
def subreddit_closed(request, subreddit):
	return render_main_page(request, subreddit, status_filter=Ticket.Status.CLOSED)

@require_safe
def subreddit_ignored(request, subreddit):
	return render_main_page(request, subreddit, status_filter=Ticket.Status.IGNORED)

@require_safe
def subreddit_mine(request, subreddit):
	return render_main_page(request, subreddit, custom_filter="mine")

def render_main_page(request, subreddit=None, status_filter=None, custom_filter=None, order=None, limit=100):
	if subreddit is None:
		return render(request, "main/index.jinja")
	
	# Subreddit info
	subreddit = get_subreddit(subreddit)
	if subreddit is None:
		return render_subreddit_404(request, subreddit)
	if not subreddit.user_moderates(request.user) or not subreddit.enabled:
		return render_subreddit_401(request, subreddit)
	
	# Get ticket list
	print("Status: {}".format(status_filter))
	if status_filter is not None:
		tickets = subreddit.get_status_tickets(status_filter)
	elif custom_filter is not None:
		if custom_filter == "mine":
			tickets = subreddit.get_user_tickets(request.user.redditor)
		else:
			print("Warning: Invalid custom ticket filter")
			tickets = subreddit.ticket_set.all()
	else:
		tickets = subreddit.ticket_set.all()
	
	# Apply modifiers to ticket list
	tickets = tickets.order_by("-id" if order is None else order)
	tickets = tickets[:limit]
	
	return render(request, "main/subreddit.jinja", {"subreddit": subreddit, "tickets": tickets, "status_filter": status_filter, "custom_filter": custom_filter})

@login_required
def subreddit_config(request, subreddit):
	# Subreddit info
	subreddit = get_subreddit(subreddit)
	if subreddit is None:
		return render_subreddit_404(request, subreddit)
	if not subreddit.user_moderates(request.user) or not subreddit.enabled:
		return render_subreddit_401(request, subreddit)
	
	if request.method == "POST":
		form = SubredditForm(request.POST, instance=subreddit)
		if form.is_valid():
			form.save()
			return redirect("main:subreddit", subreddit.name)
	else:
		form = SubredditForm(instance=subreddit)
		return render(request, "main/subreddit_config.jinja", {"subreddit": subreddit, "form": form, "custom_filter": "settings"})

# Authentication

def logout(request):
	#request.session["token"] = None
	#request.session.flush()
	auth.logout(request)
	return redirect("/")

# Other

def handler404(request):
	resp = render(request, "main/404.jinja")
	resp.status_code = 404
	return resp

# API methods

@login_required
@require_POST
def modify_ticket(request, ticket_id):
	print("Modifying ticket {}".format(ticket_id))
	ticket = get_object_or_404(Ticket, id=ticket_id)
	if not ticket.subreddit.user_moderates(request.user):
		return HttpResponseForbidden()
	
	def finalize_success():
		ticket.modified_by = request.user.redditor
		ticket.save()
	
	# Find and perform the operation
	if "inc_status" in request.GET:
		inc_status = request.GET["inc_status"]
		status = Ticket.Status[inc_status.upper()]
		# Increment the status
		if status < Ticket.Status.CLOSED:
			status += 1
		else:
			return JsonResponse({"success": False})
		
		# Update status
		ticket.status = status
		finalize_success()
		
		return JsonResponse({
			"success": True,
			"status": get_status_class(status),
			"status_class": get_status_label_class(status),
			"status_text": get_status_string(status)
		})
	if "set_status" in request.GET:
		set_status = request.GET["set_status"]
		status = Ticket.Status[set_status.upper()]
		
		# Update status
		ticket.status = status
		finalize_success()
		
		return JsonResponse({
			"success": True,
			"status": get_status_class(status),
			"status_class": get_status_label_class(status),
			"status_text": get_status_string(status)
		})
	if "set_flagged" in request.GET:
		set_flagged = request.GET["set_flagged"] == "1"
		if (set_flagged and not ticket.is_flagged) or (not set_flagged and ticket.is_flagged):
			ticket.is_flagged = set_flagged
			ticket.save()
			print(ticket.is_flagged)
		
		return JsonResponse({
			"success": True,
			"flagged":  set_flagged
		})
	
	return HttpResponseBadRequest()

@login_required
@require_GET
def get_message_body(request, ticket_id):
	print("Getting message text {}".format(ticket_id))
	ticket = get_object_or_404(Ticket, id=ticket_id)
	if not ticket.subreddit.user_moderates(request.user):
		return HttpResponseForbidden()
	
	if ticket.type == Ticket.Type.BAN:
		message = reddit_util.get_message_body_html(request.user, ticket.message.id, offset=1)
	else:
		message = reddit_util.get_message_body_html(request.user, ticket.message.id)
	
	if message:
		return JsonResponse({
				"success": True,
				"message": message,
			})
	
	return JsonResponse({
			"success": False
		})

# Util

def get_subreddit(subreddit):
	try:
		return Subreddit.objects.get(name=subreddit)
	except Subreddit.DoesNotExist:
		return None
	except Subreddit.MultipleObjectsReturned:
		print("This should never happen!")
		return None

def render_subreddit_404(request, subreddit):
	return render(request, "main/subreddit_error.jinja", {"subreddit": subreddit, "error": "that subreddit does not exist"})

def render_subreddit_401(request, subreddit):
	return render(request, "main/subreddit_error.jinja", {"subreddit": subreddit, "error": "you are not authorized to view that subreddit"})
