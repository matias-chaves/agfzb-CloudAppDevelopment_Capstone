from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
# from .models import related models
from .models import CarModel, DealerReview
# from .restapis import related methods
from .restapis import get_dealers_from_cf
from .restapis import get_dealer_reviews_from_cf
from .restapis import post_request
from .restapis import analyze_review_sentiments
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.


# Create an `about` view to render a static about page
def about(request):
    context = {}
    if request.method =='GET':
        return render(request,'djangoapp/about.html',context)



# Create a `contact` view to return a static contact page
def contact(request):
    context = {}
    if request.method =='GET':
        return render(request,'djangoapp/contact.html', context)

# Create a `login_request` view to handle sign in request
def login_request(request):
    context={}
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return render(request, 'djangoapp/index.html', context)
        else:
            return render(request, 'djangoapp/index.html', context)
    else:
        return render(request, 'djangoapp/index.html', context)

# Create a `logout_request` view to handle sign out request
def logout_request(request):
    context = {}
    logout(request)
    return render(request, 'djangoapp/index.html', context)


# Create a `registration_request` view to handle sign up request
def registration_request(request):
    context = {}

    if request.method == 'GET':
        return render(request, 'djangoapp/registration.html', context)
    elif request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        first_name = request.POST.get('firstname')
        last_name = request.POST.get('lastname')
        user_exist = False
        try:
            User.objects.get(username=username)
            user_exist = True
        except:
            pass
        if not user_exist:
            user = User.objects.create_user(
                username=username,
                first_name=first_name,
                last_name=last_name,
                password=password)
            login(request, user)
            return render(request, 'djangoapp/index.html', context)
        else:
            return render(request, 'djangoapp/index.html', context)

# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    context = {}
    if request.method == "GET":
        url = "https://us-south.functions.appdomain.cloud/api/v1/web/c18347d0-d16e-4bb2-83cf-d559d6b28653/dealership-package/get-dealership"
        dealerships = get_dealers_from_cf(url)
        context["dealership_list"] = dealerships
        return render(request, 'djangoapp/index.html', context)


# Create a `get_dealer_details` view to render the reviews of a dealer
# def get_dealer_details(request, dealer_id):
# ...

def get_dealer_details(request, dealerId, dealerFullName):
    context = {}
    if request.method == 'GET':
        url = "https://us-south.functions.appdomain.cloud/api/v1/web/c18347d0-d16e-4bb2-83cf-d559d6b28653/dealership-package/get-review"
        reviews = get_dealer_reviews_from_cf(url, dealerId)
        context['reviews'] = reviews
        context['dealerId'] = dealerId
        context['dealerFullName'] = dealerFullName
        return render(request, 'djangoapp/dealer_details.html', context)

# Create a `add_review` view to submit a review
# def add_review(request, dealer_id):
# ...
def add_review(request, dealerId):
    context = {
        "dealerId": dealerId
    }
    get_url = url = "https://us-south.functions.appdomain.cloud/api/v1/web/c18347d0-d16e-4bb2-83cf-d559d6b28653/dealership-package/get-dealership"
    car_dealer = get_dealers_from_cf(get_url, dealerId=dealerId)
    if request.method == 'POST':
        post_url = "https://us-south.functions.appdomain.cloud/api/v1/web/c18347d0-d16e-4bb2-83cf-d559d6b28653/dealership-package/post-review"
        form_data = request.POST
        car = CarModel.objects.get(id=form_data.get('car'))
        payload = {
            "review": {
            'id': 2022,
            'review': form_data.get('review_text'),
            'car_make': car.car_make.name,
            'car_year': int(car.year.strftime("%Y")),
            'car_model': car.name,
            'purchase': True if form_data.get('purchase') == 'on' else False,
            'name': form_data.get('name'),
            'dealership': dealerId,
            'sentiment': analyze_review_sentiments("natural" if form_data.get('review_text')==""else "positive" if form_data.get('purchase')=='on' else 'negative'),

            }
        }
        response = post_request(post_url, payload)
        print("Whith url {}, \nresponse => {}".format(post_url,response))
        return redirect('djangoapp:dealer_details', dealerId=dealerId, dealerFullName=car_dealer[0].full_name)
    elif request.method =='GET':
        context['cars'] = CarModel.objects.all()
        context['dealerships'] = car_dealer[0]
        return render(request, 'djangoapp/add_review.html', context)

