from django import forms
from reservation.models import Booking, Adineh


class ReservationForm(forms.ModelForm):
    class Meta:
        model = Booking
        exclude = ['id', 'is_paid', 'confirmed']


class AdinehForm(forms.ModelForm):
    class Meta:
        model = Adineh
        exclude = ['id', 'is_paid', ]