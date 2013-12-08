from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'm_learning.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

url(r'^admin/', include(admin.site.urls)),
url(r'blog/', 'blog.views.index'),
url(r'artists/', 'meta.views.index'),
# ,url(r'^blog/', include(blog.site.urls))
)

# (r'^$', 'blog.views.index'),
# url(
#     r'^blog/view/(?P<slug>[^\.]+).html', 
#     'blog.views.view_post', 
#     name='view_blog_post'),
# url(
#     r'^blog/category/(?P<slug>[^\.]+).html', 
#     'blog.views.view_category', 
#     name='view_blog_category'),
