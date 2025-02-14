from django.shortcuts import render

import random
import datetime

prices = {"regular": 12, "new_york": 10, "deep_dish": 14}
specials = ["Chicken", "Sausage", "Pepperoni"]

# Create your views here.

def main(request):
    '''Show the main page using main.html'''

    template_name = "restaurant/main.html"
    
    context = {
      "image": "image.jpg",
    }

    return render(request, template_name, context)

def order(request):
    '''Show the menu to allow orders using order.html'''

    context = {
      "special": random.choice(specials),
    }

    template_name = "restaurant/order.html"
    return render(request, template_name, context)

from pprint import pprint

def format(pies):
  for i in range(len(pies)):
    if pies[i] == 'regular':
      pies[i] = "Regular Pie"
    elif pies[i] == 'new_york':
      pies[i] = "New York Style Pie"
    elif pies[i] == 'deep_dish':
      pies[i] = "Deep Dish Pie"
  return pies

def confirmation(request):
    '''Process the form submission, and return the price and wait time using confirmation.html'''

    template_name = "restaurant/confirmation.html"

    # read the form data into python variables:
    if request.POST:
        pprint(dict(request.POST))
        pies = request.POST.getlist('pie')
        topping = request.POST.getlist('topping')
        description = request.POST['description']
        name = request.POST['name']
        phone = request.POST['phone']
        email = request.POST['email']

        cost = 0
        for p in pies:
          cost += prices[p]
        print(format(pies))

        rand = random.randint(30, 60)  # Random minutes
        rtime = datetime.datetime.now() + datetime.timedelta(minutes=rand)
        rtime = rtime.strftime("%a %b %d %H:%M:%S %Y")

        context = {
          "cost": cost,
          "pies": format(pies),
          "topping": topping,
          "description": description,
          "name": name,
          "phone": phone,
          "email": email,
          "ready_time": rtime,
        }

    return render(request, template_name, context)