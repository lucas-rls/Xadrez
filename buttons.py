import arcade

import arcade.gui
from arcade.gui import UIManager


class MyFlatButton(arcade.gui.UIFlatButton):
    def __init__(self, actual_view, next_view, **kwargs):
        super().__init__(**kwargs)
        self.actual_view = actual_view
        self.next_view = next_view

    def on_click(self):
        self.actual_view.window.show_view(self.next_view)
        self.actual_view.ui_manager.purge_ui_elements()
