from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('friend/create/', views.create_friend, name='create_friend'),
    path('friend/update/<int:pk>/', views.update_friend, name='update_friend'),
    path('friend/delete/<int:pk>/', views.delete_friend, name='delete_friend'),
    path('api/friends/', views.friends_api, name='friends_api'),
]
