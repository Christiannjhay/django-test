from django.urls import path
from .views import RegisterView, LoginView, UserProfileView, UserOutfitView, ImagesCreateView

urlpatterns = [
    path('user/outfit/', UserOutfitView.as_view(), name='user_outfit'),
    path('user/profile/', UserProfileView.as_view(), name='user_profile'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('upload/', ImagesCreateView.as_view(), name='upload'),
]
