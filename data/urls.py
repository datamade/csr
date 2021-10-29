from django.conf.urls import url
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^images/$', views.list_images, name="images"),
    url(r'^taskentry/(?P<image_id>[0-9]+)/$', views.task_entry, name="task_entry"),
    url(r'^logevent/(?P<image_id>[0-9]+)$', views.log_event, name="log_event"),
    url(r'^login/$', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    url(r'^logout/$', auth_views.LogoutView.as_view(), name='logout'),
    url(r'^home_timer/$', views.home_timer, name='home_timer'),
    url(r'^unauthorized/$', views.unauthorized, name='unauthorized'),
]
