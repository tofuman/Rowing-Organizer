from django.conf.urls import url

from . import views

app_name = 'organizer'

urlpatterns = [
    url(r'^main/$', views.main),
    url(r'^login/$', views.login_user),
    url(r'^logout/', views.logout_user),
    url(r'^createuser/$', views.createuser),
    url(r'^createouting/$', views.createouting),
    url(r'^changeouting/$', views.changeOuting),
    url(r'^outing/(?P<eventid>\d+)/$', views.outing),
    url(r'^', views.main),
    url(r'^/$', views.main),
]

