from django.conf.urls import url
from . import views
                    
urlpatterns = [
    url(r'^$', views.index),
    
    url(r'^wishes$', views.wishes),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^logout$', views.logout),
    url(r'^wishes/new$', views.new),
    url(r'^create_wish$', views.create_wish),
    url(r'^wishes/edit/(?P<wish_id>\d+)$', views.edit),
    url(r'^remove/(?P<wish_id>\d+)$', views.remove),
    url(r'^editing/(?P<wish_id>\d+)$', views.editing),
    url(r'^grant_wish/(?P<wish_id>\d+)$', views.grant_wish),
    url(r'^wishes/stats$', views.stats),
    url(r'^like/(?P<wish_id>\d+)$',views.like),
]