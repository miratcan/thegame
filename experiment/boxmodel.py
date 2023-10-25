class Box:
    pass


HORIZONTAL, VERTICAL = 'H', 'V'
FIXED_SIZE, HUG, FILL = 'F', 'H', 'F'

screen = Box(
    direction=VERTICAL,
    sizing=FILL,
    slots=[
        Box(
            name='header',
            sizing=HUG,
            slots=[
                Box(
                    name='health_indicator',
                    sizing=FIXED_SIZE,
                    width=60
                ),
                Box(
                    name='food_indicator',
                    sizing=FIXED_SIZE,
                    width=60
                ),
                Box(
                    name='religion_indicator',
                    sizing=FIXED_SIZE,
                    width=60
                ),
                Box(
                    name='army_indicator',
                    sizing=FIXED_SIZE,
                    width=60
                ),

            ]
        ),
        Box(
            name='body',
            padding_left=10,
            padding_right=10,
            direction=HORIZONTAL,
            slots=[
                Box()

            ]
        ),
        Box('footer')
    ]
)


class HealthIndicator:
    def __init__(self):
        self.el = header_el.create_element()

    def render(self):
        return self.el.draw.rect(10, 10, 15, 15)
