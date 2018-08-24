from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.dashboard),

    url(r'account_info$', views.account_info),
    url(r'add_user$', views.add_user),
    url(r'account_edit$', views.account_edit),
    url(r'change_password$', views.change_password),
    url(r'change_password_proc$', views.change_password),

    url(r'conversion_upload$', views.conversion_upload),
    url(r'delete_upload/(?P<upload_id>\d+)$', views.delete_upload),
    url(r'feedback$', views.feedback),
    url(r'delete_feedback/(?P<feedbackid>\d+)$', views.delete_feedback),
    url(r'subscription$', views.subscription),
    url(r'subscribers_search$', views.subscribers_search),
    url(r'unsubscribe/(?P<sub_id>\d+)$', views.unsubscribe),
    url(r'unsubscribe_ajax/(?P<sub_id>\d+)$', views.unsubscribe_ajax),
    url(r'^wall$', views.wall),
    url(r'post_proc$', views.post_proc),
    url(r'delete_post/(?P<post_id>\d+)$', views.delete_post),
    url(r'demo', views.demo),
    url(r'all.json', views.all_json),
    url(r'all.html', views.all_html),
    url(r'find', views.find),

]