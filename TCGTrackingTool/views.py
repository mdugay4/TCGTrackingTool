from urllib.parse import urlsplit
from django.core.serializers.json import DjangoJSONEncoder
from rest_framework.decorators import api_view
from rest_framework.response import Response
import re
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
import os
import requests
import json
import datetime
from django.conf import settings
from .models import Card, Inventory, CardPriceHistory, CardPriceNotification, CardPriceNotificationMessage
from config import public_key, private_key, recaptcha_site_key, recaptcha_secret_key
from .forms import CardForm, CreateUserForm
from .serializers import CardSerializer, CardPriceHistorySerializer, CardPriceNotificationSerializer, CardPriceNotificationMessageSerializer
import logging


def index(request):
    # show current logged in username
    context = {}
    context['username'] = request.user

    # get currently logged in user's message count
    if request.user.is_authenticated:
        cardPriceNotificationMessage_qs = CardPriceNotificationMessage.objects.filter(
            user=request.user)
        context['msg_count'] = cardPriceNotificationMessage_qs.count

    return render(request, "TCGTrackingTool/index.html", context=context)


def home(request):
    # show current logged in username
    context = {}
    context['username'] = request.user

    # get currently logged in user's message count
    if request.user.is_authenticated:
        cardPriceNotificationMessage_qs = CardPriceNotificationMessage.objects.filter(
            user=request.user)
        context['msg_count'] = cardPriceNotificationMessage_qs.count

    return render(request, "TCGTrackingTool/layout.html", context=context)


def notfounderror(request):
    # show current logged in username
    context = {}
    context['username'] = request.user

    if request.user.is_authenticated:
        cardPriceNotificationMessage_qs = CardPriceNotificationMessage.objects.filter(
            user=request.user)
        context['msg_count'] = cardPriceNotificationMessage_qs.count

    return render(request, "TCGTrackingTool/notFoundError.html", context=context)


def about(request):
    # show current logged in username
    context = {}
    context['username'] = request.user

    if request.user.is_authenticated:
        cardPriceNotificationMessage_qs = CardPriceNotificationMessage.objects.filter(
            user=request.user)
        context['msg_count'] = cardPriceNotificationMessage_qs.count

    return render(request, "TCGTrackingTool/about.html", context=context)


def contact(request):
    # show current logged in username
    context = {}
    context['username'] = request.user

    if request.user.is_authenticated:
        cardPriceNotificationMessage_qs = CardPriceNotificationMessage.objects.filter(
            user=request.user)
        context['msg_count'] = cardPriceNotificationMessage_qs.count

    return render(request, "TCGTrackingTool/contact.html", context=context)


def portfolio(request):
    '''
    @info: Retrieve all cards being tracked by the user
    and render a card list
    '''

    if not request.user.is_authenticated:
        return redirect('signin')
    # show current logged in username
    context = {}
    context['username'] = request.user

    sortType = None
    # sort cards based on sortType
    if request.POST and request.POST['sortType']:
        sortType = request.POST['sortType']

    # retrieve card tracked by the user
    inventory_qs = Inventory.objects.filter(user=request.user)
    inventory = inventory_qs.first()

    # if the user does not have an inventory, create one and assign it to user
    if not inventory:
        inventory = Inventory.objects.create(user=request.user)

    # sort query by sortType
    if sortType == 'alphabetic':
        card_qs = Card.objects.filter(
            inventory=inventory).order_by('card_name')
    elif sortType == 'lowest_price':
        card_qs = Card.objects.filter(
            inventory=inventory).order_by('latest_price')
    elif sortType == 'highest_price':
        card_qs = Card.objects.filter(
            inventory=inventory).order_by('-latest_price')
    elif sortType == 'new_to_old':
        card_qs = Card.objects.filter(
            inventory=inventory)
        card_qs = reversed(list(card_qs))
    else:
        # get all the cards that belong to the user's inventory
        card_qs = Card.objects.filter(inventory=inventory)

    serializer = CardSerializer(card_qs, many=True)

    context['card_list'] = serializer.data

    if request.user.is_authenticated:
        cardPriceNotificationMessage_qs = CardPriceNotificationMessage.objects.filter(
            user=request.user)
        context['msg_count'] = cardPriceNotificationMessage_qs.count

    short_url = []

    for card in context['card_list']:
        url = card['url']
        url = urlsplit(url)[2]

        card['edition_name'] = url[1:]
        short_url.append(card)

    context['shorten_url'] = short_url

    return render(request, "TCGTrackingTool/portfolio.html", context=context)


