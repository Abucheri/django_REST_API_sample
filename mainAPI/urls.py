"""mainAPI URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('snippets.urls')),
]

# this is good so far since only authenticated users are able to edit snippets but we need to create permissions to
# make sure that only the user that created a particular snippet can edit it, not all authenticated users. we'll add
# a snippets/permissions.py to do this

# we now move to requests and responses
# we are going to edit the views of our REST API

# adding url patterns for the browsableAPI for user authentication
urlpatterns += [
    path('api-auth/', include('rest_framework.urls')),
]
