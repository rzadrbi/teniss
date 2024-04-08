from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from django.utils import timezone
from datetime import timedelta
from django.views.generic import ListView
import pandas as pd
from django.shortcuts import render
from .models import TimeSlot, Adineh, Booking, texts, match_tree, price
from django.conf import settings
import requests
import json


def index(request):
    text = texts.objects.all().first()
    today = timezone.localtime(timezone.now()).date()
    next_week = today + timedelta(days=7)
    dates = pd.date_range(today, next_week, freq='1440min').to_series()
    dates = dates[dates.dt.weekday != 4]
    for date in dates:
        TimeSlot.objects.get_or_create(court_id=1, date=date, start_time='9:00', end_time='10:00')
        TimeSlot.objects.get_or_create(court_id=1, date=date, start_time='10:00', end_time='11:00')
        TimeSlot.objects.get_or_create(court_id=1, date=date, start_time='11:00', end_time='12:00')
        TimeSlot.objects.get_or_create(court_id=1, date=date, start_time='14:00', end_time='15:00')
        TimeSlot.objects.get_or_create(court_id=1, date=date, start_time='15:00', end_time='16:00')
        TimeSlot.objects.get_or_create(court_id=1, date=date, start_time='16:00', end_time='17:00')
        TimeSlot.objects.get_or_create(court_id=1, date=date, start_time='17:00', end_time='18:00')
        TimeSlot.objects.get_or_create(court_id=1, date=date, start_time='18:00', end_time='19:00')
        TimeSlot.objects.get_or_create(court_id=1, date=date, start_time='19:00', end_time='20:00')
        TimeSlot.objects.get_or_create(court_id=1, date=date, start_time='20:00', end_time='21:00')
        TimeSlot.objects.get_or_create(court_id=1, date=date, start_time='21:00', end_time='22:00')
        TimeSlot.objects.get_or_create(court_id=1, date=date, start_time='22:00', end_time='23:00')
        TimeSlot.objects.get_or_create(court_id=1, date=date, start_time='23:00', end_time='00:00')
        TimeSlot.objects.get_or_create(court_id=2, date=date, start_time='9:00', end_time='10:00')
        TimeSlot.objects.get_or_create(court_id=2, date=date, start_time='10:00', end_time='11:00')
        TimeSlot.objects.get_or_create(court_id=2, date=date, start_time='11:00', end_time='12:00')
        TimeSlot.objects.get_or_create(court_id=2, date=date, start_time='14:00', end_time='15:00')
        TimeSlot.objects.get_or_create(court_id=2, date=date, start_time='15:00', end_time='16:00')
        TimeSlot.objects.get_or_create(court_id=2, date=date, start_time='16:00', end_time='17:00')
        TimeSlot.objects.get_or_create(court_id=2, date=date, start_time='17:00', end_time='18:00')
        TimeSlot.objects.get_or_create(court_id=2, date=date, start_time='18:00', end_time='19:00')
        TimeSlot.objects.get_or_create(court_id=2, date=date, start_time='19:00', end_time='20:00')
        TimeSlot.objects.get_or_create(court_id=2, date=date, start_time='20:00', end_time='21:00')
        TimeSlot.objects.get_or_create(court_id=2, date=date, start_time='21:00', end_time='22:00')
        TimeSlot.objects.get_or_create(court_id=2, date=date, start_time='22:00', end_time='23:00')
        TimeSlot.objects.get_or_create(court_id=2, date=date, start_time='23:00', end_time='00:00')
    return render(request, 'index.html', {'time_slots': TimeSlot.objects.all(), 'text': text})


class WeekDay(ListView):
    paginate_by = 8
    model = TimeSlot
    template_name = 'weekdays.html'
    context_object_name = 'days'


def days(request):
    text = texts.objects.all().first()
    today = timezone.localtime(timezone.now()).date()
    next_week = today + timedelta(days=7)
    dates = pd.date_range(today, next_week, freq='1440min').to_series()
    dates = dates[dates.dt.weekday != 4]
    return render(request, 'days.html', {'dates': dates, 'text': text, })


