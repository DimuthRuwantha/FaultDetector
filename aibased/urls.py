from django.conf.urls import url
from . import views

app_name = 'aibased'

urlpatterns = [
    # /aibased/
    url(r'^$', views.IndexView.as_view(), name='index'),
    # /aibased/monitor
    url(r'^monitor$', views.Monitor.as_view(), name='monitor'),

    # /aibased/ann
    url(r'^ann$', views.NeuralNetwork.as_view(), name='ann'),

    # music/album/register
    url(r'^signup/$', views.UserRegistrationView.as_view(), name='user-signup'),

    # music/album/login
    url(r'^login/$', views.UserLoginView.as_view(), name='user-login'),

    # music/album/logout
    url(r'^logout/$', views.UserLogoutView.as_view(), name='user-logout'),

]
