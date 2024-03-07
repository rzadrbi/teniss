from django.contrib.auth.models import User
from django.db import models


class Teniss_Court(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.name}'


class texts(models.Model):
    titre1 = models.CharField(max_length=500, verbose_name='تیتر صفحه اصلی')
    text1 = models.TextField(verbose_name='متن صفحه اصلی')
    titre2 = models.CharField(max_length=500, verbose_name='تیتر صفحه آدینه')
    text2 = models.TextField(verbose_name='متن صفحه آدینه')
    titre3 = models.CharField(max_length=500, verbose_name='تیتر صفحه روز های هفته')
    text3 = models.TextField(verbose_name='متن صفحه روز های هفته')
    titre4 = models.CharField(max_length=500, verbose_name='تیتر صفحه تایم های آن روز')
    text4 = models.TextField(verbose_name='متن صفحه تایم های آن روز')
    titre5 = models.CharField(max_length=500, verbose_name='تیتر صفحه مسابفه دهندگان')
    text5 = models.TextField(verbose_name='متن صفحه مسابقه دهندگان')
    titre6 = models.CharField(max_length=500, verbose_name='تیتر صفحه صورتحساب آدینه')
    text6 = models.TextField(verbose_name='متن صفحه صورتحساب آدینه')
    titre7 = models.CharField(max_length=500, verbose_name='تیتر صفحه صورت حساب رزرو تایم')
    text7 = models.TextField(verbose_name='متن صفحه رزرو تایم')
    titre8 = models.CharField(max_length=500, verbose_name='تیتر صفحه وارد کردن مشخصات رزرو تایم')
    text8 = models.TextField(verbose_name='متن صفحه وارد کردن مشخصات رزرو تایم')

    def __str__(self):
        return (f'{self.titre1} {self.titre2} {self.titre3} {self.titre4} {self.titre5} {self.titre6} {self.titre7}'
                f' {self.titre8}')

class TimeSlot(models.Model):
    id = models.AutoField(primary_key=True, auto_created=True)
    court = models.ForeignKey(Teniss_Court, on_delete=models.CASCADE)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    available = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.court.name} - {self.date} - {self.start_time} - {self.end_time}'


class Booking(models.Model):
    time_slot = models.ForeignKey(TimeSlot, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    confirmed = models.BooleanField(default=False)
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.time_slot} - {self.full_name} - {self.phone_number}'


class Adineh(models.Model):
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    age = models.IntegerField()
    confirmed = models.BooleanField(default=False)
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.name} - {self.age}'
