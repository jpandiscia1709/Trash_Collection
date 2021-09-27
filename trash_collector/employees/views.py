from django.http import HttpResponse
from django.shortcuts import render
from django.apps import apps

# Create your views here.

# TODO: Create a function for each path created in employees/urls.py. Each will need a template as well.


def index(request):
    # This line will get the Customer model from the other app, it can now be used to query the db for Customers
    Customer = apps.get_model('customers.Customer')
    return render(request, 'employees/index.html')
# return a lsit of today's customers
# filter the list for costomers in my zip code
# filter list for scheduled pickup of today and one time pickup of today
# exclude suspended accounts
# exclude where trash has already been pick up  