def faq(request):
    # show current logged in username
    context = {}
    context['username'] = request.user

    if request.user.is_authenticated:
        cardPriceNotificationMessage_qs = CardPriceNotificationMessage.objects.filter(
            user=request.user)
        context['msg_count'] = cardPriceNotificationMessage_qs.count

    return render(request, "TCGTrackingTool/FAQ.html", context=context)


def support(request):
    # show current logged in username
    context = {}
    context['username'] = request.user

    if request.user.is_authenticated:
        cardPriceNotificationMessage_qs = CardPriceNotificationMessage.objects.filter(
            user=request.user)
        context['msg_count'] = cardPriceNotificationMessage_qs.count

    return render(request, "TCGTrackingTool/support.html", context=context)


def profile(request):
    if not request.user.is_authenticated:
        return redirect('signin')
    context = {}
    context['username'] = request.user

    if request.user.is_authenticated:
        cardPriceNotificationMessage_qs = CardPriceNotificationMessage.objects.filter(
            user=request.user)
        context['msg_count'] = cardPriceNotificationMessage_qs.count

    return render(request, "TCGTrackingTool/profile.html", context=context)


def notifications(request):
    # show current logged in username
    context = {}
    context['username'] = request.user

    if request.user.is_authenticated:
        cardPriceNotificationMessage_qs = CardPriceNotificationMessage.objects.filter(
            user=request.user)
        context['msg_count'] = cardPriceNotificationMessage_qs.count

    # * Handle POST requests ------------------------------------------
    # remove a notification config setting
    notification_to_delete = request.POST.get('remove_notification_setting')
    if notification_to_delete:

        notification_qs = CardPriceNotification.objects.filter(
            card=notification_to_delete)
        notification = notification_qs.first()
        notification.delete()

        return redirect('notifications')

    if request.POST.get('remove_msg'):
        card_name = request.POST.get('card_name')
        card_edition = request.POST.get('card_edition')
        threshold_price = request.POST.get('threshold_price')
        notification_type = request.POST.get('notification_type')

        notification_msg_qs = CardPriceNotificationMessage.objects.filter(
            card_name=card_name, card_edition=card_edition, threshold_price=threshold_price, notification_type=notification_type
        )

        notification_msg = notification_msg_qs.first()
        notification_msg.delete()
        return redirect('notifications')

    # *----------------------------------------------------------------

    # retrieve all price notification set up by the user
    notifications_qs = CardPriceNotification.objects.filter(user=request.user)

    notification_sr = CardPriceNotificationSerializer(
        notifications_qs, many=True)

    context['notification_settings'] = notification_sr.data

    # retrieve all price notification messages
    notification_msg_qs = CardPriceNotificationMessage.objects.filter(
        user=request.user)[:10]

    notification_msg_sr = CardPriceNotificationMessageSerializer(
        notification_msg_qs, many=True)

    context['notification_msg'] = notification_msg_sr.data

    return render(request, "TCGTrackingTool/notifications.html", context=context)


def user_settings(request):
    # show current logged in username
    context = {}
    context['username'] = request.user

    if request.user.is_authenticated:
        cardPriceNotificationMessage_qs = CardPriceNotificationMessage.objects.filter(
            user=request.user)
        context['msg_count'] = cardPriceNotificationMessage_qs.count

    return render(request, "TCGTrackingTool/settings.html", context=context)


def register(request):
    if request.user.is_authenticated:
        return redirect('home')
    context = {}
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            # user = form.cleaned_data.get('username')
            # messages.success(request, 'Account was created for ' + user)
            return render(request, "TCGTrackingTool/account-created.html")
        else:
            errors = form.errors.as_data()
            error_fields = list(errors.keys())
            error_msgs = list(errors.values())

            context['error_msg'] = f'{error_fields[0]}: {error_msgs[0][0]}'
            return render(request, "TCGTrackingTool/register.html", context=context)

    context = {'form': form}
    return render(request, "TCGTrackingTool/register.html", context)


def signin(request):
    if request.user.is_authenticated:
        return redirect('home')
    context = {}

#    secret_key = recaptcha_secret_key

# captcha verification
#    data = {
#        'response': data.get('g-recaptcha-response'),
#        'secret': secret_key
#    }
#    resp = requests.post(
#        'https://www.google.com/recaptcha/api/siteverify', data=data)
#    result_json = resp.json()

