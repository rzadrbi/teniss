from django.contrib import admin
from reservation.models import TimeSlot, Booking, Teniss_Court, Adineh, texts, match_tree, price
from jalali_date.admin import ModelAdminJalaliMixin


@admin.register(Adineh)
class AdinehAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    list_display = ('name', 'phone_number', 'age', 'is_paid', 'confirmed')
    list_filter = ('is_paid', 'confirmed')
    search_fields = ('refid', 'name', 'phone_number',)


@admin.register(Teniss_Court)
class ReservationAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    list_display = ('name',)


@admin.register(match_tree)
class treeAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    list_display = ('name',)


@admin.register(TimeSlot)
class ReservationAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    list_display = ('court', 'date', 'start_time', 'end_time', 'available')
    list_filter = ('court', 'date', 'available')


@admin.register(Booking)
class ReservationAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    list_display = ('time_slot', 'full_name', 'confirmed', 'is_paid')
    list_filter = ('confirmed', 'is_paid', )
    search_fields = ('refid', 'full_name', 'phone_number',)


@admin.register(texts)
class textsAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    list_display = ('titre1', )


@admin.register(price)
class textsAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    list_display = ('Time', 'Adineh',)