from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivymd.uix.screen import MDScreen
from kivymd.uix.list import OneLineListItem
from kivymd.app import MDApp
from kivy.uix.recycleview import RecycleView
from kivy.lang import Builder

kv = """
#:import Thread threading.Thread

<CustomRecycle>:
    id: crv
    key_viewclass: 'viewclass'
    key_size: "height"


    RecycleBoxLayout:
        id: rbl
        padding: "10dp"
        default_size: None, dp(48)
        default_size_hint: 1, None
        size_hint_y: None
        height: self.minimum_height
        orientation: "vertical"

<YearItem>:
    on_release:
        content = root.parent.parent.parent
        content.gyear = self.text.split('/')[0]

        thread = Thread(target=app.cal.on_year_change(content.gyear), args=(1,))
        thread.start()

        app.yeardialog.dismiss()

"""


class YearItem(OneLineListItem):
    pass


class YearContent(MDScreen):
    def build(self):
        self.name = "Year"
        self.year = None
        return Builder.load_string(kv)

    def create(self):
        self.build()

        recycle = CustomRecycle()
        recycle.size_hint_y = None
        recycle.height = 300

        for i in range(1990, 2071):
            islamic = i - 579
            item = {
                "viewclass": "YearItem",
                "text": f"{str(i)}/{str(islamic)}",
            }
            recycle.data.append(item)

        return recycle


class CustomRecycle(RecycleView):
    pass


class Example(MDApp):
    def build(self):
        self.content = YearContent(size_hint_y=None, height=400).create()
        self.dialog = MDDialog(
            title="Choose Year:",
            type="custom",
            content_cls=self.content
        )

        screen = MDScreen()
        button = MDFlatButton(text="Click Me", on_release=self.open_dialog)
        screen.add_widget(button)

        return screen

    def open_dialog(self, instance):
        self.dialog.open()


if __name__ == '__main__':
    Example().run()