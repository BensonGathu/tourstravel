# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.messages import constants as messages
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse, Http404, HttpResponseNotAllowed
from .forms import *
from .models import *
from .decorators import *
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail, BadHeaderError
# from .lipanampesa import *


# Create your views here.


def customer_registration(request):
    if request.method == 'POST':
        form = CustomerSignUpForm(request.POST)
        # import pdb
        # pdb.set_trace()
        if form.is_valid():
            user = form.save()
            first_name = form.cleaned_data.get('first_name')
            messages.success(
                request, first_name + ' ' + 'your account was created successfully!')
            return redirect('login')
    else:
        form = CustomerSignUpForm()

    context = {
        'form': form
    }
    return render(request, 'auth/register_customer.html', context)


def admin_registration(request):
    if request.method == 'POST':
        form = AdminSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            first_name = form.cleaned_data.get('first_name')
            messages.success(
                request, first_name + ' ' + 'your account was created successfully!')
            return redirect('login')
    else:
        form = AdminSignUpForm()

    context = {
        'form': form
    }
    return render(request, 'auth/register_admin.html', context)


# @unauthenticated_user
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username,
                            password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Logged in as' + ' ' + username)
            if user.is_admin:
                return redirect('dashboard')
            if user.is_customer:
                return redirect('home')
        else:
            messages.error(request, 'Invalid Username and/or Password')

    context = {}
    return render(request, 'auth/login.html', context)


def logoutUser(request):
    current_user = request.user
    logout(request)
    messages.info(
        request, 'You have logged out. Log back in to book our services.')
    if current_user.is_admin:
        return redirect('home')
    return redirect('login')


@login_required
def profile(request):
    current_user = request.user
    if current_user.is_customer:
        if request.method == 'POST':
            u_form = CustomerUpdateForm(
                request.POST, instance=request.user)
            c_form = CustomerProfileUpdateForm(
                request.POST, request.FILES, instance=request.user.customer)
            if u_form.is_valid() and c_form.is_valid():
                u_form.save()
                c_form.save()
                messages.success(request, f'Your account has been updated!')
                return redirect('profile')
        else:
            u_form = CustomerUpdateForm(instance=request.user)
            c_form = CustomerProfileUpdateForm(instance=request.user.customer)

    if current_user.is_admin:
        if request.method == 'POST':
            u_form = AdminUpdateForm(
                request.POST, instance=request.user)
            c_form = AdminProfileUpdateForm(
                request.POST, request.FILES, instance=request.user.admin_user)
            if u_form.is_valid() and c_form.is_valid():
                u_form.save()
                c_form.save()
                messages.success(request, f'Your account has been updated!')
                return redirect('profile')
        else:
            u_form = AdminUpdateForm(instance=request.user)
            c_form = AdminProfileUpdateForm(
                instance=request.user.admin_user)

    context = {'u_form': u_form,
               'c_form': c_form,
               'current_user': current_user,
               }

    return render(request, 'profile.html', context)


def home(request):
    current_user = request.user
    roadtrips = Road_trips.objects.filter(id__lte=4)
    adventures_safaris = Adventures_safaris.objects.all()
    gallery = Gallery.objects.all()
    footer_gallery = Gallery.objects.filter(id__lte=3)
    if request.method == 'GET':
        form = ContactForm()
    else:
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            from_email = form.cleaned_data['from_email']
            message = form.cleaned_data['message']
            if subject and message and from_email:
                try:
                    send_mail(subject, message, from_email, [
                        'capemedia2v@gmail.com'], fail_silently=False)
                except BadHeaderError:
                    messages.warning(
                        request, f'Mail could not be sent!')
                    return redirect('home')
                messages.success(
                    request, f'Message sent! Thank you for your feedback and/or message, we will contact you when we get your email.')
                return redirect('home')
            else:
                messages.error(
                    request, f'Make sure all fields are entered and valid.')
                return redirect('home')

    context = {'current_user': current_user,
               'roadtrips': roadtrips,
               'form': form,
               'adventures_safaris': adventures_safaris,
               'gallery': gallery,
               'footer_gallery': footer_gallery
               }
    return render(request, 'index.html', context)


def specific_trip(request, id):
    trip = Road_trips.objects.filter(id__exact=id).get()
    footer_gallery = Gallery.objects.filter(id__lte=3)
    # other_trip = Road_trips.objects.filter(id__exact=int(id)-1).get()
    # other_tripp = Road_trips.objects.filter(id__exact=int(id)-2).get()

    context = {'trip': trip,
               'footer_gallery': footer_gallery
               #    'other_trip': other_trip,
               #    'other_tripp': other_tripp
               }
    return render(request, 'a_tour.html', context)


@login_required
@admin_required
def dashboard(request):
    trips_count = Road_trips.objects.count()
    group_count = Group_tours.objects.count()
    customers_count = Customer.objects.count()
    adventures_count = Adventures_safaris.objects.count()
    gallery_count = Gallery.objects.count()
    # customer = Customer.objects.all()

    context = {'trips_count': trips_count,
               'customers_count': customers_count,
               #    'customers': customers,
               'group_count': group_count,
               'adventures_count': adventures_count,
               'gallery_count': gallery_count
               }
    return render(request, 'dashboard/dashboard.html', context)


