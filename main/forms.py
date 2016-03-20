from django.forms import forms, fields, ModelForm
from main.models import Subreddit

class SubredditForm(ModelForm):
	class Meta:
		model = Subreddit
		fields = ["bots", "hl_users",
				  "auto_respond",
				  "auto_respond_new", "auto_respond_new_text",
				  "auto_respond_closed", "auto_respond_closed_text"]