#    print(result_json)

#    if not result_json.get('success'):
#        return render(request, "TCGTrackingTool/contact.html", {'is_robot': True})

# end captcha verification

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('portfolio')
        else:
            context['error_msg'] = 'Invalid Credentials'
            return render(request, "TCGTrackingTool/signin.html", context=context)

    return render(request, "TCGTrackingTool/signin.html", {'site_key': recaptcha_site_key})


def logout_user(request):
    logout(request)
    return redirect('home')


def account_created(request):
    if not request.user.is_authenticated:
        return redirect('signin')
    return render(request, "TCGTrackingTool/account-created.html")


def info_recovery(request):
    return render(request, "TCGTrackingTool/info-recovery.html")


def forgot_username(request):
    return render(request, "TCGTrackingTool/forgot-username.html")


def forgot_password(request):
    return render(request, "TCGTrackingTool/forgot-password.html")


def product(request):
    '''
    @info: Show the list of cards from a search
    '''

    access_token = get_access_token()

    if request.POST:
        card_name = request.POST['card_name']

    search_url = f'https://api.tcgplayer.com/catalog/products?productName={card_name}'
    headers = {'Authorization': f'Bearer {access_token}'}

    try:
        res = requests.get(search_url, headers=headers)
    except requests.exceptions.ConnectionError:
        res.status_code = "Connection refused"

    context = {}

    if request.user.is_authenticated:
        cardPriceNotificationMessage_qs = CardPriceNotificationMessage.objects.filter(
            user=request.user)
        context['msg_count'] = cardPriceNotificationMessage_qs.count

    # context['search_results'] = res.json()['results']

    results = []

    for card in res.json()['results']:
        url = card['url']
        url = urlsplit(url)[2]

        card['edition_name'] = url[1:]
        results.append(card)

    context['search_results'] = results

    # # Ignore this, used for testing #
    # logging.basicConfig(filename='test.log', level=logging.DEBUG)
    # logging.info(context['search_results'])  # will print a message to the console
    # # Ignore this, used for testing #

    if not context['search_results']:
        # show current logged in username
        # for product not found page
        context = {}
        context['username'] = request.user
        return render(request, "TCGTrackingTool/notFoundError.html", context=context)
    else:
        return render(request, 'TCGTrackingTool/product.html', context=context)


def add_card_view(request):
    '''
    @info: Add a card to the user's inventory
    '''

    if not request.user.is_authenticated:
        return redirect('signin')

    # check to see if card is already in the DB
    card_qs = Card.objects.filter(product_ID=request.POST.get('product_ID'))
    card = card_qs.first()

    # save the card in the DB if it is not in the DB
    if not card:
        card_obj = {}
        card_obj['product_ID'] = request.POST.get('product_ID')
        card_obj['card_name'] = request.POST.get('card_name')
        card_obj['image_url'] = request.POST.get('image_url')
        card_obj['category_ID'] = request.POST.get('category_ID')
        card_obj['group_ID'] = request.POST.get('group_ID')
        card_obj['url'] = request.POST.get('url')
        card = Card.objects.create(**card_obj)

    price_history_qs = CardPriceHistory.objects.filter(card=card)
    price_history = price_history_qs.first()

    # if no price history exists, fetch the price data
    if not price_history:
        access_token = get_access_token()
        search_url = f'https://api.tcgplayer.com/pricing/product/{card.product_ID}'
        headers = {'Authorization': f'Bearer {access_token}'}
        res = requests.get(search_url, headers=headers)

        results = res.json()['results']

        # Records card's today price
        results_json = json.dumps(results)
        # filter out card editions with no market price
        input_dict = json.loads(results_json)
        output_dict = [x for x in input_dict if x['marketPrice'] != None]

        if len(output_dict) > 0:
            card.latest_price = output_dict[0]['marketPrice']
            card.latest_price_card_type = output_dict[0]['subTypeName']
            card.save()

            output_json = json.dumps(output_dict)

            # prices field converts 'output_dict' to json
            card_price_history = CardPriceHistory(
                card=card, date=datetime.date.today(), prices=output_json)

            if card_price_history:
                card_price_history.save()

    inventory_qs = Inventory.objects.filter(user=request.user)
    inventory = inventory_qs.first()

    if not inventory:
        inventory = Inventory.objects.create(user=request.user)

    # add card to user's inventory
    card.inventory.add(inventory)

    return HttpResponse(status=204)


