from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from datetime import date
from .models import Employee
from django.apps import apps


@login_required
def index(request):
    # The following line will get the logged-in user (if there is one) within any view function
    logged_in_user = request.user
    try:
        # This line will return the employee record of the logged-in user if one exists
        logged_in_employee = Employee.objects.get(user=logged_in_user)
        Customer = apps.get_model('customers.Customer')
        customers_in_zip = Customer.objects.filter(
            zip_code=logged_in_employee.zip_code)
        # find customers with weekly pickup day of today or onetime pickup of today's date
        today = date.today()
        weekday_number = today.weekday()
        names_of_days = ['Monday', 'Tuesday', 'Wednesday',
                         'Thursday', 'Friday', 'Saturday', 'Sunday']
        day_name = (weekday_number, names_of_days)
        todays_customer = customers_in_zip.filter(
            one_time_pickup=today) | customers_in_zip.filter(weekly_pickup=day_name)

        context = {
            'logged_in_employee': logged_in_employee,
            'today': today,
            'todays_customer': todays_customer

        }
        return render(request, 'employees/index.html', context)
    except ObjectDoesNotExist:
        return HttpResponseRedirect(reverse('employees:create'))


@login_required
def create(request):
    logged_in_user = request.user
    if request.method == "POST":
        name_from_form = request.POST.get('name')
        address_from_form = request.POST.get('address')
        zip_from_form = request.POST.get('zip_code')
        new_employee = Employee(name=name_from_form, user=logged_in_user,
                                address=address_from_form, zip_code=zip_from_form)
        new_employee.save()
        return HttpResponseRedirect(reverse('employees:index'))
    else:

        return render(request, 'employees/create.html')


@login_required
def edit_profile(request):
    logged_in_user = request.user
    logged_in_employee = Employee.objects.get(user=logged_in_user)
    if request.method == "POST":
        name_from_form = request.POST.get('name')
        address_from_form = request.POST.get('address')
        zip_from_form = request.POST.get('zip_code')
        logged_in_employee.name = name_from_form
        logged_in_employee.address = address_from_form
        logged_in_employee.zip_code = zip_from_form
        logged_in_employee.save()
        return HttpResponseRedirect(reverse('employees:index'))
    else:
        context = {
            'logged_in_employee': logged_in_employee
        }
        return render(request, 'employees/edit_profile.html', context)

# @login_required
# def customers_in_zip(request):
#     logged_in_user = request.user
#     logged_in_employee = Employee.objects.get(user=logged_in_user)
#     Customer = apps.get_model('customers.Customer')
#     my_customers = Customer.objects.filter(zip_code=logged_in_employee.zip_code)
#     context = {
#             'logged_in_employee': logged_in_employee
#          }
#     return render(request, 'employees/index.html', context)
