DEBUG = True

useragent			= "script:Modmail Ticketer Backend:v0.2dev (by /u/TheEnigmaBlade)"
if DEBUG:
	oauth_id		= "eu7AvirqDEuQeA"
	oauth_secret	= "xQCmbClGmWMRDz4oMiFXGz2TWhU"
else:
	oauth_id		= "9Lu56bhu1qSP2w"
	oauth_secret	= "spsiU-UA0olu1g0WSl7a4Bc4t78"
username			= "ModmailConductor"
password			= "cQ*$%7Xu,r5B]6~\">)SO+y8lB9o%_}do"
#username			= "LeagueOfLegendsBot"
#password			= "ihopetheydontstealthispassword"

cache_location		= "msg_caches"

if DEBUG:
	state_update_length	= 1200
else:
	state_update_length = 60
