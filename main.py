from kivy.base import ExceptionManager, ExceptionHandler
from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog
from kivymd.uix.picker import MDThemePicker
from kivy.properties import ObjectProperty, Logger
from lib.widgets.YearDialog import YearContent, CustomRecycle
from lib.widgets.MainWidgets import *
from lib.widgets.AboutDialogs import MoreInfo, License
from lib.widgets.CreateEventDialog import EventChooser
from lib.widgets.MDCalendarWidget import MDCalendar
from lib.drivers.islamic import driver
from datetime import datetime
import json


class main(MDApp):
    pressed = ObjectProperty()
    def __init__(self, **kwargs):
        self.title = "Calendar"
        self.current_month = datetime.now().strftime("%B")
        self.data = {"calendar": "Add Event", "reminder": "Add Reminder"}
        super().__init__(**kwargs)

    def build(self):
        return

    def on_save(self, instance):
        with open('./lib/data/config.json', 'r') as f:
            file = json.load(f)

        file['theme'] = str(self.theme_cls.primary_palette)

        with open('./lib/data/config.json', 'w') as f:
            json.dump(file, f)

    def on_start(self):
        year = int(datetime.now().strftime("%Y"))
        self.current_year = f'{year}/{year - 579}'

        self.create_dialogs()

        self.cal = MDCalendar()
        self.root.ids.home.ids.main.add_widget(self.cal)

        with open('./lib/data/config.json', 'r') as f:
            file = json.load(f)

        file['location'] = str(driver().getCity()['cityName'])

        with open('./lib/data/config.json', 'w') as f:
            json.dump(file, f)

        self.theme_cls.primary_palette = self.getSettings()["theme"]

    def getSettings(self):
        with open("./lib/data/config.json", "r") as file:
            config = json.load(file)
            return config

    def create_dialogs(self):
        recycle = CustomRecycle()
        recycle.size_hint_y = None
        recycle.height = 800

        for i in range(1990, 2071):
            islamic = i - 579
            item = {
                "viewclass": "YearItem",
                "text": f"{str(i)}/{str(islamic)}",
            }
            recycle.data.append(item)

        self.yearcontent = YearContent(size_hint_y=None, height=800).create()

        self.viewdialog = MDDialog(
            title="Change Calendar View:",
            type="confirmation",
            items=[
                ItemConfirm(text="Default"),
            ])

        self.theme_dialog = MDThemePicker(on_dismiss=self.on_save)

        self.license = License(size_hint_y=None, height=800)
        self.moreinfo = MoreInfo(size_hint_y=None, height=800)

        self.licensedialog = MDDialog(
            title="License:",
            type="custom",
            content_cls=self.license
        )

        self.infodialog = MDDialog(
            title="More Info:",
            type="custom",
            content_cls=self.moreinfo
        )

        self.yeardialog = MDDialog(
            title=f"Choose Year:",
            type="custom",
            content_cls=recycle
        )

        self.yeardialog.size_hint_x = .9
        self.licensedialog.size_hint_x = .9
        self.infodialog.size_hint_x = .9

    def callback(self, instance):
        self.root.ids.sm.transition.direction = 'left'
        self.root.ids.sm.current = 'chooser'

class E(ExceptionHandler):
    def handle_exception(self, inst):
        Logger.exception('Exception caught by ExceptionHandler')
        return ExceptionManager.PASS

ExceptionManager.add_handler(E())

if __name__ == '__main__':
    main().run()
