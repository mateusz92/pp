from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'pp.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    #url(r'^$', 'main.views.new_message'),

)
