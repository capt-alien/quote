from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.regester),
    url(r'^loggin$', views.login),
    url(r'^wall$', views.wall),
    url(r'^add_quote$', views.add_quote)


]
