from django.urls import path
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views
from . import views

app_name = 'users'
urlpatterns = [
    path('login/', views.login_request, name="login"),
    path('', views.login_request, name="login"),
    path('otp/<int:id>/', views.otp_request, name="otp"),
    path('homepage/', views.homepage.as_view(), name='homepage'),
    path('register/', views.register_request, name="register"),
    path('logout/', views.logout_request, name="logout"),
    # path('', TemplateView.as_view(template_name='Login/home.html'), name='homepage'),
    path('change_password/',auth_views.PasswordChangeView.as_view(
            template_name='ResetPassword/reset.html',
            success_url = '/'
        ), name='change_password'
    ),
    
]