def remove_card_view(request):
    '''
    @info: Remove a card from the user's inventory, then render
    an updated portfolio page
    '''

    product_ID = request.POST['product_ID']

    card_qs = Card.objects.filter(product_ID=product_ID)
    card = card_qs.first()

    inventory_qs = Inventory.objects.filter(user=request.user)
    inventory = inventory_qs.first()

    card.inventory.remove(inventory)

    # render a new portfolio page with updated inventory
    context = {}

    context['username'] = request.user

    if request.user.is_authenticated:
        cardPriceNotificationMessage_qs = CardPriceNotificationMessage.objects.filter(
            user=request.user)
        context['msg_count'] = cardPriceNotificationMessage_qs.count

    card_qs = Card.objects.filter(inventory=inventory)
    serializer = CardSerializer(card_qs, many=True)

    context['card_list'] = serializer.data

    return render(request, "TCGTrackingTool/portfolio.html", context=context)


def current_price_detail(request):
    '''
    @info: Display the current price of the card
    '''

    # check to see if card is already in the DB
    card_qs = Card.objects.filter(product_ID=request.POST.get('product_ID'))
    card = card_qs.first()

    # save the card in the DB if it is not in the DB
    if not card:
        card_obj = {}
        card_obj['product_ID'] = request.POST.get('product_ID')
        card_obj['card_name'] = request.POST.get('card_name')
        card_obj['image_url'] = request.POST.get('image_url')
        card_obj['category_ID'] = request.POST.get('category_ID')
        card_obj['group_ID'] = request.POST.get('group_ID')
        card = Card.objects.create(**card_obj)

    context = {}
    context['card'] = card

    context['username'] = request.user

    if request.user.is_authenticated:
        cardPriceNotificationMessage_qs = CardPriceNotificationMessage.objects.filter(
            user=request.user)
        context['msg_count'] = cardPriceNotificationMessage_qs.count

    # get price info on the card
    access_token = get_access_token()

    search_url = f'https://api.tcgplayer.com/pricing/product/{card.product_ID}'
    headers = {'Authorization': f'Bearer {access_token}'}

    try:
        res = requests.get(search_url, headers=headers)
    except requests.exceptions.ConnectionError:
        res.status_code = "Connection refused"

    results = res.json()['results']

    prices = filter(lambda card: card['marketPrice'] != None, results)

    # prices for only normal cards are displayed (no speical editions)
    context['card_prices'] = prices

    return render(request, "TCGTrackingTool/current-price-detail.html", context=context)


