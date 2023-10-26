import pyxel
from libs.boxer import Box, FIXED, FILL, VERTICAL, HORIZONTAL

screen = Box(
    name='screen',
    width=320,
    height=240,
    padding=[10, 10, 10, 10]
)

screen\
    .add_child(
        'left_panel',
        width=100,
        height=FILL,
        padding=[10, 10, 10, 10]
    ).add_sibling(
        'right_panel',
        width=FILL,
        height=FILL,
        padding=[10, 10, 10, 10],
        direction=VERTICAL
    )

for name in ['x', 'y', 'z', 't'][:4]:
    screen.right_panel.add_child(name, FILL, FILL, margin=[10, 10, 10, 10])


def render_box(box, color):
    if box.name == 'y':
        # import ipdb; ipdb.set_trace()
        pass

    x, y, w, h = box.get_bounding_box(inner_level=0)
    pyxel.rectb(x, y, w, h, 15)
    pyxel.text(x+2, y+2, box.name, 15-color)
    x, y, w, h = box.get_bounding_box(inner_level=3)
    pyxel.rect(x, y, w, h, color)
    for child in box.children.values():
        render_box(child, color + 1)


class App:
    def __init__(self):
        pyxel.init(320, 240)
        pyxel.run(self.update, self.draw)

    def update(self):
        pass

    def draw(self):
        pyxel.cls(0)

        render_box(screen, 3)


App()
