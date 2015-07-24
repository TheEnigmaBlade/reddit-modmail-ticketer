from django.db.models import Q
import re

# See: http://julienphalip.com/post/2825034077/adding-search-to-a-django-site-in-a-snap

_terms_pattern = re.compile("['\"]([^'\"]+)['\"]|(\S+)")
_space_normalizer = re.compile("\s{2,}")

def _get_query_terms(query):
	terms = _terms_pattern.findall(query)
	return [_space_normalizer.sub(" ", (term[0] or term[1])) for term in terms]

def create_query(query_text, fields):
	and_query = Q()
	terms = _get_query_terms(query_text)
	for term in terms:
		or_query = Q()
		for field in fields:
			or_query |= Q(**{"{}__icontains".format(field): term})
		and_query &= or_query
	return and_query
