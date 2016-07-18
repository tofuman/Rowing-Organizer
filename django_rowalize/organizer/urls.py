
from django.conf.urls import url

from . import views

app_name = 'organizer'

urlpatterns = [
    url(r'^main/$', views.main),
    url(r'^login/$', views.login_user),
    url(r'^logout/', views.logout_user),
]

