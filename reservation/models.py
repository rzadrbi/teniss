from django.contrib.auth.models import User
from django.db import models


class Teniss_Court(models.Model):
    name = models.CharField(max_length=100, verbose_name= 'نام زمین')

    class Meta:
        verbose_name_plural = 'زمین ها'
        verbose_name = 'زمین'

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
    titre9 = models.CharField(max_length=500, verbose_name='تیتر صفحه جدول', default='s')
    text9 = models.TextField(verbose_name='متن صفحه جدول', default='s')

    class Meta:
        verbose_name_plural = 'متن ها'
        verbose_name = 'متن'

    def __str__(self):
        return (f'{self.titre1} {self.titre2} {self.titre3} {self.titre4} {self.titre5} {self.titre6} {self.titre7}'
                f' {self.titre8}')


class TimeSlot(models.Model):
    id = models.AutoField(primary_key=True, auto_created=True, verbose_name= 'ایدی')
    court = models.ForeignKey(Teniss_Court, on_delete=models.CASCADE, verbose_name= 'زمین')
    date = models.DateField(verbose_name= 'روز')
    start_time = models.TimeField(verbose_name= 'تاریخ شروع')
    end_time = models.TimeField(verbose_name= 'تاریخ اتمام')
    available = models.BooleanField(default=True, verbose_name= 'در دسترس')

    class Meta:
        verbose_name_plural = 'تایم ها'
        verbose_name = 'تایم'

    def __str__(self):
        return f'{self.court.name} - {self.date} - {self.start_time} - {self.end_time}'


class Booking(models.Model):
    time_slot = models.ForeignKey(TimeSlot, on_delete=models.CASCADE, verbose_name= 'تایم')
    full_name = models.CharField(max_length=100, verbose_name= 'نام و نام خانوادگی')
    phone_number = models.CharField(max_length=15, verbose_name='موبایل')
    confirmed = models.BooleanField(default=False, verbose_name='تایید')
    is_paid = models.BooleanField(default=False, verbose_name='پرداخت شده')
    refid = models.CharField(max_length=200, null=True, blank=True, verbose_name='شناسه پرداخت')

    class Meta:
        verbose_name_plural = 'رزرو ها'
        verbose_name = 'رزرو'

    def __str__(self):
        return f'{self.time_slot} - {self.full_name} - {self.phone_number}'


class Adineh(models.Model):
    name = models.CharField(max_length=100, verbose_name= 'نام و نام خانوادگی')
    phone_number = models.CharField(max_length=15, verbose_name= 'موبایل')
    age = models.IntegerField(verbose_name= 'سن')
    confirmed = models.BooleanField(default=False, verbose_name= 'تایید')
    is_paid = models.BooleanField(default=False, verbose_name= 'پرداخت شده')
    refid = models.CharField(max_length=200, null=True, blank=True, verbose_name= 'شناسه پرداخت')

    class Meta:
        verbose_name_plural = 'آدینه ها'
        verbose_name = 'آدینه'

    def __str__(self):
        return f'{self.name} - {self.age}'


class match_tree(models.Model):
    name = models.CharField(max_length=100, verbose_name= 'نام')
    tree = models.ImageField(upload_to='treepic', verbose_name='درخت')

    class Meta:
        verbose_name_plural = 'جدول های مسابقه'
        verbose_name = 'جدول مسابقه'

    def __str__(self):
        return f'{self.name} - {self.tree}'


class price(models.Model):
    Time = models.IntegerField(verbose_name= 'قیمت رزرو تایم')
    Adineh = models.IntegerField(verbose_name= 'قیمت ثبت نام آدینه')

    class Meta:
        verbose_name_plural = 'قیمت ها'
        verbose_name = 'قیمت'

    def __str__(self):
        return f'{self.Time} - {self.Adineh}'
