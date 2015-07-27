from django_jinja import library
from widget_tweaks.templatetags import widget_tweaks

@library.filter()
def add_class(field, css_class):
	return widget_tweaks.add_class(field, css_class)
