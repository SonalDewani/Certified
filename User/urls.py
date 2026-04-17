from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),

    path('create-manager/', views.create_manager, name='create_manager'),
    path('create-user/', views.create_user, name='create_user'),

    path('profile/', views.profile_view, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('profile/change-password/', views.CustomPasswordChangeView.as_view(), name='change_password'),
]