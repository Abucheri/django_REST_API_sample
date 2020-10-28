from django.db import models
# We'll be using this (pygments) for the code highlighting
from pygments.lexers import get_all_lexers
from pygments.styles import get_all_styles
# pygments for highlighting code after implementing authentication
from pygments.lexers import get_lexer_by_name
from pygments.formatters.html import HtmlFormatter
from pygments import highlight

LEXERS = [item for item in get_all_lexers() if item[1]]
LANGUAGE_CHOICES = sorted([(item[1][0], item[0]) for item in LEXERS])
STYLE_CHOICES = sorted([(item, item) for item in get_all_styles()])

# Create your models here.

"""
For the purposes of this tutorial we're going to start by creating a simple Snippet model that is used to store 
code snippets. Go ahead and edit the snippets/models.py file. Note: Good programming practices include comments. 
Although you will find them in our repository version of this tutorial code, we have omitted them here to focus on 
the code itself.
"""

# after creating generic-based views we are now dealing with authentication
"""

Authentication & Permissions

Currently our API doesn't have any restrictions on who can edit or delete code snippets. We'd like to have some more 
advanced behavior in order to make sure that: 

    Code snippets are always associated with a creator.
    Only authenticated users may create snippets.
    Only the creator of a snippet may update or delete it.
    Unauthenticated requests should have full read-only access.

Adding information to our model

We're going to make a couple of changes to our Snippet model class. First, let's add a couple of fields. One of those 
fields will be used to represent the user who created the code snippet. The other field will be used to store the 
highlighted HTML representation of the code. 

Add the following two fields to the Snippet model in models.py.

    owner = models.ForeignKey('auth.User', related_name='snippets', on_delete=models.CASCADE)
    highlighted = models.TextField()

We'd also need to make sure that when the model is saved, that we populate the highlighted field, using the pygments 
code highlighting library. 

We'll need some extra imports also for pygments to highlight our code snippets

"""


# simple Snippet model that is used to store code snippets
class Snippet(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey('auth.user', related_name='snippets', on_delete=models.CASCADE)
    title = models.CharField(max_length=100, blank=True, default='')
    code = models.TextField()
    linenos = models.BooleanField(default=False)
    language = models.CharField(choices=LANGUAGE_CHOICES, default='python', max_length=100)
    style = models.CharField(choices=STYLE_CHOICES, default='friendly', max_length=100)
    highlighted = models.TextField()

    class Meta:
        ordering = ['created']

    # And now we can add a .save() method to our model class after adding owner and highlighted fields to our model
    def save(self, *args, **kwargs):
        """
        Use the `pygments` library to create a highlighted HTML
        representation of the code snippet.
        """
        lexer = get_lexer_by_name(self.language)
        linenos = 'table' if self.linenos else False
        options = {'title': self.title} if self.title else {}
        formatter = HtmlFormatter(style=self.style, linenos=linenos,
                                  full=True, **options)
        self.highlighted = highlight(self.code, lexer, formatter)
        super(Snippet, self).save(*args, **kwargs)


"""

When that's all done we'll need to update our database tables. Normally we'd create a database migration in order to 
do that, but for the purposes of this tutorial, let's just delete the database and start again.

    rm -f db.sqlite3
    rm -r snippets/migrations
    python manage.py makemigrations snippets
    python manage.py migrate

You might also want to create a few different users, to use for testing the API. The quickest way to do this will be 
with the createsuperuser command. 

    python manage.py createsuperuser

"""

# now we will go and add our user endpoints in serializers.py
