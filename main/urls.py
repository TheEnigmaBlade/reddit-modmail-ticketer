from django.contrib import admin
from django.conf.urls import url
from . import views

urlpatterns = [
	url("^$", views.index, name="index"),
	url("^help/$", views.help, name="help"),
	url("^logout/$", views.logout, name="logout"),
	
	url("^r/(?P<subreddit>[a-zA-Z0-9_]+)/$", views.subreddit_all, name="subreddit"),
	url("^r/(?P<subreddit>[a-zA-Z0-9_]+)/all/$", views.subreddit_all, name="subreddit_all"),
	url("^r/(?P<subreddit>[a-zA-Z0-9_]+)/open/$", views.subreddit_open, name="subreddit_open"),
	url("^r/(?P<subreddit>[a-zA-Z0-9_]+)/active/$", views.subreddit_active, name="subreddit_active"),
	url("^r/(?P<subreddit>[a-zA-Z0-9_]+)/closed/$", views.subreddit_closed, name="subreddit_closed"),
	url("^r/(?P<subreddit>[a-zA-Z0-9_]+)/ignored/$", views.subreddit_ignored, name="subreddit_ignored"),
	url("^r/(?P<subreddit>[a-zA-Z0-9_]+)/mine/$", views.subreddit_mine, name="subreddit_mine"),
	url("^r/(?P<subreddit>[a-zA-Z0-9_]+)/settings/$", views.subreddit_config, name="subreddit_config"),
	
	url("^api/ticket/(?P<ticket_id>[a-zA-Z0-9]+)/$", views.get_message_body, name="get_message_body"),
	url("^api/ticket/(?P<ticket_id>[a-zA-Z0-9]+)/modify/$", views.modify_ticket, name="modify_ticket"),
]

admin.site.site_title = "Modmail Ticketer"
admin.site.site_header = "Modmail Ticketer Administration"
#admin.site.index_title = "Site administration"
