from django.apps import AppConfig
from django.db.models.signals import post_save


class ReservationConfig(AppConfig):
    name = 'reservation'

    def ready(self):
        from .models import Booking
        from .signals import update_timeslot_availability
        post_save.connect(update_timeslot_availability, sender=Booking)

