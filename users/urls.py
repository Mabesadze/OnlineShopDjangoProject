from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('logout/', views.logoutUserView.as_view(), name='logout'),
    path('login/', views.loginUserView.as_view(), name='login'),
    path('register/', views.RegisterView.as_view(), name='registration'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
]