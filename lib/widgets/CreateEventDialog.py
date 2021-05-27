from kivy.core.window import Window
from kivy.uix.widget import WidgetException
from kivymd.app import MDApp
from kivy.lang import Builder
from kivymd.uix.screen import MDScreen
from kivymd.uix.picker import MDDatePicker, MDTimePicker
from kivymd.uix.dialog import MDDialog
from kivy.uix.recycleview import RecycleView
from kivymd.uix.list import OneLineRightIconListItem, IRightBodyTouch, OneLineListItem
from kivymd.uix.selectioncontrol import MDCheckbox
from kivymd.uix.snackbar import BaseSnackbar
from kivy.properties import BooleanProperty, StringProperty, NumericProperty
from kivymd.uix.label import MDLabel
from kivy.uix.screenmanager import ScreenManager
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.toast import toast
import datetime
import json

Builder.load_string("""
#:import Window kivy.core.window.Window

<CustomRecycle>:
    key_viewclass: 'viewclass'
    key_size: "height"


    RecycleBoxLayout:
        padding: "10dp"
        default_size: None, dp(48)
        default_size_hint: 1, None
        size_hint_y: None
        height: self.minimum_height
        orientation: "vertical"


<ItemWithCheckBox>:
    on_active:
        root.children[0].active = False
        
    ItemRightCheckBox:
        on_release:
            root.active = self.active
        
        
<EventChooser>:        
    MDBoxLayout:
        orientation: "vertical"
        Widget:
            size_hint_y: .2
            
        MDTextField:
            id: text_field
            hint_text: "Name"
            size_hint_x: .9
            size_hint_y: .15
            pos_hint: {"center_x": .5}

        OneLineListItem:
            text: "Choose Date"
            on_release: root.date.open()

        OneLineListItem:
            text: "Choose Time"
            on_release: root.time.open()


        ItemWithCheckBox:
            id: ad
            text: "All Day"
            padding_x: 50

        OneLineListItem:
            text: "Repeat"
            padding_x: 50
            on_release:
                root.dialog.open()
                

        MDBoxLayout:
            orientation: 'horizontal'
            Widget
            MDFlatButton:
                text: "Discard"
                on_release: 
                    root.parent.transition.direction = 'left'
                    root.parent.current = 'home'
                    root.clear()
                    root.parent.transition.direction = 'right'

            MDFlatButton:
                text: "Save"
                on_release:                        
                    root.save_event(root.ids.text_field.text, root.ttime, root.ddate)
                    
                


<DaysLabel>:
    adaptive_size: True
    on_touch_down:
        if self.collide_point(*args[1].pos): \
        self.selected = False if self.selected else True

    on_selected:
        root.parent.parent.parent.parent.parent.parent.set_list(self.day)

    canvas.before:
        Color:
            rgba: app.theme_cls.primary_color if self.selected else (0, 0, 0, 0)

        Ellipse:
            size: dp(40), dp(40)
            pos: self.center_x - dp(20), self.center_y - dp(20)

<CustomRepeat>:
    MDBoxLayout:
        id: box
        orientation: 'vertical'
        size_hint_x: 1
        MDTextField:
            id: text_field
            hint_text: "Repeat Every"
            mode: "rectangle"
            pos_hint: {"center_x": .5}
            input_filter: "int"
            size_hint_x: .8

        Widget

        MDGridLayout:
            cols: 4
            rows: 1
            spacing: dp(10)
            pos_hint: {"center_x": .5}
            size_hint_x: .9

            MDRectangleFlatButton:
                size_hint: .2, 1
                text: "Day"
                on_release: root.parent.parent.on_all_press(self.text)

            MDRectangleFlatButton:
                size_hint: .2, 1
                text: "Week"
                on_release: root.parent.parent.on_all_press(self.text)


            MDRectangleFlatButton:
                size_hint: .2, 1
                text: "Month"
                on_release: root.parent.parent.on_all_press(self.text)


            MDRectangleFlatButton:
                size_hint: .2, 1
                text: "Year"
                on_release: root.parent.parent.on_all_press(self.text)

        Widget

        MDFloatLayout:
            id: float
            size_hint_x: 1

        Widget:
            size_hint_y: 5

        MDFloatLayout:
            size_hint_x: 1
            MDRectangleFlatButton:
                text: "Choose End Date"
                size_hint_x: .9
                pos_hint: {"center_y": .5, "center_x": .5}
                on_release: root.parent.parent.date.open()

        Widget

        ItemWithCheckBox:
            id: fr
            text: "Forever"

        Widget:
            size_hint_y: 10

        MDBoxLayout:    
            orientation: 'horizontal'
            Widget

            MDFlatButton:
                text: 'Cancel'
                on_release: 
                    root.parent.transition.direction = 'right'
                    root.parent.current = "repeat"

            MDFlatButton:
                text: 'OK'
                on_release:
                    root.parent.parent.on_save(root.ids.text_field.text)

<RepeatItem>:
    on_release:
        main = root.parent.parent.parent.parent.parent
        dialog = main.parent.parent.parent
        main.repeat(self.text)
        if self.text != 'Custom': dialog.dismiss()

<SelectGrid>:
    cols: 4 
    spacing: dp(40)
    pos_hint: {"center_x": .6 if Window.width < 550 else .5, "center_y": .1}
    size_hint_x: 1 if Window.width < 550 else .5        
    
<CustomSnackbar>

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
""")

class CustomSnackbar(BaseSnackbar):
    text = StringProperty(None)
    icon = StringProperty(None)
    font_size = NumericProperty("15sp")

class DaysLabel(MDLabel):
    selected = BooleanProperty(False)
    day = StringProperty()


class CustomRecycle(RecycleView):
    pass


class ItemRightCheckBox(IRightBodyTouch, MDCheckbox):
    pass


