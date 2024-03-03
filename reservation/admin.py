from django.contrib import admin
from reservation.models import TimeSlot, Booking, Teniss_Court, Adineh, texts
from jalali_date.admin import ModelAdminJalaliMixin

@admin.register(Adineh)
class AdinehAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    list_display = ('name', 'phone_number', 'age', 'is_paid', 'confirmed')


@admin.register(Teniss_Court)
class ReservationAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    list_display = ('name',)


@admin.register(TimeSlot)
class ReservationAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    list_display = ('court', 'date', 'start_time', 'end_time', 'available')
    list_filter = ('court', 'date', 'available')


@admin.register(Booking)
class ReservationAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    list_display = ('time_slot', 'full_name', 'confirmed', 'is_paid')
    list_filter = ('confirmed', 'is_paid')

@admin.register(texts)
class textsAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    list_display = ('titre1', )



