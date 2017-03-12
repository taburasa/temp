from django.shortcuts import render, redirect
from ..login_registration.models import User
from .models import Trip
from datetime import datetime
from django.contrib import messages
from django.db.models import Q

# Create your views here.
def index(request):
    context = {
        'user': User.objects.get(id=request.session['id']),
        'user_trips': Trip.objects.filter(Q(planner=request.session['id']) | Q(tagalongs__id__contains=request.session['id'])).distinct(),
        'other_trips': Trip.objects.exclude(planner=request.session['id']).exclude(tagalongs__id__contains=request.session['id'])
    }
    return render(request, 'travel_buddy/index.html', context)

def add(request):
    return render(request, 'travel_buddy/add.html')

def create(request):
    if request.method == 'POST':
        error_flag = False
        destination = request.POST.get('destination')
        description = request.POST.get('description')
        date_from = request.POST.get('date_from')
        date_to = request.POST.get('date_to')

        if len(destination) < 1:
            messages.add_message(request, messages.ERROR,
            'Destination may not be blank.')
            error_flag = True
        if len(description) < 1:
            messages.add_message(request, messages.ERROR,
            'Description may not be blank.')
            error_flag = True
        if date_from is None:
            messages.add_message(request, messages.ERROR,
            'Travel Date From may not be blank.')
            error_flag = True
        if date_to is None:
            messages.add_message(request, messages.ERROR,
            'Travel Date To may not be blank.')
            error_flag = True
        if date_from <= str(datetime.now()):
            messages.add_message(request, messages.ERROR,
            'Travel Date From must be in the future.')
            error_flag = True
        if date_to <= date_from:
            messages.add_message(request, messages.ERROR,
            'Travel Date To may not be before Travel Date From.')
            error_flag = True
        if error_flag == True:
            return redirect('travel_buddy:add')
        else:
            trip = Trip.objects.add_trip(request.POST) # TripManager method
            return redirect('travel_buddy:index')
    else:
        return redirect('travel_buddy:add')
    redirect('/')

def trip(request, trip_id):
    context = {
        'trip': Trip.objects.get(id=trip_id),
        'tagalongs': User.objects.filter(tagalong_trips__id__contains=trip_id)
    }
    return render(request, 'travel_buddy/trip.html', context)

def join(request, trip_id):
    trip = Trip.objects.get(id=trip_id)
    trip.tagalongs.add(request.session['id'])
    return redirect('travel_buddy:index')
