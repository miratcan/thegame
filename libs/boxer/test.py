from . import Box, HUG, FILL, FIXED, HORIZONTAL, VERTICAL
from itertools import product


def test_size_method():
    box = Box()
    assert box._get_size_method(HORIZONTAL) == HUG
    assert box._get_size_method(VERTICAL) == HUG

    box = Box(width=100, height=HUG)
    assert box._get_size_method(HORIZONTAL) == FIXED
    assert box._get_size_method(VERTICAL) == HUG

    box = Box(width=FILL, height=HUG)
    assert box._get_size_method(HORIZONTAL) == FILL
    assert box._get_size_method(VERTICAL) == HUG


def test_get_width_methods():
    frame = [1, 2, 3, 4]
    frame_types = ['padding', 'border', 'margin']
    methods = ['_get_%s_width' % s for s in frame_types]
    for frame_type, method in zip(frame_types, methods):
        box = Box()
        assert getattr(box, method)(HORIZONTAL) == 0
        assert getattr(box, method)(VERTICAL) == 0
        setattr(box, frame_type, frame)
        assert getattr(box, method)(HORIZONTAL) == 6
        assert getattr(box, method)(VERTICAL) == 4


def test_get_fixed_size():
    margin = [1, 2, 3, 4]
    border = [5, 6, 7, 8]
    padding = [9, 10, 11, 12]
    box = Box(width=100, height=100, margin=margin, border=border,
              padding=padding)

    # Raw
    assert box._get_size(HORIZONTAL) == 100
    assert box._get_size(VERTICAL) == 100

    # Reduce margin
    assert box._get_size(HORIZONTAL, inner_level=1) == 94
    assert box._get_size(VERTICAL, inner_level=1) == 96

    # Reduce border
    assert box._get_size(HORIZONTAL, inner_level=2) == 80
    assert box._get_size(VERTICAL, inner_level=2) == 84

    # Reduce padding
    assert box._get_size(HORIZONTAL, inner_level=3) == 58
    assert box._get_size(VERTICAL, inner_level=3) == 64


def test_get_hugged_size():
    margin = [1, 2, 3, 4]
    border = [5, 6, 7, 8]
    padding = [9, 10, 11, 12]

    parent = Box(margin=[10, 10, 10, 10], padding=[10, 10, 10, 10],
                 border=[10, 10, 10, 10])
    parent.add_child('child', width=100, height=100, margin=margin,
                     border=border, padding=padding)

    # Raw
    assert parent._get_size(HORIZONTAL) == 160
    assert parent._get_size(VERTICAL) == 160

    # Reduce margin
    assert parent._get_size(HORIZONTAL, inner_level=1) == 140
    assert parent._get_size(VERTICAL, inner_level=1) == 140

    # Reduce border
    assert parent._get_size(HORIZONTAL, inner_level=2) == 120
    assert parent._get_size(VERTICAL, inner_level=2) == 120

    # Reduce padding
    assert parent._get_size(HORIZONTAL, inner_level=3) == 100
    assert parent._get_size(VERTICAL, inner_level=3) == 100


def test_hugged_size_nested():
    parent = Box(name='parent')
    parent\
        .add_child(
            name='left_panel',
        )\
        .add_child(
            name='left_panel_item_1', width=20, height=20
        )\
        .add_sibling(
            name='left_panel_item_2', width=20, height=20
        )
    parent\
        .add_child(
            name='right_panel', width=HUG, height=HUG
        )\
        .add_child(
            name='right_panel_item_1', width=20, height=20
        )\
        .add_sibling(
            name='right_panel_item_2', width=20, height=20
        )
    assert parent._get_size(HORIZONTAL) == 80


def test_get_fill_size():
    margin = [1, 2, 3, 4]
    border = [5, 6, 7, 8]
    padding = [9, 10, 11, 12]
    parent = Box(
        margin=[10, 10, 10, 10], padding=[10, 10, 10, 10],
        border=[10, 10, 10, 10], width=100, height=100
    )
    child = parent.add_child(
        'child', width=FILL, height=FILL, margin=margin,
        border=border, padding=padding
    )
    assert child._get_size(HORIZONTAL) == 40
    assert child._get_size(VERTICAL) == 40


