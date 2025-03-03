from django.urls import path
from  account import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.index, name='index'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logged_out/', auth_views.LogoutView.as_view(), name='logged_out'),
    path('change_passwords/', auth_views.PasswordChangeView.as_view(), name='change_passwords'),
    path('change_passwords/done/', auth_views.PasswordChangeDoneView.as_view(), name='change_passwords_done'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('register/', views.register, name='register'),
    path('edit/', views.edit, name='edit'),
    path('speech_translate', views.transcribe, name='speech_translate'),
    path('upload/', views.upload_audio, name='upload'),
]