from django.conf.urls import patterns, include, url

from . import views

urlpatterns = patterns( '',
  url(r'^start/(?P<howMany>[0-9]+)$', views.start),
  url(r'^audio/?$', views.getAudio ),
  url(r'^audio/(?P<audioType>\w+)$', views.getAudio),

  url(r'^image/(?P<index>[0-9]+)$', views.getImage),
  url(r'^try$', views.trySubmission),
  url(r'^$', views.index),
)
