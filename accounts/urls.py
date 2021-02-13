from django.urls import path, include
from django.contrib.auth import views as av
from . import views
from .forms import (
    CustomAuthenticationForm, CustomPasswordChangeForm
)


app_name = 'accounts'

urlpatterns = [
    # copy from django.contrib.auth.urls.py
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('', views.AccountsView.as_view(), name='accounts'),
    path('introduce/', views.UserProfileView.as_view(), name='intro'),


    # ページ遷移を変えたい時
    # path('', views.CustomLoginView.as_view(), name='login'),

    path('logout/', views.CustomLogoutView.as_view(), name='logout'),

    # path('password_change/', av.PasswordChangeView.as_view(), name='password_change'),
    # path('password_change/done/', av.PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('password_change/', views.CustomPasswordChangeView.as_view(), name='password_change'),
    path('password_change/done/', views.CustomPasswordChangeDoneView.as_view(), name='password_change_done'),


    # path('password_reset/', av.PasswordResetView.as_view(), name='password_reset'),
    # path('password_reset/done/', av.PasswordResetDoneView.as_view(), name='password_reset_done'),
    # path('reset///', av.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    # path('reset/done/', av.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    path('password_reset/', views.CustomPasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', views.CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset///', av.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', views.CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),
    
    

    path('create/', views.UserCreateView.as_view(), name="create"),
    # path('profile/', views.UserProfileView.as_view(), name="profile"),
    path('change/', views.EmailChangeView.as_view(), name="change"),
]
