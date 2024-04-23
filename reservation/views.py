from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta
from jdatetime import jalali
from persiantools.jdatetime import JalaliDate
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView
import pandas as pd
from django.shortcuts import render
from .models import TimeSlot, Adineh, Booking, texts, match_tree, price
from django.conf import settings
import requests
import json


#main page
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


class AdinehList(ListView):
    model = Adineh
    paginate_by = 5
    template_name = 'ahineh_list.html'
    context_object_name = 'object'

    def get_context_data(self, **kwargs):
        contex = super().get_context_data()
        contex['text'] = texts.objects.all().first()
        return contex

    def get_queryset(self):
        return Adineh.objects.filter(confirmed=True, is_paid=True)


@csrf_exempt
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
        user = User.objects.create(first_name=booking.full_name, username=booking.id, password=booking.phone_number)
        login(request, user)
        Tslot.save()
        return redirect('reservation:factor', pk=booking.id)


def page_not_found_view(request, exception):
    response = render(request, "404.html")
    response.status_code = 404
    return response


def match_tree_view(request):
    tree = match_tree.objects.all().first()
    text = texts.objects.all().first()
    return render(request, 'match_tree.html', {'MatchTree': tree, "text": text})


@csrf_exempt
def factor(request, pk):
    booking = Booking.objects.get(id=pk)
    Tslot = TimeSlot.objects.get(booking=booking)
    if request.method == 'GET':
        text = texts.objects.all().first()
        Price = price.objects.all().first()
        return render(request, 'factor.html', {"booking": booking, "text": text, "price": Price})
    if request.method == 'POST':
        if Tslot.available:
            return redirect('reservation:request', pk=booking.id)
        else:
            return render(request, 'TimeNotAv.html')


if settings.SANDBOX:
    sandbox = 'sandbox'
else:
    sandbox = 'www'
ZP_API_REQUEST = f"https://{sandbox}.zarinpal.com/pg/rest/WebGate/PaymentRequest.json"
ZP_API_VERIFY = f"https://{sandbox}.zarinpal.com/pg/rest/WebGate/PaymentVerification.json"
ZP_API_STARTPAY = f"https://{sandbox}.zarinpal.com/pg/StartPay/"
description = "توضیحات مربوط به تراکنش را در این قسمت وارد کنید"  # Required
phone = 'YOUR_PHONE_NUMBER'  # Optional


def send_request(request, pk):
    booking = Booking.objects.get(id=pk)
    Price = price.objects.all().first()
    data = {
        "MerchantID": settings.MERCHANT,
        "Amount": Price.Time,
        "Description": description,
        "Phone": booking.phone_number,
        "CallbackURL": 'https://partotennis.ir/verify',
    }
    data = json.dumps(data)
    headers = {'content-type': 'application/json', 'content-length': str(len(data))}
    try:
        response = requests.post(ZP_API_REQUEST, data=data, headers=headers, timeout=10)
        if response.status_code == 200:
            response = response.json()
            if response['Status'] == 100:
                url = f"{ZP_API_STARTPAY}{response['Authority']}"
                return redirect(url)
            else:
                return render(request, 'NotRedPay.html')
        return response
    except requests.exceptions.Timeout:
        return render(request, 'NotRedPay.html')
    except requests.exceptions.ConnectionError:
        return render(request, 'NotRedPay.html')


@csrf_exempt
def verify_payment(request):
    api = 'https://eitaayar.ir/api'
    token = "/bot259971:95b0266c-6494-4b5e-9767-fd6e1fd8305e/"
    authority = request.GET['Authority']
    Price = price.objects.all().first()
    booking_id = request.user.username
    booking = Booking.objects.get(id=int(float(booking_id)))
    Tslot = TimeSlot.objects.get(booking=booking)
    data = {
        "MerchantID": settings.MERCHANT,
        "Amount": Price.Time,
        'Authority': authority,
    }
    data = json.dumps(data)
    headers = {'content-type': 'application/json', 'content-length': str(len(data))}
    res = requests.post(ZP_API_VERIFY, data=data, headers=headers)
    if res.status_code == 200:
        response = res.json()
        if response['Status'] == 100:
            booking.is_paid = True
            booking.refid = response['RefID']
            booking.save()
            Tslot.available = False
            Tslot.save()
            reservDate = JalaliDate(Tslot.date)
            txt = f'''***رزرو تایم***
            روز : {reservDate}
            ساعت:{Tslot.start_time}--{Tslot.end_time}
            کاربر :{booking.full_name}
            موبایل:{booking.phone_number}
            شناسه پرداخت:{booking.refid}'''
            response2 = requests.get(
                api + token + 'sendMessage' + '?' + 'chat_id=' + 'partotennis' + '&' + '&text=' + f'{txt}')
            request.user.delete()
            logout(request)
            return render(request, 'SucPay.html', {"booking": booking,
                                                   "Tslot": Tslot,
                                                   'RefID': response['RefID']})
        else:
            booking.delete()
            request.user.delete()
            logout(request)
            return render(request, 'FailPay.html')
    booking.delete()
    request.user.delete()
    logout(request)
    return render(request, 'FailPay.html')


