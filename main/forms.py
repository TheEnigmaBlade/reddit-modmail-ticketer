from django.forms import forms, fields, ModelForm
from main.models import Subreddit

class SubredditForm(ModelForm):
	bots = fields.CharField(required=False, max_length=209,
							label="bots", help_text="bot names separated by a comma, case-insensitive")
	hl_users = fields.CharField(required=False, max_length=209,
							label="highlight users", help_text="user names separated by a comma, case-insensitive")
	
	class Meta:
		model = Subreddit
		fields = ["bots", "hl_users"]
