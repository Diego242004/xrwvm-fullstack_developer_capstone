# Uncomment the required imports before adding the code

from urllib.parse import quote
from .restapis import get_request, analyze_review_sentiments, post_review
from django.contrib.auth.models import User
from django.contrib.auth import logout
from .models import CarModel


from django.http import JsonResponse
from django.contrib.auth import login, authenticate
import logging
import json
from django.views.decorators.csrf import csrf_exempt
from .populate import initiate


# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.

# Create a `login_request` view to handle sign in request
@csrf_exempt
def login_user(request):
    # Get username and password from request.POST dictionary
    data = json.loads(request.body)
    username = data['userName']
    password = data['password']
    # Try to check if provide credential can be authenticated
    user = authenticate(username=username, password=password)
    data = {"userName": username}
    if user is not None:
        # If user is valid, call login method to login current user
        login(request, user)
        data = {"userName": username, "status": "Authenticated"}
    return JsonResponse(data)

# Create a `logout_request` view to handle sign out request


def logout_request(request):
    logout(request)
    return JsonResponse({"userName": ""})


def get_cars(request):
    if not CarModel.objects.exists():
        initiate()

    car_models = CarModel.objects.select_related('car_make')
    cars = [
        {
            "CarModel": car_model.name,
            "CarMake": car_model.car_make.name,
        }
        for car_model in car_models
    ]
    return JsonResponse({"CarModels": cars})

# # Update the `get_dealerships` view to render the index page with
# a list of dealerships
# def get_dealerships(request):
# ...

# Create a `get_dealer_reviews` view to render the reviews of a dealer
# def get_dealer_reviews(request,dealer_id):
# ...

# Create a `get_dealer_details` view to render the dealer details
# def get_dealer_details(request, dealer_id):
# ...

# Create a `add_review` view to submit a review
# def add_review(request):
# ...


@csrf_exempt
def registration(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST required"}, status=405)
    try:
        data = json.loads(request.body)
        username = data['userName']
        password = data['password']
        first_name = data['firstName']
        last_name = data['lastName']
        email = data['email']
    except (ValueError, KeyError, TypeError):
        return JsonResponse({"error": "Invalid registration data"}, status=400)
    if not isinstance(
            username,
            str) or not username.strip() or not isinstance(
            password,
            str) or not password:
        return JsonResponse(
            {"error": "Username and password are required"}, status=400)
    if User.objects.filter(username=username).exists():
        return JsonResponse(
            {"userName": username, "error": "Already Registered"})
    user = User.objects.create_user(
        username=username, password=password, first_name=first_name,
        last_name=last_name, email=email,
    )
    login(request, user)
    return JsonResponse({"userName": username, "status": "Authenticated"})


def get_dealerships(request, state='All'):
    endpoint = '/fetchDealers' if state == 'All' else '/fetchDealers/' + \
        quote(state, safe='')
    dealerships = get_request(endpoint)
    if dealerships is None:
        return JsonResponse(
            {'status': 502, 'message': 'Backend unavailable'}, status=502)
    return JsonResponse({'status': 200, 'dealers': dealerships})


def get_dealer_details(request, dealer_id):
    if dealer_id <= 0:
        return JsonResponse(
            {'status': 400, 'message': 'Bad Request'}, status=400)
    dealership = get_request('/fetchDealer/' + str(dealer_id))
    if dealership is None:
        return JsonResponse(
            {'status': 502, 'message': 'Backend unavailable'}, status=502)
    return JsonResponse({'status': 200, 'dealer': dealership})


def get_dealer_reviews(request, dealer_id):
    if dealer_id <= 0:
        return JsonResponse(
            {'status': 400, 'message': 'Bad Request'}, status=400)
    reviews = get_request('/fetchReviews/dealer/' + str(dealer_id))
    if reviews is None:
        return JsonResponse(
            {'status': 502, 'message': 'Backend unavailable'}, status=502)
    for review_detail in reviews:
        response = analyze_review_sentiments(review_detail['review'])
        if not isinstance(
                response,
                dict) or response.get('sentiment') not in (
                'positive',
                'neutral',
                'negative'):
            return JsonResponse(
                {'status': 502, 'message': 'Sentiment service unavailable'},
                status=502)
        review_detail['sentiment'] = response['sentiment']
    return JsonResponse({'status': 200, 'reviews': reviews})


def add_review(request):
    if not request.user.is_authenticated:
        return JsonResponse(
            {'status': 403, 'message': 'Unauthorized'}, status=403)
    if request.method != 'POST':
        return JsonResponse(
            {'status': 405, 'message': 'POST required'}, status=405)
    try:
        data = json.loads(request.body)
    except (ValueError, TypeError):
        return JsonResponse(
            {'status': 400, 'message': 'Invalid review data'}, status=400)
    required = (
        'name',
        'dealership',
        'review',
        'purchase',
        'purchase_date',
        'car_make',
        'car_model',
        'car_year')
    if not isinstance(
            data, dict) or any(
            field not in data for field in required):
        return JsonResponse(
            {'status': 400, 'message': 'Missing review fields'}, status=400)
    response = post_review(data)
    if response is None:
        return JsonResponse(
            {'status': 502, 'message': 'Error in posting review'}, status=502)
    return JsonResponse(
        {'status': 200, 'message': 'Review posted successfully'})
