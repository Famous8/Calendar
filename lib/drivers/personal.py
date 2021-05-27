from datetime import datetime
import json


def getPersonal(date):
    personal = []
    with open('./lib/data/events.json', 'r') as f:
        file = json.load(f)

    for key in file['events'].keys():
        if file['events'][key]['repeat'] is not None:
            if type(file['events'][key]['repeat']) == dict:
                rep = checkRepeat(date, key, cus=file['events'][key]['repeat'])

            else:
                rep = checkRepeat(date, key, reptype=file['events'][key]['repeat'])

            if rep == True:
                personal.append(file['events'][key]['name'])

        if key == str(date):
            personal.append(file['events'][key]['name'])

    return list(set(personal))


def checkRepeat(curr, eve, reptype=None, cus=None):
    date1 = datetime.strptime(curr, "%Y-%m-%d")
    date2 = datetime.strptime(eve, "%Y-%m-%d")

    if reptype:
        if reptype.lower() == 'day':
            if date1 < date2:
                return False

            else:
                return True

        elif reptype.lower() == 'week':
            if date1 < date2:
                return False

            else:
                if (date1 - date2).days % 7 == 0:
                    return True

        elif reptype.lower() == 'month':
            if date1 < date2:
                return False

            elif date1.day == date2.day:
                try:
                    return True

                except ValueError:
                    return False

        elif reptype.lower() == 'year':
            if date1 < date2:
                return False

            elif date1.strftime('%m-%d') == date2.strftime('%m-%d'):
                try:
                    return True

                except ValueError:
                    return False

    elif cus:
        if cus['end'] is not None and date1 > datetime.strptime(cus['end'], "%Y-%m-%d"):
            return False

        if cus['every'].lower() == "week":
            if int((date1 - date2).days // 7) % int(cus['num']) == 0:
                if cus['days'] is not None and date1.strftime('%A') in cus['days']:
                    return True

                else:
                    return True

            else:
                return False

        if cus['every'].lower() == 'year':
            if date1 < date2:
                return False

            elif date1.year - date2.year == int(cus['num']) and date1.strftime('%m-%d') == date2.strftime('%m-%d'):
                return True

        if cus['every'].lower() == 'day':
            if int(date1.day) % int(cus['num']) == 0:
                return True

            else:
                return False

        if cus['every'].lower() == 'month':
            if date1.day == date2.day and (date1.month - date2.month) % int(cus['num']) == 0:
                return True

            else:
                return False

