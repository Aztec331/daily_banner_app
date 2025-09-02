from django.urls import path
from .views import BusinessProfileView

urlpatterns = [
    path('business-profile/', BusinessProfileView.as_view()),
]
