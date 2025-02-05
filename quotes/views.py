from django.shortcuts import render
from django.http import HttpRequest, HttpResponse

import random

quotes = [
  "“Appear weak when you are strong, and strong when you are weak.”", 
  "“The supreme art of war is to subdue the enemy without fighting.”", 
  "“Let your plans be dark and impenetrable as night, and when you move, fall like a thunderbolt.”",
]

images = ["suntzu1.jpg", "suntzu2.jpg", "suntzu3.jpg"]

def home_page(request):
    # A view to display the homepage using the 'quote.html' template
    
    template = 'quotes/quote.html'

    context = {
      "quote": random.choice(quotes),
      "image": random.choice(images),
    }

    return render(request, template, context)

def quote(request):
    # A view to display a quote using the 'quote.html' template
    
    template = 'quotes/quote.html'

    context = {
      "quote": random.choice(quotes),
      "image": random.choice(images),
    }

    return render(request, template, context)

def show_all(request):
    # A view to display all quotes using the 'show_all.html' template
    
    template = 'quotes/show_all.html'
        
    paired_data = zip(quotes, images)

    context = {
      "paired_data": paired_data
    }

    return render(request, template, context)

def about (request):
    # A view to display an about page using the 'about.html' template
    
    template = 'quotes/about.html'

    context = {
      "image": random.choice(images),
    }

    return render(request, template, context)