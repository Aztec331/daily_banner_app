from django.urls import path
from .views import (
    UserBusinessListView,
    BusinessCreateView,
    BusinessUpdateView,
    BusinessDeleteView
)

urlpatterns = [
    path('user/businesses/', UserBusinessListView.as_view(), name='user-businesses'),
    path('business/', BusinessCreateView.as_view(), name='business-create'),
    path('business/<int:pk>/', BusinessUpdateView.as_view(), name='business-update'),
    path('business/<int:pk>/delete/', BusinessDeleteView.as_view(), name='business-delete'),
]
