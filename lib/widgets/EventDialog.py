from kivy.core.window import Window
from kivy.properties import StringProperty, NumericProperty
from kivy.uix.scrollview import ScrollView
from kivymd.app import MDApp
from kivy.lang import Builder
from kivymd.uix.button import MDFlatButton
from kivymd.uix.screen import MDScreen
from kivymd.uix.list import OneLineListItem, TwoLineListItem, MDList
from kivymd.uix.snackbar import BaseSnackbar
from kivymd.uix.tab import MDTabsBase, MDTabs
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.dialog import MDDialog
from kivymd.uix.textfield import MDTextField
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel

from lib.drivers.holidays import Holidays
from lib.drivers.islamic import driver
from lib.drivers.personal import getPersonal
from lib.drivers.getdatelist import getDict, getstrftime

from hijri_converter import convert
from kivy.metrics import dp
from datetime import datetime
import json
import requests
import threading



APIKEY = '259ddcb11156c1648597938984b52919f458ec88e45a6364276e863b3289aadd'

kv = """
<WorldEvents>:
    BoxLayout:
        orientation: 'vertical'
        Widget:
            size_hint_y: .02
            
        MDLabel:
            text: "World Events:"
            padding_x: 15
            size_hint_y: .1
            pos_hint: {"center_y": .5}
            theme_text_color: "Custom"
            text_color: app.theme_cls.primary_color
        
        ScrollView:
            MDList:
                id: wrv

<PersonalEvents>:
    BoxLayout:
        orientation: 'vertical'
        MDLabel:
            text: "Personal Events:"
            padding_x: 15
            size_hint_y: .1
            pos_hint: {"center_y": .5}
            theme_text_color: "Custom"
            text_color: app.theme_cls.primary_color
        
        ScrollView:
            MDList:
                id: prv

<Tabs>:
    background_color: 0, 0, 0, 0
    size_hint_y: .25
    text_color_normal: app.theme_cls.primary_color
    text_color_active: app.theme_cls.primary_color
    underline_color: app.theme_cls.primary_color

<Tab>:
    text_color_normal: app.theme_cls.primary_color
    
<ErrorSnackbar>:
    MDIconButton:
        pos_hint: {'center_y': .5}
        icon: root.icon
        opposite_colors: True

    MDLabel:
        id: text_bar
        size_hint_y: None
        height: self.texture_size[1]
        text: root.text
        font_size: root.font_size
        theme_text_color: 'Custom'
        text_color: get_color_from_hex('ffffff')
        shorten: True
        shorten_from: 'right'
        pos_hint: {'center_y': .5}
"""

class ErrorSnackbar(BaseSnackbar):
    text = StringProperty(None)
    icon = StringProperty(None)
    font_size = NumericProperty("15sp")


class Tabs(MDTabs):
    pass


class Tab(MDFloatLayout, MDTabsBase):
    pass


class WorldEvents(MDScreen):
    pass


class PersonalEvents(MDScreen):
    pass


class EventItem(OneLineListItem):
    description = StringProperty()
    def on_release(self):
        dialog = MDDialog(
            title=self.text,
            text=str(self.description)
        )

        dialog.open()