class ItemWithCheckBox(OneLineRightIconListItem):
    active = BooleanProperty(False)


class EventChooser(MDScreen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.name = 'chooser'
        self.repeat = RepeatDialog(size_hint_y=None, height=800)

        self.dialog = MDDialog(
            title="Repeat",
            type="custom",
            content_cls=self.repeat
        )

        self.date = MDDatePicker()
        self.date.bind(on_save=self.on_date_save)
        self.time = MDTimePicker()
        self.time.bind(on_save=self.on_time_save)

        self.ttime, self.ddate = None, None

        self.dialog.size_hint_x = .9

    def on_date_save(self, instance, value, date_range):
        iso = datetime.date(datetime.datetime.now().year, datetime.datetime.now().month, datetime.datetime.now().day)
        if not str(value) > str(iso) or not str(value) < "2071-01-01":
            toast('Invalid Date! Must be in the future!')

        if str(value) > str(iso) and str(value) < "2071-01-01":
            self.ddate = str(value)

    def on_time_save(self, instance, time):
        self.ttime = str(time)

    def save_event(self, name, time, date):
        if not name:
            toast("Please Enter Event Name!")

        elif not time and not self.ids.ad.active:
            toast("Please Choose a time for the Event")

        elif not date:
            toast("Please Choose a date for the Event")

        else:
            repeat = self.repeat.get_repeat()

            with open('./lib/data/events.json', 'r') as f:
                file = json.load(f)

            file['events'][date] = {"name": name, "time": time, "repeat": repeat}

            if self.ids.ad.active:
                file['events'][date] = {"name": name, "repeat": repeat}

            with open('./lib/data/events.json', 'w') as f:
                json.dump(file, f)

            self.parent.transition.direction = 'right'
            self.parent.current = "home"

            self.clear()
            self.snackbar(name, date)
            self.parent.transition.direction = 'left'

    def clear(self):
        self.ttime, self.ddate = None, None
        self.ids.text_field.text = ''
        self.ids.ad.active = False

        self.repeat.custom = False
        self.repeat.repeat_type = None
        self.repeat.customdict = {}
        self.repeat.days = []
        self.repeat.custom_end = ''
        self.repeat.customrepeat.ids.fr.active = False

    def snackbar(self, text, date):
        snackbar = CustomSnackbar(
            text=f"Successfully Created {text}! Date: {date}",
            icon="information",
            snackbar_x="10dp",
            snackbar_y="10dp",
        )
        snackbar.size_hint_x = (
        Window.width - (snackbar.snackbar_x * 2)
        ) / Window.width

        snackbar.open()






class RepeatItem(OneLineListItem):
    pass


class CustomRepeat(MDScreen):
    pass


class SelectGrid(MDGridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        for day in days:
            self.add_widget(DaysLabel(text=day[0], day=day))


class RepeatDialog(MDScreen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.rv = CustomRecycle()
        self.sm = ScreenManager()

        self.custom = False
        self.repeat_type = None

        self.date = MDDatePicker()
        self.date.bind(on_save=self.on_date_save)

        self.customrepeat = CustomRepeat(name='custom')
        self.repeatscreen = MDScreen(name='repeat')
        self.selectgrid = SelectGrid()

        self.repeatscreen.add_widget(self.rv)

        self.sm.add_widget(self.repeatscreen)
        self.sm.add_widget(self.customrepeat)

        self.items = ["Doesn't Repeat", 'Repeat Every Day', 'Repeat Every Week', 'Repeat Every Month',
                      'Repeat Every Year', 'Custom']

        for item in self.items:
            rv_item = {"viewclass": 'RepeatItem', 'text': item}
            self.rv.data.append(rv_item)

        self.customrepeat.ids.fr.active = False

        self.add_widget(self.sm)

    def repeat(self, name):
        if name == 'Custom':
            self.sm.transition.direction = 'left'
            self.sm.current = 'custom'
            self.customrepeat_type = None
            self.custom_end = None
            self.custom = True

        elif name == "Doesn't Repeat":
            pass

        else:
            self.repeat_type = name.split()[2]
            self.repeat_dict = {"type": self.repeat_type}

    def get_repeat(self):
        if not self.custom:
            return self.repeat_type

        if self.custom:
            return self.customdict

    def on_all_press(self, text):
        self.customrepeat_type = text
        if text == 'Week':
            try:
                self.customrepeat.ids.float.add_widget(self.selectgrid)
                self.days = []

            except WidgetException:
                pass

        else:
            self.customrepeat.ids.float.remove_widget(self.selectgrid)

    def set_list(self, day):
        if day in self.days:
            self.days.remove(day)

        else:
            self.days.append(day)

    def on_save(self, text):
        if text == "":
            toast('Text Missing!')

        elif not self.customrepeat_type:
            toast('Type Missing!')

        elif self.customrepeat_type == 'Week' and not self.days:
            self.days = None

        elif not self.custom_end and not self.customrepeat.ids.fr.active:
            toast('End Date Missing!')


        else:
            self.customdict = {'num': text, 'every': self.customrepeat_type}

            if self.customrepeat_type == 'Week':
                self.customdict['days'] = self.days

            self.customdict['end'] = self.custom_end

            self.parent.parent.parent.dismiss()

    def on_date_save(self, instance, value, date_range):
        iso = datetime.date(datetime.datetime.now().year, datetime.datetime.now().month, datetime.datetime.now().day)
        if not str(value) > str(iso) or not str(value) < "2071-01-01":
            toast('Invalid Date! Must be in the future!')

        if str(value) > str(iso) and str(value) < "2071-01-01":
            self.custom_end = str(value)


class test(MDApp):
    def build(self):
        chooser = EventChooser()
        return chooser


if __name__ == '__main__':
    test().run()