import pyxel
from libs.boxer import Box, FILL, VERTICAL, HORIZONTAL
from src.decorators import fg_renderer, bg_renderer


class Indicator(Box):
    def __init__(self, name, title, value):
        self.title = title
        self.value = value
        self.current_value = 0
        super().__init__(name, FILL, FILL, margin=(0, 5))


screen = \
    Box(
        'screen', 320, 240, direction=VERTICAL,
    ).add_child(
        'header', FILL, 30, direction=HORIZONTAL, padding=5,
    ).add_sibling(
        'body', FILL, FILL, direction=HORIZONTAL, padding=(5, 10)
    ).add_sibling(
        'footer', FILL, 16, direction=HORIZONTAL
    ).get_root()

screen.header.add_child_obj(
    Indicator('health', 'HEALTH', 30),
    Indicator('food', 'FOOD', 22),
    Indicator('army', 'ARMY', 85),
    Indicator('religion', 'RELIGION', 100)
)

screen.body.add_child(
    'deck', FILL, FILL, margin=[0, 10, 0, 0],
).add_sibling(
    'story', 100, FILL
)


@bg_renderer(screen)
def render_screen_bg(box, x, y, w, h):
    pyxel.rect(x, y, w, h, 1)


@fg_renderer(screen)
def render_screen_fg(box, x, y, w, h):
    pyxel.rect(x, y, w, h, 2)


@fg_renderer(screen.header.children)
def render_indicator(self, x, y, w, h):
    if self.current_value < self.value:
        self.current_value += \
            (self.value - self.current_value) / 8
    elif self.current_value > self.value:
        self.current_value -= \
            (self.current_value - self.value) / 8
    pyxel.text(x, y - 1, self.title, 0)
    pyxel.text(x, y, self.title, 12)
    pyxel.rectb(x, y + 8, w, h - 8, 3)
    pyxel.rect(x+1, y + 9, w - 2, h - 10, 0)
    pyxel.rect(x+1, y + 9, (w / 100 * self.current_value) - 2, h - 10, 3)


@bg_renderer(screen.body)
def render_body_bg(box, x, y, w, h):
    pyxel.rect(x, y, w, h, 4)


@fg_renderer([screen.body.deck, screen.body.story])
def render_body_items(box, x, y, w, h):
    pyxel.rect(x, y, w, h, 9)


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
