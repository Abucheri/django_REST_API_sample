from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from .models import Snippet
from .serializers import SnippetSerializer

"""
Writing regular Django views using our Serializer

Let's see how we can write some API views using our new Serializer class. For the moment we won't use any of REST 
framework's other features, we'll just write the views as regular Django views. 

Edit the snippets/views.py
"""


# The root of our API is going to be a view that supports listing all the existing snippets, or creating a new snippet.

# Create your views here.
@csrf_exempt
def snippet_list(request):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        snippets = Snippet.objects.all()
        serializer = SnippetSerializer(snippets, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = SnippetSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


"""
Note that because we want to be able to POST to this view from clients that won't have a CSRF token we need to 
mark the view as csrf_exempt. This isn't something that you'd normally want to do, and REST framework views actually 
use more sensible behavior than this, but it'll do for our purposes right now. 

We'll also need a view which corresponds to an individual snippet, and can be used to retrieve, update or delete the 
snippet.
"""


@csrf_exempt
def snippet_detail(request, pk):
    """
    Retrieve, update or delete a code snippet.
    """
    try:
        snippet = Snippet.objects.get(pk=pk)
    except Snippet.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = SnippetSerializer(snippet)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = SnippetSerializer(snippet, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        snippet.delete()
        return HttpResponse(status=204)


"""
Finally we need to wire these views up. Create the snippets/urls.py file:
"""

"""
It's worth noting that there are a couple of edge cases we're not dealing with properly at the moment. If we send 
malformed json, or if a request is made with a method that the view doesn't handle, then we'll end up with a 500 
"server error" response. Still, this'll do for now.
"""

"""
Testing our first attempt at a Web API

Now we can start up a sample server that serves our snippets.

Quit out of the shell...

quit()

...and start up Django's development server.

In another terminal window, we can test the server.

We can test our API using curl or httpie. Httpie is a user friendly http client that's written in Python. Let's 
install that. 

You can install httpie using pip:
"""


"""
Finally, we can get a list of all of the snippets:

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

Or we can get a particular snippet by referencing its id:

http http://127.0.0.1:8000/snippets/2/

HTTP/1.1 200 OK
...
{
  "id": 2,
  "title": "",
  "code": "print(\"hello, world\")\n",
  "linenos": false,
  "language": "python",
  "style": "friendly"
}

Similarly, you can have the same json displayed by visiting these URLs in a web browser.
"""

"""
Where are we now

We're doing okay so far, we've got a serialization API that feels pretty similar to Django's Forms API, 
and some regular Django views. 

Our API views don't do anything particularly special at the moment, beyond serving json responses, and there are some 
error handling edge cases we'd still like to clean up, but it's a functioning Web API.
"""