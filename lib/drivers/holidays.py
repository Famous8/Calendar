from tornado.platform.asyncio import AnyThreadEventLoopPolicy
import json
import asyncio
import aiohttp

asyncio.set_event_loop_policy(AnyThreadEventLoopPolicy())
APIKEY = '259ddcb11156c1648597938984b52919f458ec88e45a6364276e863b3289aadd'


class Holidays():
    def __init__(self):
        pass

    async def main(self, year, country):
        async with aiohttp.ClientSession() as session:
            async with session.get(
                    f'https://calendarific.com/api/v2/holidays?&api_key={APIKEY}&country={country}&year={year}') as req:
                text = await req.text()
                return json.loads(text)

    def createHolidays(self, year, country):
        loop = asyncio.get_event_loop()
        holidays = loop.run_until_complete(self.main(year, country))
        return holidays

    def getHoliday(self, day, month, year, dict):
        list = []

        iso = f'{year}-{"%02d" % month}-{"%02d" % day}'

        for event in dict["response"]["holidays"]:
            if event["date"]["iso"] == iso:
                list.append(event)

        return list

if __name__ == '__main__':
    print(Holidays().getHoliday(10, 5, 2021, Holidays().createHolidays(2021, 'US'))[1])
