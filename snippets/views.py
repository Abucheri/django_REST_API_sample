from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from .models import Snippet
from .serializers import SnippetSerializer
# working with requests and responses
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
# enabling class-based views
from django.http import Http404
from rest_framework.views import APIView
# implementing mixins for our class-based views to handle CRUD instead of using individual functions
from rest_framework import mixins, generics

"""
Writing regular Django views using our Serializer

Let's see how we can write some API views using our new Serializer class. For the moment we won't use any of REST 
framework's other features, we'll just write the views as regular Django views. 

Edit the snippets/views.py
"""

# The root of our API is going to be a view that supports listing all the existing snippets, or creating a new snippet.

# Create your views here.
# @csrf_exempt
# def snippet_list(request):
#     """
#     List all code snippets, or create a new snippet.
#     """
#     if request.method == 'GET':
#         snippets = Snippet.objects.all()
#         serializer = SnippetSerializer(snippets, many=True)
#         return JsonResponse(serializer.data, safe=False)
#
#     elif request.method == 'POST':
#         data = JSONParser().parse(request)
#         serializer = SnippetSerializer(data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return JsonResponse(serializer.data, status=201)
#         return JsonResponse(serializer.errors, status=400)


"""
Note that because we want to be able to POST to this view from clients that won't have a CSRF token we need to 
mark the view as csrf_exempt. This isn't something that you'd normally want to do, and REST framework views actually 
use more sensible behavior than this, but it'll do for our purposes right now. 

We'll also need a view which corresponds to an individual snippet, and can be used to retrieve, update or delete the 
snippet.
"""

# @csrf_exempt
# def snippet_detail(request, pk):
#     """
#     Retrieve, update or delete a code snippet.
#     """
#     try:
#         snippet = Snippet.objects.get(pk=pk)
#     except Snippet.DoesNotExist:
#         return HttpResponse(status=404)
#
#     if request.method == 'GET':
#         serializer = SnippetSerializer(snippet)
#         return JsonResponse(serializer.data)
#
#     elif request.method == 'PUT':
#         data = JSONParser().parse(request)
#         serializer = SnippetSerializer(snippet, data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return JsonResponse(serializer.data)
#         return JsonResponse(serializer.errors, status=400)
#
#     elif request.method == 'DELETE':
#         snippet.delete()
#         return HttpResponse(status=204)


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

"""

Requests and Responses

From this point we're going to really start covering the core of REST framework. Let's introduce a couple of 
essential building blocks. Request objects 

REST framework introduces a Request object that extends the regular HttpRequest, and provides more flexible request 
parsing. The core functionality of the Request object is the request.data attribute, which is similar to 
request.POST, but more useful for working with Web APIs. 

    request.POST  # Only handles form data.  Only works for 'POST' method.
    request.data  # Handles arbitrary data.  Works for 'POST', 'PUT' and 'PATCH' methods.

Response objects

REST framework also introduces a Response object, which is a type of TemplateResponse that takes unrendered content 
and uses content negotiation to determine the correct content type to return to the client. 

    return Response(data)  # Renders to content type as requested by the client.

Status codes

Using numeric HTTP status codes in your views doesn't always make for obvious reading, and it's easy to not notice if 
you get an error code wrong. REST framework provides more explicit identifiers for each status code, 
such as HTTP_400_BAD_REQUEST in the status module. It's a good idea to use these throughout rather than using numeric 
identifiers. Wrapping API views 

REST framework provides two wrappers you can use to write API views.

    1. The @api_view decorator for working with function based views.
    2. The APIView class for working with class-based views.

These wrappers provide a few bits of functionality such as making sure you receive Request instances in your view, 
and adding context to Response objects so that content negotiation can be performed. 

The wrappers also provide behaviour such as returning 405 Method Not Allowed responses when appropriate, and handling 
any ParseError exceptions that occur when accessing request.data with malformed input. Pulling it all together 

Okay, let's go ahead and start using these new components to refactor our views slightly

"""

# @api_view(['GET', 'POST'])
# def snippet_list(request, format=None):
#     """
#     List all code snippets, or create a new snippet.
#     """
#     if request.method == 'GET':
#         snippets = Snippet.objects.all()
#         serializer = SnippetSerializer(snippets, many=True)
#         return Response(serializer.data)
#
#     elif request.method == 'POST':
#         serializer = SnippetSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Our instance view is an improvement over the previous example. It's a little more concise, and the code now feels
# very similar to if we were working with the Forms API. We're also using named status codes, which makes the
# response meanings more obvious.
#
# Here is the view for an individual snippet (snippet details), in the views.py module.
# @api_view(['GET', 'PUT', 'DELETE'])
# def snippet_detail(request, pk, format=None):
#     """
#     Retrieve, update or delete a code snippet.
#     """
#     try:
#         snippet = Snippet.objects.get(pk=pk)
#     except Snippet.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)
#
#     if request.method == 'GET':
#         serializer = SnippetSerializer(snippet)
#         return Response(serializer.data)
#
#     elif request.method == 'PUT':
#         serializer = SnippetSerializer(snippet, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     elif request.method == 'DELETE':
#         snippet.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


