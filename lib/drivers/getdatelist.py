from hijri_converter import convert
from datetime import timedelta, date

class my_dictionary(dict):
    def __init__(self):
        self = dict()

    def add(self, key, value):
        self[key] = value

dict = my_dictionary()

def suffix(d):
    return 'th' if 11 <= d <= 13 else {1: 'st', 2: 'nd', 3: 'rd'}.get(d % 10, 'th')


def getstrftime(format, t):
    return t.strftime(format).replace('{S}', str(t.day) + suffix(t.day))

def daterange(date1, date2):
    for n in range(int ((date2 - date1).days)+1):
        yield date1 + timedelta(n)

start_dt = date(1990, 1, 1)
end_dt = date(2070, 12, 31)

for dt in daterange(start_dt, end_dt):
    y = int(dt.strftime("%Y"))
    m = int(dt.strftime("%m"))
    d = int(dt.strftime("%d"))
    hijri = convert.Gregorian(y, m, d).to_hijri()
    hdt = hijri.datetuple()
    dict.add(getstrftime('%A, %B {S}, %Y', dt), f"{hijri.day_name()}, {hijri.month_name()} {(hdt[2])}{suffix(hdt[2])}, {hdt[0]}")


def getDict():
    return dict

def getDayNum(day):
    daydict = {"MONDAY": 1, "TUESDAY": 2, "WEDNESDAY": 3, "THURSDAY": 4, "FRIDAY": 5, "SATURDAY": 6, "SUNDAY": 7}
    return daydict[day.upper()]

def getMonthDays(month, year):
    if (year % 4) == 0:
        if (year % 100) == 0:
            if (year % 400) == 0:
                feb = 29
            else:
                feb = 28
        else:
            feb = 29
    else:
        feb = 28

    monthdict = {"JANUARY": 31, "FEBRUARY": feb, "MARCH": 31, "APRIL": 30, "MAY": 31, "JUNE": 30, 'JULY': 31,
                 'AUGUST': 31, "SEPTEMBER": 30, "OCTOBER": 32, "NOVEMBER": 30, "DECEMBER": 31}

    return monthdict[month.upper()]

def isLeap(year):
    if (year % 4) == 0:
        if (year % 100) == 0:
            if (year % 400) == 0:
                return True
            else:
                return False
        else:
            return True
    else:
        return False

def getMonth(month):
    months = {'January': 1, 'February': 2, 'March': 3, 'April': 4,
              'May': 5, 'June': 6, 'July': 7, 'August': 8, 'September': 9,
              'October': 10, 'November': 11, 'December': 12}

    return months[month]

def getDay(string):
    nums = ''
    for i in string:
        if i in '0123456789':
            nums += i

    return int(nums)



