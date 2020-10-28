"""
The first thing we need to get started on our Web API is to provide a way of serializing and deserializing the
snippet instances into representations such as 'json'. We can do this by declaring serializers that work very similar
to Django's forms. Create a file in the snippets directory named serializers.py
"""
from rest_framework import serializers
from .models import Snippet, LANGUAGE_CHOICES, STYLE_CHOICES
# importing auth model for user serializer
from django.contrib.auth.models import User


# class SnippetSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)
#     title = serializers.CharField(required=False, allow_blank=True, max_length=100)
#     code = serializers.CharField(style={'base_template': 'textarea.html'})
#     linenos = serializers.BooleanField(required=False)
#     language = serializers.ChoiceField(choices=LANGUAGE_CHOICES, default='python')
#     style = serializers.ChoiceField(choices=STYLE_CHOICES, default='friendly')
#
#     def create(self, validated_data):
#         """
#         Create and return a new `Snippet` instance, given the validated data.
#         """
#
#         return Snippet.objects.create(**validated_data)
#
#     def update(self, instance, validated_data):
#         """
#         Update and return an existing `Snippet` instance, given the validated data.
#         """
#         instance.title = validated_data.get('title', instance.title)
#         instance.code = validated_data.get('code', instance.code)
#         instance.linenos = validated_data.get('linenos', instance.linenos)
#         instance.language = validated_data.get('language', instance.language)
#         instance.style = validated_data.get('style', instance.style)
#         instance.save()
#         return instance


# using a ModelSerializers
class SnippetSerializer(serializers.ModelSerializer):
    """

    Updating our serializer

    Now that snippets are associated with the user that created them, let's update our SnippetSerializer to reflect that.
    Add the following field to the serializer definition in serializers.py:
        owner = serializers.ReadOnlyField(source='owner.username')

    Note: Make sure you also add 'owner', to the list of fields in the inner Meta class.

    This field is doing something quite interesting. The source argument controls which attribute is used to populate
    a field, and can point at any attribute on the serialized instance. It can also take the dotted notation shown
    above, in which case it will traverse the given attributes, in a similar way as it is used with Django's template
    language.

    The field we've added is the untyped ReadOnlyField class, in contrast to the other typed fields,
    such as CharField, BooleanField etc... The untyped ReadOnlyField is always read-only, and will be used for
    serialized representations, but will not be used for updating model instances when they are deserialized. We
    could have also used 'CharField(read_only=True)' here.

    """
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Snippet
        # fields = ['url', 'id', 'title', 'code', 'linenos', 'language', 'language', 'style']
        fields = ['id', 'owner', 'title', 'code', 'linenos', 'language', 'language', 'style']

        # now we will go on to add required permissions to views after associating users


"""
The first part of the serializer class defines the fields that get serialized/deserialized. The create() and 
update() methods define how fully fledged instances are created or modified when calling serializer.save() A 
serializer class is very similar to a Django Form class, and includes similar validation flags on the various fields, 
such as required, max_length and default The field flags can also control how the serializer should be displayed in 
certain circumstances, such as when rendering to HTML. The {'base_template': 'textarea.html'} flag above is 
equivalent to using widget=widgets.Textarea on a Django Form class. This is particularly useful for controlling how 
the browsable API should be displayed, as we'll see later in the tutorial. We can actually also save ourselves some 
time by using the ModelSerializer class, as we'll see later, but for now we'll keep our serializer definition 
explicit.
"""

