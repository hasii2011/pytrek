
import arcade
import arcade.gui

from pytrek.guiv2.BaseSection import BaseSection


class Popup(BaseSection):

    def __init__(self, left, bottom, width, height):
        super().__init__(left, bottom, width, height)
        self.manager = arcade.gui.UIManager()
        self.manager.enable()
        box = arcade.gui.UIBoxLayout()
        button = arcade.gui.UITextureButton(x=0, y=0,
                                            texture=arcade.load_texture('tests/button.png'),
                                            texture_pressed=arcade.load_texture('tests/button_pressed.png'),
                                            )
        box.add(button)
        button.on_click = self.on_click_button
        anchored_box = arcade.gui.UIAnchorWidget(anchor_x='center_x', anchor_y='center_y', child=box)
        self.manager.add(anchored_box)
        self.clicked = False

    # noinspection PyUnusedLocal
    def on_click_button(self, event):
        self.clicked = True

    def on_draw(self):
        self.manager.draw()
        super().on_draw()
        if self.clicked:
            arcade.draw_text(text='Clicked!', start_x=window.width/2, start_y=window.height-40, color=arcade.color.RED, anchor_x='center', font_size=20)


class GameView(arcade.View):
    def __init__(self):
        super().__init__()
        self.popup = Popup(0, 0, 400, 300)
        self.section_manager.add_section(self.popup)

    def on_draw(self):
        arcade.start_render()


window = arcade.Window()
game_view = GameView()
window.show_view(game_view)
window.run()
