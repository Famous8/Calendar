from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivy.uix.screenmanager import Screen, ScreenManager
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.label import MDLabel
from kivy.properties import ObjectProperty, BooleanProperty
from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from lib.widgets.YearDialog import YearContent
from lib.drivers.getdatelist import getDict, getDayNum, getMonthDays, isLeap
from datetime import datetime
from lib.widgets.EventDialog import EventContent
from kivymd.uix.dropdownitem import MDDropDownItem
from kivymd.uix.dialog import MDDialog
import calendar

KV = """
<SelectableLabel>:
    adaptive_size: True
    size_hint_x: 1/7
    size_hint_y: 1/5
    halign: 'center'
        
    on_touch_down:
        if self.collide_point(*args[1].pos): \
        self.selected = False if self.selected else True

    on_selected:
        app.pressed = self
        root.switch_dates()

    canvas.before:
        Color:
            rgba: app.theme_cls.primary_color if self.selected and app.pressed == self else (0, 0, 0, 0)
            
        Ellipse:
            size: dp(35), dp(35)
            pos: self.center_x - dp(18), self.center_y - dp(18)

<DayLabel>:
    adaptive_size: True
    size_hint_x: 1
    size_hint_y: .2
    halign: 'center'
    theme_text_color: "Custom"
    text_color: app.theme_cls.primary_color

<Spacer>:
    adaptive_size: True
    size_hint_x: 1
    size_hint_y: .2

<TopBar>:
    size_hint_y: .1
    MDIconButton:
        icon: "arrow-left"
        pos_hint: {"center_y": .5}
        on_release: 
            app.cal.sm.transition.direction = 'right'
            app.cal.sm.current = app.cal.sm.previous()
            root.ids.topLabel.text = app.cal.sm.current

    MDLabel:
        id: topLabel
        text: app.current_month
        halign: 'center'
        pos_hint: {"center_y": .5}

    MDIconButton:
        icon: "arrow-right"
        pos_hint: {"center_y": .5}
        on_release: 
            app.cal.sm.transition.direction = 'left'
            app.cal.sm.current = app.cal.sm.next()
            root.ids.topLabel.text = app.cal.sm.current

<YearChooser>:
    text: app.current_year
    pos_hint: {"center_x": .5}
    on_release: 
        #app.dialogsm.current = "Year"
        app.yeardialog.open()



"""


class TopBar(BoxLayout):
    pass


class YearChooser(MDDropDownItem):
    pass


class SelectableLabel(MDLabel):
    selected = BooleanProperty(False)
    pressed = ObjectProperty()
    def switch_dates(self):
        try:
            cal = self.parent.parent.parent.parent.parent.parent
            self.year = int(cal.yearchooser.text.split('/')[0])
            self.month = cal.months[self.parent.parent.name]

            cal.events.switch_dates(self.year, self.month, int(self.text))

        except AttributeError as e:
            pass

class DayLabel(MDLabel):
    pass


class Spacer(Widget):
    pass


