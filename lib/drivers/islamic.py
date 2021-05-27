from requests import get
from datetime import datetime
import json


class driver(object):
    def getIP(self):
        return get('https://api.ipify.org').text

    def getCity(self):
        return json.loads(get(
            f"http://api.ipinfodb.com/v3/ip-city/?key=20b96dca8b9a5d37b0355e9461c66e76eed30a2274422fa6213d9de6ffb2b34e&format=json&ip={self.getIP()}").text)

    
    def getSalaatTimesForDate(self, iso):
        iso = str(iso).split()[0].split('-')
        iso = f"{iso[2]}-{iso[1]}-{iso[0]}"

        times = json.loads(
            get(
                f"http://api.aladhan.com/v1/calendarByCity?city={self.getCity()['cityName']}&country={self.getCity()['countryName']}&method=0&month={iso.split('-')[1]}&year={iso.split('-')[2]}").text)

        date = [time for time in times['data'] if time['date']['gregorian']['date'] == iso]
        times = date[0]['timings']

        for time in times:
            strp = datetime.strptime(times[time].split()[0], '%H:%M').strftime('%I:%M%p')
            times[time] = str(strp)

        return times