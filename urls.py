from django.conf import settings
from django.conf.urls.defaults import patterns, include, url
from josh.views import Amazon

urlpatterns = patterns('',
        url(r'amazon$', Amazon.as_view()),
)
