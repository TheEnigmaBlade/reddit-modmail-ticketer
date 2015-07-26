def create_user_from_oauth(backend, user, response, *args, **kwargs):
	from main.models import Redditor
	redditors = Redditor.objects.filter(name=response["name"])
	num_known = len(redditors)
	
	# Redditor created by bot
	if num_known > 0:
		redditor = redditors[0]
		if redditor.user is None:
			redditor.user = user
			redditor.save()
	# Redditor unknown
	elif num_known == 0:
		redditor = Redditor(id=response["id"], name=response["name"])
		redditor.user = user
		redditor.save()
