
HORIZONTAL, VERTICAL = 'H', 'V'
FIXED, HUG, FILL = 'F', 'H', 'F'

screen = Box.from_dict({
    'direction': VERTICAL,
    'sizing': (FILL, FILL),
    'bg_color': 3,
    'children': {
        'header': {
            'sizing': (FILL, HUG),
            'children': {
                'health_indicator': {
                    'sizing': (FIXED, HUG),
                    'width': 60
                },
                'food_indicator': {
                    'sizing': (FIXED, HUG),
                    'width': 60
                },
                'religion_indicator': {
                    'sizing': (FIXED, HUG),
                    'width': 60
                },
                'army_indicator': {
                    'sizing': (FIXED, HUG),
                    'width': 60
                }
            }
        },
        'body': {
            'padding_left': 10,
            'padding_right': 10,
            'direction': HORIZONTAL,
            'sizing': (FILL, FILL),
            'children': {
                'left': {
                    'sizing': (FILL, FILL),
                    'padding_right': 5,
                    'border_right_color': 2,
                    'children': {
                        'card': {
                            'sizing': (FILL, FILL),
                            'gap': 5,
                            'children': {
                                'image': {
                                    'sizing': (FILL, FILL),
                                    'ratio': 1/1,
                                },
                                'text': {
                                    'sizing': (FILL, FILL)
                                }
                            }
                        },
                        'buttons': {
                            'gap': 10,
                            'children': {
                                'left': {},
                                'right': {}
                            }
                        }
                    }
                },
                'right': {
                    'sizing': (FIXED, FILL),
                    'padding_left': 5,
                    'width': 80,
                }
            }
        },
        'footer': {
            'sizing': (FILL, FILL)
        }
    }
})

