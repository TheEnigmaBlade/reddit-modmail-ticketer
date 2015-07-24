from django_jinja import library
from datetime import datetime
import pytz

@library.global_function
def humanize_date(date):
	if not date:
		return "A long time ago"
	now = datetime.now(pytz.utc)
	
	# Start with seconds.
	diff = (now - date).total_seconds()
	if diff < 60:
		return _humanize_value(diff, "second")
	# Maybe minutes?
	diff /= 60
	if diff < 60:
		return _humanize_value(diff, "minute")
	# Alright, how about hours?
	diff /= 60
	if diff < 24:
		return _humanize_value(diff, "hour")
	# Hmm, days seems like a long time.
	diff /= 24
	if diff < 7:
		return _humanize_value(diff, "day")
	# Really? Has no one checked the tickets?
	diff /= 7
	if diff < 4:
		return _humanize_value(diff, "week")
	# This is getting ridiculous...
	diff /= 4
	if diff < 12:
		return _humanize_value(diff, "month")
	# I'm just going to assume the subreddit died at this point.
	diff /= 12
	if diff < 10000000:
		return _humanize_value(diff, "year")
	# What are you, Q?
	diff /= 10000000
	return _humanize_value(diff, "epoch")

def _humanize_value(val, name):
	val = int(val)
	return "{} {}{} ago".format(val, name, _plural_pls(val))

def _plural_pls(val):
	return "" if val == 1 else "s"