"""
Working with Serializers

Before we go any further we'll familiarize ourselves with using our new Serializer class. Let's drop into the Django 
shell. 

python manage.py shell

Okay, once we've got a few imports out of the way, let's create a couple of code snippets to work with.

from snippets.models import Snippet
from snippets.serializers import SnippetSerializer
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser

snippet = Snippet(code='foo = "bar"\n')
snippet.save()

snippet = Snippet(code='print("hello, world")\n')
snippet.save()

We've now got a few snippet instances to play with. Let's take a look at serializing one of those instances.

serializer = SnippetSerializer(snippet)
serializer.data
# {'id': 2, 'title': '', 'code': 'print("hello, world")\n', 'linenos': False, 'language': 'python', 'style': 'friendly'}

At this point we've translated the model instance into Python native datatypes. To finalize the serialization process 
we render the data into json. 

content = JSONRenderer().render(serializer.data) 
content 
# b'{"id": 2, "title": "", "code": "print(\\"hello, 
world\\")\\n", "linenos": false, "language": "python", "style": "friendly"}' 

Deserialization is similar. First we parse a stream into Python native datatypes...

import io

stream = io.BytesIO(content)
data = JSONParser().parse(stream)

...then we restore those native datatypes into a fully populated object instance.

serializer = SnippetSerializer(data=data)
serializer.is_valid() 
# True 
serializer.validated_data 
# OrderedDict([(
'title', ''), ('code', 'print("hello, world")\n'), ('linenos', False), ('language', 'python'), ('style', 
'friendly')]) 
serializer.save() 
# <Snippet: Snippet object> 

Notice how similar the API is to working with forms. The similarity should become even more apparent when we start 
writing views that use our serializer. 

We can also serialize querysets instead of model instances. To do so we simply add a many=True flag to the serializer 
arguments. 

serializer = SnippetSerializer(Snippet.objects.all(), many=True)
serializer.data 
# [OrderedDict([('id', 1), ('title', 
''), ('code', 'foo = "bar"\n'), ('linenos', False), ('language', 'python'), ('style', 'friendly')]), OrderedDict([(
'id', 2), ('title', ''), ('code', 'print("hello, world")\n'), ('linenos', False), ('language', 'python'), ('style', 
'friendly')]), OrderedDict([('id', 3), ('title', ''), ('code', 'print("hello, world")'), ('linenos', False), 
('language', 'python'), ('style', 'friendly')])]
"""

"""
Using ModelSerializers

Our SnippetSerializer class is replicating a lot of information that's also contained in the Snippet model. It would 
be nice if we could keep our code a bit more concise. 

In the same way that Django provides both Form classes and ModelForm classes, REST framework includes both Serializer 
classes, and ModelSerializer classes. 

Let's look at refactoring our serializer using the ModelSerializer class. Open the file snippets/serializers.py 
again, and replace the SnippetSerializer class with the following. (above ) 

class SnippetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Snippet
        fields = ['id', 'title', 'code', 'linenos', 'language', 'style']
"""

"""
One nice property that serializers have is that you can inspect all the fields in a serializer instance, 
by printing its representation. Open the Django shell with python manage.py shell, then try the following: 

from snippets.serializers import SnippetSerializer
serializer = SnippetSerializer()
print(repr(serializer))
# SnippetSerializer():
#    id = IntegerField(label='ID', read_only=True)
#    title = CharField(allow_blank=True, max_length=100, required=False)
#    code = CharField(style={'base_template': 'textarea.html'})
#    linenos = BooleanField(required=False)
#    language = ChoiceField(choices=[('Clipper', 'FoxPro'), ('Cucumber', 'Gherkin'), ('RobotFramework', 'RobotFramework'),
    ('abap', 'ABAP'), ('ada', 'Ada')...
#    style = ChoiceField(choices=[('autumn', 'autumn'), ('borland', 'borland'), ('bw', 'bw'), ('colorful', 'colorful')... 
"""

"""
It's important to remember that ModelSerializer classes don't do anything particularly magical, they are simply a 
shortcut for creating serializer classes: 

    An automatically determined set of fields.
    Simple default implementations for the create() and update() methods.

"""

"""

Adding endpoints for our User models

Now that we've got some users to work with, we'd better add representations of those users to our API. Creating a new 
serializer is easy. In serializers.py add: 

    from django.contrib.auth.models import User
    
    class UserSerializer(serializers.ModelSerializer):
        snippets = serializers.PrimaryKeyRelatedField(many=True, queryset=Snippet.objects.all())
    
        class Meta:
            model = User
            fields = ['id', 'username', 'snippets']

"""


class UserSerializer(serializers.ModelSerializer):
    snippets = serializers.PrimaryKeyRelatedField(many=True, queryset=Snippet.objects.all())

    class Meta:
        model = User
        fields = ['id', 'username', 'snippets']


"""

Because 'snippets' is a reverse relationship on the User model, it will not be included by default when using the 
ModelSerializer class, so we needed to add an explicit field for it. 

We'll also add a couple of views to views.py. We'd like to just use read-only views for the user representations, 
so we'll use the ListAPIView and RetrieveAPIView generic class-based views. 

"""

# off to views.py
