from django.urls import path
from . import views
from .views import register_view
from django.contrib.auth.decorators import login_required
from .views import logout_view
from django.contrib.auth import views as auth_views
from .views import predict_view


urlpatterns = [
    path('', views.home, name='home'),
    path('about',views.about,name="about"),
    path('contact/', views.contact_view, name='contact'),
    path('register/', register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('predict/', predict_view, name='predict'),
    path('logout/', logout_view, name='logout'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
     path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]






