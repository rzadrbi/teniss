from django.urls import path
from reservation import views

app_name = 'reservation'

urlpatterns = [
    path('', views.index, name='index'),
    path('weekdays', views.WeekDay.as_view(), name='weekdays'),
    path('days', views.days, name='days'),
    path('reservation/<int:id>', views.PreReserv, name='reservation'),
    path('times/<str:date>', views.TimeView.as_view(), name='times'),
    path('adineh_list', views.AdinehList, name='adineh_list'),
    path('adineh', views.PreAdineh, name='adineh'),
]