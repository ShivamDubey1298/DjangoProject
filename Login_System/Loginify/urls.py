from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.hello_world, name='hello_world'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    
    # CRUD API URLs
    path('users/', views.get_all_users, name='get_all_users'),
    re_path(r'^users/(?P<email>[^/]+)/$', views.get_user_by_email, name='get_user_by_email'),
    re_path(r'^users/update/(?P<email>[^/]+)/$', views.update_user, name='update_user'),
    re_path(r'^users/delete/(?P<email>[^/]+)/$', views.delete_user, name='delete_user'),
]