from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$',views.index),
    url(r'^add', views.add),
    url(r'^login',views.login),
    url(r'^quotes', views.userquotes),
    url(r'^users/(?P<id>\d+)$', views.showuser),
    url(r'^newquote', views.newquote),
    url(r'^favorites', views.fav),
    url(r'^removefav', views.removefav),
]
