from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Booking, TimeSlot


@receiver(post_save, sender=Booking)
def update_timeslot_availability(sender, instance, **kwargs):
    if instance.is_paid:
        timeslot = instance.time_slot
        timeslot.available = False
        timeslot.save()
