from kivy.properties import StringProperty, ListProperty
from kivy.uix.screenmanager import ScreenManager
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.theming import ThemableBehavior
from kivymd.uix.list import OneLineIconListItem, MDList, IRightBodyTouch, OneLineAvatarIconListItem, OneLineRightIconListItem
from kivymd.uix.selectioncontrol import MDSwitch
from kivymd.uix.screen import MDScreen

class MyAppBar(MDScreen):
    pass

class MyScreenManager(ScreenManager):
    pass

class Settings_(MDScreen):
    pass

class Home(MDScreen):
    pass

class About(MDScreen):
    pass

class ItemConfirm(OneLineAvatarIconListItem):
    divider = None
    def set_icon(self, instance_check):
        instance_check.active = True
        check_list = instance_check.get_widgets(instance_check.group)

        for check in check_list:
            if check != instance_check:
                check.active = False

class ContentNavigationDrawer(MDBoxLayout):
    pass

class ItemDrawer(OneLineIconListItem):
    icon = StringProperty()
    text_color = ListProperty((0, 0, 0, 1))


class DrawerList(ThemableBehavior, MDList):
    def set_color_item(self, instance_item):
        """Called when tap on a menu item."""

        # Set the color of the icon and text for the menu item.
        for item in self.children:
            if item.text_color == self.theme_cls.primary_color:
                item.text_color = self.theme_cls.text_color
                break
        instance_item.text_color = self.theme_cls.primary_color

class RightContainer(IRightBodyTouch, MDBoxLayout):
    pass

class RightSwitch(IRightBodyTouch, MDSwitch):
    pass


class ListItemWithSwitch(OneLineRightIconListItem):
    pass

class ListItem(OneLineIconListItem):
    icon = StringProperty()
    text = StringProperty()
    text_color = ListProperty((0, 0, 0, 1))