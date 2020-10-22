from django.urls import path
from . import views

urlpatterns = [
    path('snippets/', views.snippet_list),
    path('snippets/<int:pk>/', views.snippet_detail),
]


"""
We also need to wire up the root urlconf, in the tutorial/urls.py file, to include our snippet app's URLs.
"""