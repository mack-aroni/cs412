from django.shortcuts import render

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

    template_name = "restaurant/order.html"
    return render(request, template_name)

# def confirmation(request):
#     '''Process the form submission, and return the price and wait time using confirmation.html'''

#     template_name = "formdata/confirmation.html"

#     # read the form data into python variables:
#     if request.POST:

#         name = request.POST['name']
#         favorite_color = request.POST['favorite_color']

#         context = {
#             'name': name,
#             'favorite_color':  favorite_color,
            
#         }

#     return render(request, template_name, context=context)