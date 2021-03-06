from django.urls import path
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

# urlpatterns = [
#     path('snippets/', views.snippet_list),
#     path('snippets/<int:pk>/', views.snippet_detail),
# ]

"""
We also need to wire up the root urlconf, in the mainApi/urls.py file, to include our snippet app's URLs.
"""

# Now update the snippets/urls.py file slightly, to append a set of format_suffix_patterns in addition to the
# existing URLs.

# urlpatterns = format_suffix_patterns(urlpatterns)

# We don't necessarily need to add these extra url patterns in, but it gives us a simple, clean way of referring to a
# specific format.

"""

How's it looking?

Go ahead and test the API from the command line, as we did in tutorial part 1. Everything is working pretty 
similarly, although we've got some nicer error handling if we send invalid requests. 

We can get a list of all of the snippets, as before.

http http://127.0.0.1:8000/snippets/

HTTP/1.1 200 OK
...
[
  {
    "id": 1,
    "title": "",
    "code": "foo = \"bar\"\n",
    "linenos": false,
    "language": "python",
    "style": "friendly"
  },
  {
    "id": 2,
    "title": "",
    "code": "print(\"hello, world\")\n",
    "linenos": false,
    "language": "python",
    "style": "friendly"
  }
]

We can control the format of the response that we get back, either by using the Accept header:

    http http://127.0.0.1:8000/snippets/ Accept:application/json  # Request JSON
    http http://127.0.0.1:8000/snippets/ Accept:text/html         # Request HTML

Or by appending a format suffix:

    http http://127.0.0.1:8000/snippets.json  # JSON suffix
    http http://127.0.0.1:8000/snippets.api   # Browsable API suffix

Similarly, we can control the format of the request that we send, using the Content-Type header.

# POST using form data
http --form POST http://127.0.0.1:8000/snippets/ code="print(123)"

{
  "id": 3,
  "title": "",
  "code": "print(123)",
  "linenos": false,
  "language": "python",
  "style": "friendly"
}

# POST using JSON
http --json POST http://127.0.0.1:8000/snippets/ code="print(456)"

{
    "id": 4,
    "title": "",
    "code": "print(456)",
    "linenos": false,
    "language": "python",
    "style": "friendly"
}

If you add a --debug switch to the http requests above, you will be able to see the request type in request headers.

Now go and open the API in a web browser, by visiting http://127.0.0.1:8000/snippets/.
Browsability

Because the API chooses the content type of the response based on the client request, it will, by default, 
return an HTML-formatted representation of the resource when that resource is requested by a web browser. This allows 
for the API to return a fully web-browsable HTML representation. 

Having a web-browsable API is a huge usability win, and makes developing and using your API much easier. It also 
dramatically lowers the barrier-to-entry for other developers wanting to inspect and work with your API. 

"""

# going to views to add class-based views to snippets/views.py

# Refactoring urls for class based views
# urlpatterns = [
#     path('snippets/', views.SnippetList.as_view()),
#     path('snippets/<int:pk>/', views.SnippetDetail.as_view()),
    # adding path for user API views
    # path('users/', views.UserList.as_view()),
    # path('users/<int:pk>/', views.UserDetail.as_view()),
    # now what is remaining is associating a snippet with the respective user, we will now edit the SnippetList class in
    # snippets/views.py to implement this
    # path('', views.api_root),
    # path('snippets/<int:pk>/highlight/', views.SnippetHighlight.as_view()),
    # we now go on to implement hyperlinks for our API at snippets/serializers.py
# ]

# urlpatterns = format_suffix_patterns(urlpatterns)

# Okay, we're done. If you run the development server everything should be working just as before.
# we are now going to create mixins for our views to implement CRUD without using functions

# let's add url patterns that have names for hyperlinking the APIs

# API endpoints
urlpatterns = format_suffix_patterns([
    path('', views.api_root),
    path('snippets/', views.SnippetList.as_view(), name='snippet-list'),
    path('snippets/<int:pk>/', views.SnippetDetail.as_view(), name='snippet-detail'),
    path('snippets/<int:pk>/highlight/', views.SnippetHighlight.as_view(), name='snippet-highlight'),
    path('users/', views.UserList.as_view(), name='user-list'),
    path('users/<int:pk>/', views.UserDetail.as_view(), name='user-detail'),
])

# we are all set, now we need to add some pagination because we are going to get alot of instances from our API
# we'll do this in the settings file
