from django import forms
from reservation.models import Booking


class ReservationForm(forms.ModelForm):
    class Meta:
        model = Booking
        exclude = ['id', 'is_paid', 'confirmed']
