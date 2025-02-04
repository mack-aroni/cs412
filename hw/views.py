from django.shortcuts import render
from django.http import HttpRequest, HttpResponse

import time, random

def home_page(request):
    '''Define a view to show the 'home.html' template.'''
    
    # the template to which we will delegate the work
    template = 'hw/home.html'

    # a dict of key/value pairs, to be available for use in template
    context = {
        'current_time': time.ctime(),
        'letter1' : chr(random.randint(65,90)),
        'letter2' : chr(random.randint(65,90)),
        'number' : random.randint(1,10),
    }

    return render(request, template, context)

def about(request):
    '''Define a view to show the 'about.html' template.'''

    # the template to which we will delegate the work
    template = 'hw/about.html'

    # a dict of key/value pairs, to be available for use in template
    context = {
        'current_time': time.ctime(),
    }

    return render(request, template, context)