from django.urls import path
from . import views

urlpatterns = [
    # Greeting Categories
    path("greeting-categories/", views.GreetingCategoryListView.as_view(), name="greeting-categories"),

    # Greeting Templates
    path("greeting-templates/", views.GreetingTemplateListView.as_view(), name="greeting-templates"),
    path("greeting-templates/search/", views.GreetingTemplateSearchView.as_view(), name="greeting-templates-search"),
    path("greeting-templates/<int:pk>/like/", views.GreetingTemplateLikeView.as_view(), name="greeting-template-like"),
    path("greeting-templates/<int:pk>/download/", views.GreetingTemplateDownloadView.as_view(), name="greeting-template-download"),

    # Greetings
    path("greetings/", views.GreetingCreateView.as_view(), name="create-greeting"),
]