def test_fill_content_width_with_shareholders():
    parent = Box(
        margin=[10, 10, 10, 10], padding=[10, 10, 10, 10],
        border=[10, 10, 10, 10], width=300, height=300
    )
    parent\
        .add_child(
            name='left_child',
            width=100, height=FILL,
            margin=[10, 10, 10, 10]
        ).add_sibling(
            name='right_child_1',
            width=FILL, height=FILL
        ).add_sibling(
            name='right_child_2',
            width=FILL, height=FILL
        )
    assert parent.right_child_1._get_size(HORIZONTAL) == 70
    assert parent.right_child_2._get_size(VERTICAL) == 240


def test_get_pos():
    parent = Box(
        name='parent', width=400, height=400, padding=[1, 2, 3, 4]
    )
    child = parent.add_child(
        name='child', width=100, height=FILL, margin=[10, 10, 10, 10],
        border=[10, 10, 10, 10], padding=[10, 10, 10, 10]
    )
    assert parent.x == 0
    assert parent.y == 0

    assert child._get_pos(HORIZONTAL, inner_level=0) == 4
    assert child._get_pos(HORIZONTAL, inner_level=1) == 14
    assert child._get_pos(HORIZONTAL, inner_level=2) == 24

    assert child._get_pos(VERTICAL, inner_level=0) == 1
    assert child._get_pos(VERTICAL, inner_level=1) == 11
    assert child._get_pos(VERTICAL, inner_level=2) == 21


def test_get_pos_nested():
    parent = Box(
        name='parent', width=400, height=400,
        padding=[1, 2, 3, 4]
    )
    child_1 = parent.add_child(
        name='child_1', width=100, height=100,
        margin=[10, 10, 10, 10], border=[10, 10, 10, 10],
        padding=[10, 10, 10, 10]
    )
    child_2 = parent.add_child(
        name='child_2', width=FILL, height=FILL,
        margin=[10, 10, 10, 10], border=[10, 10, 10, 10],
        padding=[10, 10, 10, 10]
    )

    assert child_1._get_pos(HORIZONTAL, inner_level=0) == 4
    assert child_1._get_pos(HORIZONTAL, inner_level=1) == 14
    assert child_1._get_pos(HORIZONTAL, inner_level=2) == 24
    assert child_1._get_pos(HORIZONTAL, inner_level=3) == 34
    assert child_2._get_pos(HORIZONTAL, inner_level=0) == 104
    assert child_2._get_pos(HORIZONTAL, inner_level=1) == 114
    assert child_2._get_pos(HORIZONTAL, inner_level=2) == 124
    assert child_2._get_pos(HORIZONTAL, inner_level=3) == 134

    assert child_1._get_pos(VERTICAL, inner_level=0) == 1
    assert child_1._get_pos(VERTICAL, inner_level=1) == 11
    assert child_1._get_pos(VERTICAL, inner_level=2) == 21
    assert child_1._get_pos(VERTICAL, inner_level=3) == 31
    assert child_2._get_pos(VERTICAL, inner_level=0) == 1
    assert child_2._get_pos(VERTICAL, inner_level=1) == 11
    assert child_2._get_pos(VERTICAL, inner_level=2) == 21
    assert child_2._get_pos(VERTICAL, inner_level=3) == 31


def test_get_box():
    box = Box(width=100, height=100, margin=[10, 10, 10, 10],
              border=[10, 10, 10, 10], padding=[10, 10, 10, 10])
    assert box.get_bounding_box(inner_level=0) == (0, 0, 100, 100)
    assert box.get_bounding_box(inner_level=1) == (10, 10, 80, 80)
    assert box.get_bounding_box(inner_level=2) == (20, 20, 60, 60)
    assert box.get_bounding_box(inner_level=3) == (30, 30, 40, 40)
