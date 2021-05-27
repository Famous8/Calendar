from kivy.lang import Builder
from kivymd.app import MDApp

from kivymd.uix.screen import MDScreen
from kivymd.uix.dialog import MDDialog

Builder.load_string("""
#:import Window kivy.core.window.Window

<License>
    BoxLayout:
        orientation: "vertical"
        spacing: "10dp"
        padding: 0, 0, 0, "10dp"

        ScrollView:
            bar_width: 0

            MDGridLayout:
                cols: 1
                adaptive_height: True
                padding: "10dp"

                MDLabel:
                    id: text_label
                    markup: True
                    size_hint_y: None
                    height: self.texture_size[1]
                    font_size: "25px"

<MoreInfo>
    BoxLayout:
        orientation: "vertical"
        spacing: "10dp"
        padding: 0, 0, 0, "10dp"
        ScrollView:
            bar_width: 0

            MDGridLayout:
                cols: 1
                adaptive_height: True
                padding: "10dp"

                MDLabel:
                    id: text_label
                    markup: True
                    size_hint_y: None
                    height: self.texture_size[1]
                    font_size: "25px"
                                 
""")

KV = """
MDFlatButton:
    text: "Click Me"
    on_release: app.dialog.open()    
"""

class License(MDScreen):
    def __init__(self, **kw):
        super().__init__(**kw)
        with open("./LICENSE", encoding="utf-8") as license:
            self.ids.text_label.text = license.read()

class MoreInfo(MDScreen):
    def __init__(self, **kw):
        super().__init__(**kw)
        with open("./INFO", encoding="utf-8") as info:
            self.ids.text_label.text = info.read()

class test(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.dialog = MDDialog(
            title='License:',
            type='custom',
            content_cls=License(size_hint_y=None, height=300)
        )

    def build(self):
        return Builder.load_string(KV)

if __name__ == '__main__':
    test().run()