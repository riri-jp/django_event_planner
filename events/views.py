from django.db.models import Q
import datetime
from django.contrib import messages
from django.shortcuts import render, redirect
from .models import Event, BookEvent
from django.http import Http404, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.views import View
from .forms import UserSignup, UserLogin, EventForm, BookEventForm
import requests


#def events_search(request):
    #query = "Events"
    #url = "https://www.eventbriteapi.com/v3/events/search"+query
    #response = requests.get(url)
    #return JsonResponse(response.json(),safe=False)

def home(request):
    events = Event.objects.filter(date__gte=datetime.date.today()).order_by("date")[:6]
    context = {
        'events': events,
    }
    return render(request, 'home.html', context)

def event(request):
    events = Event.objects.filter(date__gte=datetime.date.today()).order_by("date")
    query = request.GET.get('search')
    if query:
        events = events.filter(
            Q(title__icontains=query)|
            Q(description__icontains=query)|
            Q(added_by__username__icontains=query)
        ).distinct()
    context = {
        'events': events
    }
    return render(request, 'event.html', context)

def event_detail(request, event_id):
    if request.user.is_anonymous:
        return redirect('login')
    event = Event.objects.get(id=event_id)
    ticket = event.tickets.all()

    context = {
        'event': event,
        'ticket': ticket,
        
    }
    return render(request, 'event_detail.html', context)


def add_event(request):
    if request.user.is_anonymous:
        return redirect('login')
    form = EventForm()
    if request.method == "POST":
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            event = form.save(commit=False)
            event.added_by = request.user
            event.save()
            return redirect('event')
    context = {
        'form':form,
    }
    return render(request, 'add_event.html', context)


def update_event(request, event_id):
    event = Event.objects.get(id=event_id)
    
    if request.user.is_anonymous:
        return redirect('login')
        
    if not request.user.is_staff and not request.user == event.added_by:
        raise Http404

    form = EventForm(instance=event)
    if request.method == "POST":
        form = EventForm(request.POST, request.FILES, instance=event)
        if form.is_valid():
            event.save()
            return redirect('event')
    context = {
        'form':form,
        'event':event,
    }
    return render(request, 'update_event.html', context)


def dashboard(request):
    if request.user.is_anonymous:
        return redirect('login')
    
    events = request.user.events.all()
    context = {
        'dashboard': True,
        'events':events,
    }
    return render(request, 'dashboard.html', context)

def booked(request):
    # event_booked = request.user.tickets.filter(event__date__lte=datetime.date.today())
    # future_events = request.user.tickets.filter(event__date__gte=datetime.date.today())

    bookevents = request.user.tickets.all()
    context = {
        'bookevents':bookevents,
        # 'future_events': future_events,
    }
    return render(request, 'booked.html', context)


def booking(request, event_id):
    event = Event.objects.get(id=event_id)
    if (request.user.is_anonymous):
       messages.success(request, "YOU CAN NOT BOOK YOU NEED TO SIGNIN " )
       return redirect("login")
    form = BookEventForm()
    if request.method == "POST":

        form = BookEventForm(request.POST)
        if event.remain_ticket() == 0:
            messages.warning(request,"No messages left")

        elif int(form['tickets'].value()) > event.remain_ticket():
            messages.warning(request,"too many!")

        elif form.is_valid():
            booking= form.save(commit=False)
            booking.event = event
            booking.user =request.user
            booking.save()
            messages.success(request, "HAVE FUN")
            return redirect('dashboard')
    context = {
       "form": form,
       "event": event,
    }
    return render(request, "booking.html", context)


def delete_event(request, event_id):
    
    
    if request.user.is_anonymous:
        return redirect('event')
        
    if not request.user.is_staff:
        raise Http404

    Event.objects.get(id=event_id).delete()
    return redirect('event')





class Signup(View):
    form_class = UserSignup
    template_name = 'signup.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(user.password)
            user.save()
            messages.success(request, "You have successfully signed up.")
            login(request, user)
            return redirect("event")
        messages.warning(request, form.errors)
        return redirect("signup")


class Login(View):
    form_class = UserLogin
    template_name = 'login.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):      
        form = self.form_class(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            auth_user = authenticate(username=username, password=password)
            if auth_user is not None:
                login(request, auth_user)
                messages.success(request, "Welcome Back!")
                return redirect('dashboard')
            messages.warning(request, "Wrong email/password combination. Please try again.")
            return redirect("login")
        messages.warning(request, form.errors)
        return redirect("login")


class Logout(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        messages.success(request, "You have successfully logged out.")
        return redirect("login")

