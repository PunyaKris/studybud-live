from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_page, name = "home page"),
    path('login/', views.loginPage, name = "login"),
    path('logout/', views.logoutUser, name = "logout"),
    path('register/', views.registerPage, name = "register"),
    path('profile/<str:pk>/', views.userProfile, name = "user-profile"),
    path('create-room/', views.create_room, name = "create-room"),
    path('room/<str:pk>', views.room_page, name = "room page"),
    path('update-room/<str:pk>', views.update_room, name = "update-room"),
    path('delete-room/<str:pk>', views.delete_room, name = "delete-room"),
    path('delete-comment/<str:pk>', views.delete_comment, name = "delete-comment"),
    path('update-user/', views.update_user, name = "update-user"),
    path('browse-topics/', views.browse_topics, name = "browse-topics"),
    path('recent-activities/', views.recent_activities, name = "recent-activities"),
]