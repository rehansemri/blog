from django.urls import path
from . import views
urlpatterns = [
    path('',views.home,name='home'),
    path('login',views.login,name='login'),
    path('register',views.register,name='register'),
    path('logout',views.logout,name='logout'),
    path('post/<str:pk>',views.post,name='post'),
    path('comment/<str:pk>',views.comment,name='comment'),
    path('add_post',views.add_post,name='add_post'),
    path('profile/<str:pk>',views.profile,name='profile'),
    path('delete_post/<str:pk>',views.delete_post,name='delete_post'),


]