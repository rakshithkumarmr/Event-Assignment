from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name="home"),
    path('login/',views.login,name='login'),
    path('signup/',views.signup,name='signup'),
    path('logout_user/',views.logout_user,name='logout_user'),
    path('upload_post/', views.create_event, name='create_event'),
    path('like_post/', views.like_post, name='like_post'),
    path('my_likes/', views.my_likes, name='my_likes'),
]