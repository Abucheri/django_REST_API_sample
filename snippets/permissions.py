# implemeting object level permoissions
from rest_framework import permissions

"""

Object level permissions

Really we'd like all code snippets to be visible to anyone, but also make sure that only the user that created a code 
snippet is able to update or delete it. 

To do that we're going to need to create a custom permission.

In the snippets app, create a new file, permissions.py

"""


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the snippet.
        return obj.owner == request.user


"""

Now we can add that custom permission to our snippet instance endpoint, by editing the permission_classes property on 
the SnippetDetail view class:

    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                      IsOwnerOrReadOnly]
                      
Make sure to also import the IsOwnerOrReadOnly class.

    from snippets.permissions import IsOwnerOrReadOnly

Now, if you open a browser again, you find that the 'DELETE' and 'PUT' actions only appear on a snippet instance 
endpoint if you're logged in as the same user that created the code snippet. 

"""

"""

Authenticating with the API

Because we now have a set of permissions on the API, we need to authenticate our requests to it if we want to edit 
any snippets. We haven't set up any authentication classes, so the defaults are currently applied, which are 
SessionAuthentication and BasicAuthentication. 

When we interact with the API through the web browser, we can login, and the browser session will then provide the 
required authentication for the requests. 

If we're interacting with the API programmatically we need to explicitly provide the authentication credentials on 
each request. 

If we try to create a snippet without authenticating, we'll get an error:

    http POST http://127.0.0.1:8000/snippets/ code="print(123)"
    
    {
        "detail": "Authentication credentials were not provided."
    }

We can make a successful request by including the username and password of one of the users we created earlier.

    http -a admin:password123 POST http://127.0.0.1:8000/snippets/ code="print(789)"
    
    {
        "id": 1,
        "owner": "admin",
        "title": "foo",
        "code": "print(789)",
        "linenos": false,
        "language": "python",
        "style": "friendly"
    }

Summary

We've now got a fairly fine-grained set of permissions on our Web API, and end points for users of the system and for 
the code snippets that they have created. 

"""