"""

This should all feel very familiar - it is not a lot different from working with regular Django views.

Notice that we're no longer explicitly tying our requests or responses to a given content type. request.data can 
handle incoming json requests, but it can also handle other formats. Similarly we're returning response objects with 
data, but allowing REST framework to render the response into the correct content type for us. 

"""

"""

Adding optional format suffixes to our URLs

To take advantage of the fact that our responses are no longer hardwired to a single content type let's add support 
for format suffixes to our API endpoints. Using format suffixes gives us URLs that explicitly refer to a given 
format, and means our API will be able to handle URLs such as http://example.com/api/items/4.json. 

Start by adding a format keyword argument to both of the views, like so.

    def snippet_list(request, format=None):

and

    def snippet_detail(request, pk, format=None):

"""
# now lets move to our urls file to add suffix patterns

"""

Class-based Views

We can also write our API views using class-based views, rather than function based views. As we'll see this is a 
powerful pattern that allows us to reuse common functionality, and helps us keep our code DRY (Don't Repeat Yourself). 

Rewriting our API using class-based views 

We'll start by rewriting the root view as a class-based view. All this involves is a little bit of refactoring of 
views.py. 

"""

# class SnippetList(APIView):
#     """
#     List all snippets, or create a new snippet.
#     """
#
#     def get(self, request, format=None):
#         snippets = Snippet.objects.all()
#         serializer = SnippetSerializer(snippets, many=True)
#         return Response(serializer.data)
#
#     def post(self, request, format=None):
#         serializer = SnippetSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


"""

So far, so good. It looks pretty similar to the previous case, but we've got better separation between the different 
HTTP methods. We'll also need to update the instance view in views.py. 

"""

# class SnippetDetail(APIView):
#     """
#     Retrieve, update or delete a snippet instance.
#     """
#     def get_object(self, pk):
#         try:
#             return Snippet.objects.get(pk=pk)
#         except Snippet.DoesNotExist:
#             raise Http404
#
#     def get(self, request, pk, format=None):
#         snippet = self.get_object(pk)
#         serializer = SnippetSerializer(snippet)
#         return Response(serializer.data)
#
#     def put(self, request, pk, format=None):
#         snippet = self.get_object(pk)
#         serializer = SnippetSerializer(snippet, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     def delete(self, request, pk, format=None):
#         snippet = self.get_object(pk)
#         snippet.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

# That's looking good. Again, it's still pretty similar to the function based view right now.
#
# We'll also need to refactor our snippets/urls.py slightly now that we're using class-based views.

"""

Using mixins

One of the big wins of using class-based views is that it allows us to easily compose reusable bits of behaviour.

The create/retrieve/update/delete operations that we've been using so far are going to be pretty similar for any 
model-backed API views we create. Those bits of common behaviour are implemented in REST framework's mixin classes. 

Let's take a look at how we can compose the views by using the mixin classes. Here's our views.py module again.

"""

# class SnippetList(mixins.ListModelMixin,
#                   mixins.CreateModelMixin,
#                   generics.GenericAPIView):
#     queryset = Snippet.objects.all()
#     serializer_class = SnippetSerializer
#
#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)
#
#     def post(self, requset, *args, **kwargs):
#         return self.create(requset, *args, **kwargs)


"""

We'll take a moment to examine exactly what's happening here. We're building our view using GenericAPIView, 
and adding in ListModelMixin and CreateModelMixin. 

The base class provides the core functionality, and the mixin classes provide the .list() and .create() actions. 
We're then explicitly binding the get and post methods to the appropriate actions. Simple enough stuff so far. 

"""

# class SnippetDetail(mixins.RetrieveModelMixin,
#                     mixins.UpdateModelMixin,
#                     mixins.DestroyModelMixin,
#                     generics.GenericAPIView):
#     queryset = Snippet.objects.all()
#     serializer_class = SnippetSerializer
#
#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)
#
#     def put(self, request, *args, **kwargs):
#         return self.update(request, *args, **kwargs)
#
#     def delete(self, request, *args, **kwargs):
#         return self.destroy(request, *args, **kwargs)

# Pretty similar. Again we're using the GenericAPIView class to provide the core functionality
# and adding in mixins to provide the .retrieve(), .update() and .destroy() actions.

# still working wih views

"""

Using generic class-based views

Using the mixin classes we've rewritten the views to use slightly less code than before, but we can go one step 
further. REST framework provides a set of already mixed-in generic views that we can use to trim down our views.py 
module even more. 

"""


class SnippetList(generics.ListCreateAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer


class SnippetDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer

# Wow, that's pretty concise. We've gotten a huge amount for free, and our code looks like good, clean,
# idiomatic Django.
