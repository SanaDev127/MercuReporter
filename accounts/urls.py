from django.urls import path
from .views import SignupPageView
from . import views


urlpatterns = [
    # path("signup/", SignupPageView.as_view(), name="signup"),
    path('login/', views.user_login, name='login'),
    path('register/', views.register, name='register'),
]