from django.urls import path
from .views import *


urlpatterns = [
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('refresh/', refresh_token_view, name='refresh'),
    path('logout/', logout_view, name='logout'),
    path('profile/', profile_view, name='profile'),
]