class MDCalendar(MDScreen):
    def build(self):
        Builder.load_string(KV)

    def getDay(self, year, month, day):
        for date in getDict():
            list = date.split(',')
            if year in list[2] and month in list[1] and day in list[1]:
                return list[0]

    def __init__(self, **kw):
        super().__init__(**kw)
        self.build()
        self.sm = ScreenManager()

        self.boxlayout = BoxLayout(orientation='vertical')

        self.main_screen = MDScreen()
        self.main_screen.size_hint = 1, .4

        year = int(datetime.now().strftime("%Y"))

        self.current_year = f'{year}/{year - 579}'
        self.yearchooser = YearChooser()
        self.yearchooser.size_hint_y = 0.1

        self.widget = Widget()
        self.widget.size_hint_y = 0.02

        self.topBar = TopBar()
        self.topBar.size_hint_y = 0.1

        current_month = datetime.now().strftime("%B")

        self.months = {'January': 1, 'February': 2, 'March': 3, 'April': 4,
                       'May': 5, 'June': 6, 'July': 7, 'August': 8, 'September': 9,
                       'October': 10, 'November': 11, 'December': 12}

        day = datetime.now().strftime("%d")
        days = ['M', 'T', 'W', 'T', 'F', 'S', 'S']

        self.events = EventContent().create(int(year), self.months[current_month], int(day))
        self.events.size_hint = 1, .6

        for month in self.months:
            screen = Screen(name=month)

            grid = MDGridLayout(cols=7)
            grid.id = month

            spacer_grid = MDGridLayout(cols=7)
            spacer_grid.size_hint_y = .2
            spacer_grid.size_hint_x = 1

            screen.add_widget(grid)

            for day in days:
                grid.add_widget(DayLabel(text=day))

            daysinmonth = calendar.monthrange(year, self.months[month])[1] + 1

            for i in range(1, daysinmonth):
                if i == 1:
                    day = self.getDay("2021", month, str(i))
                    daynum = getattr(calendar, day.upper())

                    for n in range(daynum):
                        grid.add_widget(Spacer())

                label = SelectableLabel(text=str(i))
                if month == current_month and label.text == str(datetime.now().strftime('%#d')):
                    label.selected = True

                grid.add_widget(label)

            self.sm.add_widget(screen)

        self.main_screen.add_widget(self.sm)

        self.sm.current = str(current_month)

        self.boxlayout.add_widget(self.yearchooser)
        self.boxlayout.add_widget(self.topBar)
        self.boxlayout.add_widget(self.main_screen)
        self.boxlayout.add_widget(self.widget)
        self.boxlayout.add_widget(self.events)

        self.add_widget(self.boxlayout)

    def on_year_change(self, year):
        screens = self.sm.screens
        self.events.switch_year(year)

        for screen in screens[:]:
            spacers = []

            day = self.getDay(str(year), screen.name, str(1))
            monthnum = self.months[str(screen.name)]

            daysinmonth = getMonthDays(screen.name, int(year)) + 1
            grid = screen.children[0]

            for widget in grid.children:
                if "Spacer" in str(widget):
                    spacers.append(widget)

            spacers_amount = len(spacers)
            amount_needed = getattr(calendar, day.upper()) + 1
            label = SelectableLabel(text="29")

            if screen.name == "February" and isLeap(int(year)) is True:
                grid.add_widget(label)

            elif screen.name == "February" and isLeap(int(year)) is False:
                for widget in grid.children:
                    try:
                        if "29" in widget.text:
                            grid.remove_widget(widget)
                            break

                    except AttributeError:
                        pass

            if amount_needed > spacers_amount:
                add = amount_needed - spacers_amount - 1
                index = len(grid.children) - 7
                for x in range(add):
                    grid.add_widget(Spacer(), index)

            elif spacers_amount > amount_needed:
                remove = spacers_amount - amount_needed + 1
                for y in range(remove):
                    for widget in grid.children:
                        if "Spacer" in str(widget):
                            grid.remove_widget(widget)
                            break

            self.yearchooser.text = f"{year}/{int(year) - 579}"
            self.sm.current = "January"
            self.topBar.ids.topLabel.text = self.sm.current


class Test(MDApp):
    pressed = ObjectProperty()

    def build(self):
        year = int(datetime.now().strftime("%Y"))
        self.current_year = f'{year}/{year - 579}'

        self.content = YearContent(size_hint_y=None, height=300).create()

        self.months = {'January': 1, 'February': 2, 'March': 3, 'April': 4,
                       'May': 5, 'June': 6, 'July': 7, 'August': 8, 'September': 9,
                       'October': 10, 'November': 11, 'December': 12}

        self.yeardialog = MDDialog(
            type="custom",
            title="Choose Year",
            content_cls=self.content,
        )

        self.yeardialog.size_hint_x = .8

        self.current_month = datetime.now().strftime("%B")
        self.cal = MDCalendar()

        return self.cal


if __name__ == '__main__':
    Test().run()