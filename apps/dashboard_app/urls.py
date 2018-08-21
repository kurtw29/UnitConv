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
    url(r'delete_feedback/(?P<feedback_id>\d+)$', views.delete_feedback),
    url(r'subscription$', views.subscription),
    url(r'unsubscribe/(?P<subscription_id>)$', views.unsubscribe),

    url(r'wall$', views.wall),
    url(r'post_proc$', views.post_proc),
    url(r'delete_post/(?P<post_id>\d+)$', views.delete_post),

]