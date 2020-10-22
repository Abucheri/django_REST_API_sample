from django.db import models
# We'll be using this (pygments) for the code highlighting
from pygments.lexers import get_all_lexers
from pygments.styles import get_all_styles

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


# simple Snippet model that is used to store code snippets
class Snippet(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100, blank=True, default='')
    code = models.TextField()
    linenos = models.BooleanField(default=False)
    language = models.CharField(choices=LANGUAGE_CHOICES, default='python', max_length=100)
    style = models.CharField(choices=STYLE_CHOICES, default='friendly', max_length=100)

    class Meta:
        ordering = ['created']