@csrf_exempt
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
            user = User.objects.create(first_name=adenine.name, username=adenine.id, password=adenine.phone_number)
            login(request, user)
            return redirect('reservation:factor_adineh', pk=adenine.id)


@csrf_exempt
def FactorAdineh(request, pk):
    adineh = Adineh.objects.get(id=pk)
    if request.method == 'GET':
        text = texts.objects.all().first()
        Price = price.objects.all().first()
        return render(request, 'factor_adineh.html', {"price": Price, "text": text, 'adineh': adineh})
    if request.method == 'POST':
        return redirect('reservation:request_adineh', pk=adineh.id)


def send_request_adineh(request, pk):
    adineh = Adineh.objects.get(id=pk)
    Price = price.objects.all().first()
    data = {
        "MerchantID": settings.MERCHANT,
        "Amount": Price.Adineh,
        "Description": description,
        "Phone": adineh.phone_number,
        "CallbackURL": 'https://partotennis.ir/verify_adineh',
    }
    data = json.dumps(data)
    headers = {'content-type': 'application/json', 'content-length': str(len(data))}
    try:
        response = requests.post(ZP_API_REQUEST, data=data, headers=headers, timeout=10)
        if response.status_code == 200:
            response = response.json()
            if response['Status'] == 100:
                url = f"{ZP_API_STARTPAY}{response['Authority']}"
                return redirect(url)
            else:
                return render(request, 'FailRedirect.html')
        return response
    except requests.exceptions.Timeout:
        return render(request, 'FailRedirect.html')
    except requests.exceptions.ConnectionError:
        return render(request, 'FailRedirect.html')


@csrf_exempt
def verify_payment_adineh(request):
    api = 'https://eitaayar.ir/api'
    token = "/bot259971:95b0266c-6494-4b5e-9767-fd6e1fd8305e/"
    authority = request.GET['Authority']
    Price = price.objects.all().first()
    adineh_id = request.user.username
    adineh = Adineh.objects.get(id=int(adineh_id))
    data = {
        "MerchantID": settings.MERCHANT,
        "Amount": Price.Adineh,
        'Authority': authority,
    }
    data = json.dumps(data)
    headers = {'content-type': 'application/json', 'content-length': str(len(data))}
    res = requests.post(ZP_API_VERIFY, data=data, headers=headers)
    if res.status_code == 200:
        response = res.json()
        if response['Status'] == 100:
            adineh.is_paid = True
            adineh.refid = response['RefID']
            adineh.save()
            txt = f'''***ثبت نام آدینه***
            نام : {adineh.name}
            موبایل : {adineh.phone_number}
            سن : {adineh.age}
            شناسه پرداخت:{adineh.refid}'''
            response2 = requests.get(
                api + token + 'sendMessage' + '?' + 'chat_id=' + 'partotennis_adineh' + '&' + '&text=' + f'{txt}')
            request.user.delete()
            logout(request)
            return render(request, 'SucPay_adineh.html', {"adineh": adineh,
                                                          'RefID': response['RefID']})
        else:
            adineh.delete()
            request.user.delete()
            logout(request)
            return render(request, 'FailPay.html')
    adineh.delete()
    request.user.delete()
    logout(request)
    return render(request, 'FailPay.html')


def signout(request):
    user = User.objects.get(username=request.user.username)
    logout(request)
    user.delete()
    return redirect('reservation:index')