@login_required
@admin_required
def group_tours(request):
    current_user = request.user
    form = group_tour_form(request.POST or None,
                           request.FILES or None)
    if current_user.is_admin and current_user.is_authenticated:
        if request.method == 'POST':
            form = group_tour_form(
                request.POST or None, request.FILES or None)
            if form.is_valid():
                form.save()
                messages.success(
                    request, f'You have successfully booked this group tour.')
                return redirect('dashboard')

    context = {'form': form,
               'current_user': current_user
               }
    return render(request, 'dashboard/group_tours.html', context)


@login_required
@admin_required
def road_trips(request):
    current_user = request.user
    form = road_trip_form(request.POST or None, request.FILES or None)
    if current_user.is_admin and current_user.is_authenticated:
        if request.method == 'POST':
            form = road_trip_form(request.POST or None,
                                  request.FILES or None)
            if form.is_valid():
                form.save()
                messages.success(
                    request, f'You have successfully booked this road trip.')
                return redirect('dashboard')

    context = {'form': form,
               'current_user': current_user
               }
    return render(request, 'dashboard/road_trips.html', context)


@login_required
@admin_required
def adventures_safaris(request):
    current_user = request.user
    form = adventures_safarisForm(
        request.POST or None, request.FILES or None)
    if current_user.is_admin and current_user.is_authenticated:
        if request.method == 'POST':
            form = adventures_safarisForm(request.POST or None,
                                          request.FILES or None)
            if form.is_valid():
                form.save()
                messages.success(
                    request, f'You have successfully posted an adventure and safaris.')
                return redirect('dashboard')

    context = {'form': form,
               'current_user': current_user
               }
    return render(request, 'dashboard/adventures_safaris.html', context)


def trips(request):
    trips = Road_trips.objects.all()
    footer_gallery = Gallery.objects.filter(id__lte=3)

    context = {'trips': trips,
               'footer_gallery': footer_gallery
               }
    return render(request, 'trips.html', context)


@login_required
@auth_required
def bookings(request, id):
    print(request.POST['totalPriceView'])
    current_user = request.user
    trip = Road_trips.objects.get(id=id)
    price = trip.price
    if current_user.is_authenticated and current_user.is_active:
        if request.method == 'POST':
            if request.POST['totalPriceView']:
                total_amount = request.POST['totalPriceView']
                phoneNumber = current_user.customer.contacts
                if price * request.POST['members'] != request.POST['totalPriceView']:
                    messages.error(
                        request, f'This is not what your not suppossed to pay')

                # try:
                #     lipa_na_mpesa(total_amount, phoneNumber)
                # except BadHeaderError:
                #     messages.warning(
                #         request, f'Transaction failed')
                #     messages.success(
                #         request, f'You have successfully booked it.')
                #     return redirect('')

    footer_gallery = Gallery.objects.filter(id__lte=3)

    context = {'current_user': current_user,
               'trip': trip,
               #    'u_form': u_form,
               'footer_gallery': footer_gallery
               }
    return render(request, 'bookings.html', context)


def search_tours(request):
    if 'road_trips' in request.GET and request.GET["road_trips"]:
        search_tour = request.GET.get("road_trips")
        tour_search = Road_trips.get_tour(search_tour)
        message = f"{search_tour}"
        context = {
            'message': message,
            'trips': tour_search
        }
        return render(request, 'tours_search.html', context)
    else:
        message = "You haven't searched for any tours"
        return render(request, 'tours_search.html', {"message": message})


def contact(request):
    footer_gallery = Gallery.objects.filter(id__lte=3)
    if request.method == 'GET':
        form = ContactForm()
    else:
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            from_email = form.cleaned_data['from_email']
            message = form.cleaned_data['message']
            if subject and message and from_email:
                try:
                    send_mail(subject, message, from_email, [
                              'capemedia2v@gmail.com'], fail_silently=False)
                except BadHeaderError:
                    messages.warning(
                        request, f'Mail could not be sent!')
                    return redirect('contact')
                messages.success(
                    request, f'Message sent! Thank you for your feedback and/or message, we will contact you when we get your email.')
                return redirect('contact')
            else:
                messages.error(
                    request, f'Make sure all fields are entered and valid.')
                return redirect('contact')

    context = {'form': form,
               'footer_gallery': footer_gallery
               }
    return render(request, 'contact.html', context)


def gallery_post(request):
    current_user = request.user
    form = galleryForm(request.POST or None, request.FILES or None)
    if current_user.is_admin and current_user.is_authenticated:
        if request.method == 'POST':
            form = galleryForm(request.POST or None, request.FILES or None)
            if form.is_valid():
                form.save()
                messages.success(
                    request, f'You have successfully posted an gallery picture.')
                return redirect('dashboard')

    context = {'form': form,
               'current_user': current_user
               }
    return render(request, 'dashboard/gallery.html', context)


def gallery(request):
    photos = Gallery.objects.all()
    photos_no = Gallery.objects.count()
    first_half = photos_no // 2
    pics = Gallery.objects.filter(id__lte=first_half)
    other_pics = Gallery.objects.filter(id__gt=first_half)

    context = {'photos': photos,
               'pics': pics,
               'other_pics': other_pics
               }
    return render(request, 'gallery.html', context)


def about(request):
    footer_gallery = Gallery.objects.filter(id__lte=3)

    context = {'footer_gallery': footer_gallery}
    return render(request, 'about.html', context)


def a_tour(request, id):
    trip = Adventures_safaris.objects.filter(id__exact=id).get()
    footer_gallery = Gallery.objects.filter(id__lte=3)

    context = {'trip': trip,
               'footer_gallery': footer_gallery
               }
    return render(request, 'past_stuff.html', context)


def elements(request):

    context = {}
    return render(request, 'elements.html', context)