class EventContent(MDScreen):
    def build(self):
        return Builder.load_string(kv)

    def create(self, year, month, day):
        self.build()

        country = driver().getCity()['countryCode']
        iso = datetime(int(year), int(month), int(day))

        key = getstrftime('%A, %B {S}, %Y', iso)
        islamic_date = getDict()[key].split(',')[1].strip()

        hijri = convert.Gregorian(year, month, day).to_hijri().datetuple()
        hijri_iso = f"{hijri[2]}-{hijri[1]}"
        islamic = []

        self.label = MDLabel()
        self.label.size_hint_y = .05
        self.label.font_size = "35px"
        self.label.halign = "center"
        self.label.text = islamic_date

        tabs = Tabs()
        tabs.on_tab_switch = self.on_tab_switch

        events = Screen(name='events')
        namaz = Screen(name='namaz')

        personal_events = getPersonal(str(iso).split()[0])

        layout = MDBoxLayout(orientation='vertical')
        eventslayout = MDBoxLayout(orientation='vertical')

        self.sm = ScreenManager()

        events.add_widget(eventslayout)

        self.sm.add_widget(events)
        self.sm.add_widget(namaz)

        tabs.add_widget(Tab(text="Events"))
        tabs.add_widget(Tab(text="Namaz Times"))
        personalscreen = PersonalEvents()
        world = WorldEvents()

        scroll = ScrollView()

        self.nrv = MDList()
        self.wrv = world.ids.wrv
        self.prv = personalscreen.ids.prv

        self.holidays = json.loads(requests.get(
            f'https://calendarific.com/api/v2/holidays?&api_key={APIKEY}&country={country}&year={year}').text)

        self.holidays['year'] = year

        with open('./lib/data/islamic.json', 'r', encoding="utf-8") as file:
            data = json.loads(str(file.read()))

        for key in data.keys():
            if key == hijri_iso:
                islamic.append(data[key]["event"])

        holidays = (Holidays().getHoliday(day, month, year, self.holidays))

        self.wrv.add_widget(OneLineListItem(text="No Events"))
        self.prv.add_widget(OneLineListItem(text="No Events"))

        if holidays or islamic:
            self.wrv.clear_widgets()

        for i in holidays + islamic:
            text = str(i)
            description = None

            if type(i) == dict:
                text = str(i['name'])
                description = str(i['description'])

            item = EventItem(text=str(text), description=str(description))
            self.wrv.add_widget(item)

        if personal_events:
            self.prv.clear_widgets()

        for x in personal_events:
            item = OneLineListItem(text=str(x))
            self.prv.add_widget(item)

        self.namaz_times = driver().getSalaatTimesForDate(iso)  

        for item in self.namaz_times.keys():
            self.nrv.add_widget(
                TwoLineListItem(text=str(item), secondary_text=str(self.namaz_times[item]), height=dp(50)))

        scroll.add_widget(self.nrv)

        layout.add_widget(self.label)
        layout.add_widget(tabs)
        layout.add_widget(self.sm)

        eventslayout.add_widget(world)
        eventslayout.add_widget(personalscreen)

        namaz.add_widget(scroll)
       

        self.sm.current = "events"
        self.add_widget(layout)

        return self

    def switch_year(self, year):
        thread = threading.Thread(target=self.setHoliday, args=(year,))
        thread.start()

        return self.holidays

    def setHoliday(self, year):
        country = driver().getCity()['countryCode']
        self.holidays = json.loads(requests.get(
            f'https://calendarific.com/api/v2/holidays?&api_key={APIKEY}&country={country}&year={year}').text)

    def switch_dates(self, year, month, day):
        iso = datetime(int(year), int(month), int(day))

        key = getstrftime('%A, %B {S}, %Y', iso)
        islamic_date = getDict()[key].split(',')[1].strip()
        self.label.text = islamic_date

        thread = threading.Thread(target=self.setNamaz, args=(iso,))
        thread.start()

        hijri = convert.Gregorian(year, month, day).to_hijri().datetuple()
        hijri_iso = f"{hijri[2]}-{hijri[1]}"
        islamic = []

        personal_events = getPersonal(str(iso).split()[0])

        with open('./lib/data/islamic.json', 'r', encoding="utf-8") as file:
            data = json.loads(str(file.read()))

        for key in data.keys():
            if key == hijri_iso:
                islamic.append(data[key]["event"])

        self.wrv.clear_widgets()
        self.prv.clear_widgets()

        holidays = (Holidays().getHoliday(day, month, year, self.holidays))

        self.wrv.add_widget(OneLineListItem(text="No Events"))
        self.prv.add_widget(OneLineListItem(text="No Events"))

        if holidays or islamic:
            self.wrv.clear_widgets()

        for i in holidays + islamic:
            text = str(i)
            description = None

            if type(i) == dict:
                text = str(i['name'])
                description = str(i['description'])

            item = EventItem(text=str(text), description=str(description))
            self.wrv.add_widget(item)

        if personal_events:
            self.prv.clear_widgets()

        for x in personal_events:
            item = OneLineListItem(text=str(x))
            self.prv.add_widget(item)

    def on_tab_switch(self, *args):
        if args[2] == "Events":
            self.sm.transition.direction = 'right'
            self.sm.current = "events"

        elif args[2] == "Namaz Times":
            self.sm.transition.direction = 'left'
            self.sm.current = "namaz"

    def setNamaz(self, iso):
        self.namaz_times = driver().getSalaatTimesForDate(str(iso).split()[0])

        self.nrv.clear_widgets()

        for item in self.namaz_times.keys():
            self.nrv.add_widget(TwoLineListItem(text=str(item), secondary_text=str(self.namaz_times[item]), height=dp(60)))

class test(MDApp):
    def build(self):
        self.content = EventContent(size_hint_y=None, height=400).create(2021, 4, 29)
        self.layout = MDBoxLayout(orientation='vertical')
        self.textfield = MDTextField(hint_text="Type Here")
        self.button = MDFlatButton(text="Change Date", on_release=self.changedate)

        self.layout.add_widget(self.textfield)
        self.layout.add_widget(self.button)
        self.layout.add_widget(self.content)

        return self.layout

    def changedate(self, instance):
        text = self.textfield.text.split('|')
        self.content.switch_dates(int(text[0]), int(text[1]), int(text[2]))


if __name__ == '__main__':
    test().run()
