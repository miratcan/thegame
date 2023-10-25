import pyxel
from libs.boxer import Box, FIXED, FILL, VERTICAL

screen = Box(
    name='screen',
    width=320,
    height=240,
    size_method=(FIXED, FIXED),
    padding=[10, 10, 10, 10]
)

screen\
    .add_child(
        'left_panel',
        size_method=(FIXED, FILL),
        width=100,
        margin=[5, 5, 5, 5],
        padding=[5, 5, 5, 5]
    ).add_sibling(
        'right_panel',
        size_method=(FILL, FILL),
        margin=[5, 5, 5, 5]
    )


def render_box(box, color):
    pyxel.rect(*list(box.full_box) + [15-color,])
    pyxel.rect(*list(box.content_box) + [color,])
    pyxel.text(*list(box.content_box)[:2], box.name or 'Box', 15-color)


class App:
    def __init__(self):
        pyxel.init(320, 240)
        pyxel.run(self.update, self.draw)

    def update(self):
        pass

    def draw(self):
        pyxel.cls(0)

        render_box(screen, 1)
        render_box(screen.left_panel, 3)
        render_box(screen.right_panel, 5)

App()
