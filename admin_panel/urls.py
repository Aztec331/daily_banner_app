from django.urls import path
from .views import(
    AdminUserListView,
    AdminUserDetailView,
    AdminSubscriptionListView,
    TemplateCreateView,
    TemplateUpdateDeleteView,
    AdminMediaListView,
)


urlpatterns = [
    #users
    path('users/', AdminUserListView.as_view(), name ='admin-users'),
    path('user/<int:id>/', AdminUserDetailView.as_view(), name = 'admin-user-detail'),
    path('user/<int:id>/status/', AdminUserDetailView.as_view(), name='admin-user-status-update'),

    #subscriptions
    path('subscription/', AdminSubscriptionListView.as_view(), name = 'admin-subscriptions'),

    #Banner Templates
    path('template/', TemplateCreateView.as_view(), name= 'admin-template-create'),
    path('template/<int:pk>/', TemplateUpdateDeleteView.as_view(), name='admin-template-update-delete'),

    #media
    path('media/', AdminMediaListView.as_view(), name= 'admin-medial-list'),

    
]