class TimeView(ListView):
    model = TimeSlot
    paginate_by = 5
    template_name = 'times.html'
    context_object_name = 'times'

    def get_context_data(self, **kwargs):
        contex = super().get_context_data()
        contex['text'] = texts.objects.all().first()
        contex['selected_date'] = self.kwargs['date']
        return contex

    def get_queryset(self):
        date = self.kwargs['date']
        return TimeSlot.objects.filter(date=date, available=True)


def PreReserv(request, id):
    Tslot = get_object_or_404(TimeSlot, id=id, available=True)
    text = texts.objects.all().first()
    if request.method == 'GET':
        return render(request, 'reserve.html', {"Tslot": Tslot, 'text': text})
    if request.method == 'POST':
        name = request.POST.get('user_name')
        phone = request.POST.get('user_phone')
        booking = Booking.objects.create(full_name=name, phone_number=phone, time_slot=Tslot)
        booking.save()
        Tslot.available = False
        Tslot.save()
        return redirect('reservation:factor', pk=booking.id)


def PreAdineh(request):
    if request.method == 'GET':
        text = texts.objects.all().first()
        return render(request, 'PreAdineh.html', {'text': text})

    if request.method == 'POST':
        user_fullname = request.POST.get('user_fullname')
        user_phone = request.POST.get('user_phone')
        user_age = request.POST.get('user_age')
        if user_fullname and user_phone and user_age:
            adenine = Adineh.objects.create(name=user_fullname, phone_number=user_phone, age=user_age)
            adenine.save()
            return redirect('reservation:index')


def AdinehList(request):
    adenines = Adineh.objects.filter(confirmed=True, is_paid=True)
    text = texts.objects.all().first()
    return render(request, 'ahineh_list.html', {"object": adenines, "text": text})


def page_not_found_view(request, exception):
    response = render(request, "404.html")
    response.status_code = 404
    return response


def match_tree_view(request):
    tree = match_tree.objects.all().first()
    text = texts.objects.all().first()
    return render(request, 'match_tree.html', {'MatchTree': tree, "text": text})


def factor(request, pk):
    booking = Booking.objects.get(id=pk)
    if request.method == 'GET':
        text = texts.objects.all().first()
        Price = price.objects.all().first()
        return render(request, 'factor.html', {"booking": booking, "text": text, "price": Price})
    if request.method == 'POST':
        return redirect('reservation:request', pk=booking.id)


sandbox = 'www'
ZP_API_REQUEST = f"https://{sandbox}.zarinpal.com/pg/rest/WebGate/PaymentRequest.json"
ZP_API_VERIFY = f"https://{sandbox}.zarinpal.com/pg/rest/WebGate/PaymentVerification.json"
ZP_API_STARTPAY = f"https://{sandbox}.zarinpal.com/pg/StartPay/"
description = "توضیحات مربوط به تراکنش را در این قسمت وارد کنید"  # Required
phone = 'YOUR_PHONE_NUMBER'  # Optional
# Important: need to edit for realy server.
CallbackURL = 'http://127.0.0.1:8080/verify/'


def send_request(request, pk):
    booking = Booking.objects.get(id=pk)
    Price = price.objects.all().first()
    data = {
        "MerchantID": settings.MERCHANT,
        "Amount": Price.Time,
        "Description": description,
        "Phone": booking.phone_number,
        "CallbackURL": CallbackURL,
    }
    request.session['booking_id'] = str(booking.id)
    data = json.dumps(data)
    headers = {'content-type': 'application/json', 'content-length': str(len(data))}
    try:
        response = requests.post(ZP_API_REQUEST, data=data, headers=headers, timeout=10)
        if response.status_code == 200:
            response = response.json()
            if response['Status'] == 100:
                return {'status': True, 'url': ZP_API_STARTPAY + str(response['Authority']),
                        'authority': response['Authority']}
            else:
                return {'status': False, 'code': str(response['Status'])}
        return response
    except requests.exceptions.Timeout:
        return {'status': False, 'code': 'timeout'}
    except requests.exceptions.ConnectionError:
        return {'status': False, 'code': 'connection error'}