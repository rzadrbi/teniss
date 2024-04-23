from django.urls import path
from reservation import views

app_name = 'reservation'

urlpatterns = [
    path('', views.index, name='index'),
    path('weekdays', views.WeekDay.as_view(), name='weekdays'),
    path('days', views.days, name='days'),
    path('reservation/<int:id>', views.PreReserv, name='reservation'),
    path('times/<str:date>', views.TimeView.as_view(), name='times'),
    path('adineh_list', views.AdinehList.as_view(), name='adineh_list'),
    path('adineh', views.PreAdineh, name='adineh'),
    path('tree', views.match_tree_view, name='tree'),
    path('factor/<int:pk>', views.factor, name='factor'),
    path('factor_adineh/<int:pk>', views.FactorAdineh, name='factor_adineh'),
    path('request/<int:pk>', views.send_request, name='request'),
    path('request_adineh/<int:pk>', views.send_request_adineh, name='request_adineh'),
    path('verify/', views.verify_payment, name='verify'),
    path('verify_adineh/', views.verify_payment_adineh, name='verify_adineh'),
]
