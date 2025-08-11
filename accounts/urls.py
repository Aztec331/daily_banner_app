from django.urls import path
from .views import RegisterView, LoginView,LogoutView, UserProfileView
#from rest_framework.authtoken.views import obtain_auth_token
urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    # path('login/', obtain_auth_token, name='api-token-auth'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('user/profile/', UserProfileView.as_view(), name='user-profile'),
]
