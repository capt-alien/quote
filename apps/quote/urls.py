from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.regester),
    url(r'^loggin$', views.login),
    url(r'^wall$', views.wall),
    url(r'^wall/(?P<id>\d+)$', views.user_posts),
    url(r'^add_quote$', views.add_quote),
    url(r'^user/edit/(?P<id>\d+)$', views.edit_to_account),
    url(r'^user/editing/(?P<id>\d+)$', views.edit_account),
    url(r'^logout$', views.logout),

]