def price_history_detail(request):
    '''
    @info: Display the price history of the card
    '''

    card_qs = Card.objects.filter(product_ID=request.POST.get('product_ID'))
    card = card_qs.first()

    # save the card in the DB if it does not exists in the db already
    if not card:
        card_obj = {}
        card_obj['product_ID'] = request.POST.get('product_ID')
        card_obj['card_name'] = request.POST.get('card_name')
        card_obj['image_url'] = request.POST.get('image_url')
        card_obj['category_ID'] = request.POST.get('category_ID')
        card_obj['group_ID'] = request.POST.get('group_ID')
        card_obj['url'] = request.POST.get('url')
        card = Card.objects.create(**card_obj)

    context = {}
    context['card'] = card
    context['username'] = request.user

    if request.user.is_authenticated:
        cardPriceNotificationMessage_qs = CardPriceNotificationMessage.objects.filter(
            user=request.user)
        context['msg_count'] = cardPriceNotificationMessage_qs.count

    price_history_qs = CardPriceHistory.objects.filter(card=card)
    price_history = price_history_qs.first()

    # if no price history exists, fetch the price data
    if not price_history:
        access_token = get_access_token()
        search_url = f'https://api.tcgplayer.com/pricing/product/{card.product_ID}'
        headers = {'Authorization': f'Bearer {access_token}'}
        res = requests.get(search_url, headers=headers)

        results = res.json()['results']

        # Records card's today price
        results_json = json.dumps(results)
        # filter out card editions with no market price
        input_dict = json.loads(results_json)
        output_dict = [x for x in input_dict if x['marketPrice'] != None]

        if len(output_dict) > 0:
            card.latest_price = output_dict[0]['marketPrice']
            card.latest_price_card_type = output_dict[0]['subTypeName']
            card.save()

            output_json = json.dumps(output_dict)

            # prices field converts 'output_dict' to json
            card_price_history = CardPriceHistory(
                card=card, date=datetime.date.today(), prices=output_json)

            print(card_price_history)

            if card_price_history:
                card_price_history.save()

    history_serializer = CardPriceHistorySerializer(
        price_history_qs, many=True)

    graph_data = {}

    # process price history data
    '''
        # * graph_data shape
        {
            subTypeName(edition name):{
                date: [],
                market_price: []
            },

        }
    '''

    # get the graph choice made by the user
    graph_choice = request.POST.get('graph_choice')

    for history in price_history_qs:
        price_json = json.loads(history.prices)
        for card in price_json:
            graph_data.setdefault(card['subTypeName'], {})
            graph_data[card['subTypeName']].setdefault(
                'date', []).append(history.date)
            graph_data[card['subTypeName']].setdefault(
                'market_price', []).append(card['marketPrice'])

    # **********************************************************
    # TODO: Clean up code here

    # create the choices for different editions of the cards
    context['graph_options'] = graph_data.keys()

    # send the chosen card's graph data
    if graph_choice:
        card_graph_data = graph_data[graph_choice]

        # convert graph data in to json
        card_graph_data_json = json.dumps(
            card_graph_data, cls=DjangoJSONEncoder)

        context['card_graph_data'] = card_graph_data_json
        context['card_edition'] = graph_choice

    # show default graph when user has not made a choice
    else:

        graph_data_keys = graph_data.keys()

        if not graph_data_keys:
            context['no_price_msg'] = 'No Price History'
            return render(request, "TCGTrackingTool/price-history-detail.html", context=context)

        card_graph_data = graph_data[
            list(graph_data.keys())[0]
        ]

        # convert graph data into json
        card_graph_data_json = json.dumps(
            card_graph_data, cls=DjangoJSONEncoder)

        context['card_graph_data'] = card_graph_data_json
        context['card_edition'] = list(graph_data.keys())[0]

    # **********************************************************
        access_token = get_access_token()

        product_ID = request.POST['product_ID']

        # Current problem, limit the search to the current product id
        # otherwise it searches for all the card editions

        search_url = f'https://api.tcgplayer.com/catalog/products/{product_ID}'
        headers = {'Authorization': f'Bearer {access_token}'}
        res = requests.get(search_url, headers=headers)

        results = []

        for card in res.json()['results']:
            url = card['url']
            url = urlsplit(url)[2]

            card['edition_name'] = url[1:]
            results.append(card)

        context['category_name'] = results

    # Ignore this, used for testing #
    # logging.basicConfig(filename='test.log', level=logging.DEBUG)
    # will print a message to the console
    # logging.info(context['category_name'])
    # Ignore this, used for testing #

    return render(request, "TCGTrackingTool/price-history-detail.html", context=context)


def create_notification(request):

    product_ID = request.POST.get('product_ID')
    below_price = request.POST.get('below_price')
    above_price = request.POST.get('above_price')
    card_edition = request.POST.get('card_edition')

    curr_card_qs = Card.objects.filter(product_ID=product_ID)
    curr_card = curr_card_qs.first()

    card_price_notification_qs = CardPriceNotification.objects.filter(
        card=curr_card)
    card_price_notification = card_price_notification_qs.first()

    if not card_price_notification:
        card_price_notification = CardPriceNotification(
            card=curr_card, product_ID=product_ID, card_name=curr_card.card_name, card_edition=card_edition, user=request.user, below_price=below_price, above_price=above_price)
    else:
        card_price_notification.below_price = below_price
        card_price_notification.above_price = above_price

    card_price_notification.save()

    notification_qs = CardPriceNotification.objects.filter(card=curr_card)

    return HttpResponse(status=204)


def messages(request):
    # show current logged in username
    context = {}
    context['username'] = request.user

    if request.user.is_authenticated:
        cardPriceNotificationMessage_qs = CardPriceNotificationMessage.objects.filter(
            user=request.user)
        context['msg_count'] = cardPriceNotificationMessage_qs.count

    return render(request, "TCGTrackingTool/messages.html", context=context)

# ----------------------------------------------------------------------------------
# * Utility Functions


def get_access_token():
    '''
    Retreive access_token from TCGPlayer API
    '''
    # receive access_token from TCG Player API
    url = 'https://api.tcgplayer.com/token'
    data = {'grant_type': 'client_credentials',
            'client_id': public_key, 'client_secret': private_key}

    res = requests.post(url, data=data)

    return res.json()['access_token']
