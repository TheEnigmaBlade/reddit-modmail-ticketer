def create_user_from_oauth(backend, user, response, *args, **kwargs):
	from main.models import Redditor
	print("New user: {}".format(user.username))
	redditors = Redditor.objects.filter(name=user.username)
	if len(redditors) > 0:
		redditors[0].user = user
		redditors[0].save()
