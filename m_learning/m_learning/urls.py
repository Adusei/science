from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'm_learning.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

url(r'^admin/', include(admin.site.urls)),
url(r'^artists/$', 'meta.views.artists'),
url(r'^$', 'listen.views.basic'),
url(r'^sounds/$', 'listen.views.sounds'),


)

