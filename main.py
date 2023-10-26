import pyxel
from libs.boxer import Box, FILL, VERTICAL, HORIZONTAL

screen = Box('screen', 320, 240, direction=VERTICAL)

screen\
    .add_child('header', FILL, 22, direction=HORIZONTAL, padding=[5, 0, 0, 0])\
    .add_sibling('body', FILL, FILL, direction=HORIZONTAL)\
    .add_sibling('footer', FILL, 16, direction=HORIZONTAL)


class Indicator(Box):
    def __init__(self, name, title, value):
        self.title = title
        self.value = value
        super().__init__(name, FILL, FILL, margin=[0, 5, 0, 5])

    def render(self, x, y, w, h):
        pyxel.text(x, y, self.title, 8)
        pyxel.rectb(x, y + 8, w, h - 8, 3)
        pyxel.rect(x+1, y + 9, (w / 100 * self.value) - 2, h - 10, 4)


screen.header.add_child_obj(
    Indicator('health', 'Health', 30),
    Indicator('food', 'Food', 22),
    Indicator('army', 'Army', 85),
    Indicator('religion', 'Religion', 100)
)


class App:
    def __init__(self):
        pyxel.init(320, 240)
        pyxel.run(self.update, self.draw)

    def update(self):
        pass

    def draw(self):
        pyxel.cls(0)
        screen._render()


App()
