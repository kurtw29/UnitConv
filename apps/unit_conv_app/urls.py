from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^volume$', views.index_volume),
    url(r'^subscribe$', views.subscribe),
    url(r'^subscribe_proc$', views.subscribe_proc),
    url(r'^feedback$', views.feedback),
    url(r'^feedback_proc$', views.feedback_proc),
    url(r'^loginReg$', views.loginReg),
    url(r'reg_process$', views.reg_process),
    url(r'login_process$', views.login_process),
    url(r'logout$', views.logout),
    url(r'^display_image/(?P<numkey>\d+)$', views.display_image),
]