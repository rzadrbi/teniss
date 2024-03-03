import datetime

# ایجاد یک لیست خالی
days = []

# ایجاد یک شیء تاریخ برای امروز
today = datetime.date.today()

# ایجاد یک حلقه for برای ۱۴ روز آینده
for i in range(14):
    # اضافه کردن یک روز به تاریخ امروز
    day = today + datetime.timedelta(days=i)
    # بررسی اینکه روز جمعه نباشد
    if day.weekday() != 4:
        # اضافه کردن روز به لیست
        days.append(day.strftime("%d-%m-%Y"))

# چاپ کردن لیست
print(days)