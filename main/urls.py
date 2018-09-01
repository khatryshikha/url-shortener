from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.index_page, name ='index'),
    url(r'^(?P<slug>[-\w]+)/$', views.redirect_view)
]