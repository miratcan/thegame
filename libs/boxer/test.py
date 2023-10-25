from . import Box, HUG, FILL, FIXED, HORIZONTAL, VERTICAL


def test_size_method():
    for h_sizing_method in (HUG, FILL, FIXED):
        for v_sizing_method in (HUG, FILL, FIXED):
            box = Box(
                size_method=(h_sizing_method, v_sizing_method),
                width=100,
                padding=[10, 10, 10, 10]
            )
            assert box.get_size_method(HORIZONTAL) == h_sizing_method
            assert box.get_size_method(VERTICAL) == v_sizing_method


def test_get_padding():
    box = Box()
    assert box.get_padding(HORIZONTAL) == 0
    assert box.get_padding(VERTICAL) == 0

    box = Box(padding=[1, 2, 3, 4])
    assert box.get_padding(HORIZONTAL) == 6
    assert box.get_padding(VERTICAL) == 4


def test_get_margin():
    box = Box()
    assert box.get_margin(HORIZONTAL) == 0
    assert box.get_margin(VERTICAL) == 0

    box = Box(margin=[1, 2, 3, 4])
    assert box.get_margin(HORIZONTAL) == 6
    assert box.get_margin(VERTICAL) == 4


def test_get_border():
    box = Box()
    assert box.get_border(HORIZONTAL) == 0
    assert box.get_border(VERTICAL) == 0

    box = Box(border=[1, 2, 3, 4])
    assert box.get_border(HORIZONTAL) == 6
    assert box.get_border(VERTICAL) == 4


def test_get_content_width():
    # Content must be narrowed by padding.
    box = Box(size_method=(FIXED, FIXED), width=20, height=20,
              padding=[1, 2, 3, 4])
    assert box.content_width == 14


def test_get_client_width():
    # Client width must not changed with padding.
    box = Box(size_method=(FIXED, FIXED), width=10, height=20,
              padding=[1, 2, 3, 4])
    assert box.client_width == 10


def test_get_offset_width():
    # Border size must be added to the width.
    box = Box(size_method=(FIXED, FIXED), width=10, height=20,
              padding=[1, 2, 3, 4], border=[1, 2, 3, 4])
    assert box.offset_width == 16


def test_get_full_width():
    # Border size must be added to the width.
    box = Box(size_method=(FIXED, FIXED), width=10, height=20,
              padding=[1, 2, 3, 4], border=[1, 2, 3, 4],
              margin=[10, 10, 10, 10])
    assert box.full_width == 36


def test_hug_content_width():
    """Width of the HUG sized element must be sum of width, border
    and margins of the children."""
    parent = Box(size_method=(HUG, HUG))
    parent.add_child(
        name='child_1',
        size_method=(FIXED, FIXED),
        width=10,
        height=10,
        padding=[1, 2, 3, 4],
        margin=[1, 2, 3, 4]
    )   # 16
    parent.add_child(
        name='child_2',
        size_method=(FIXED, FIXED),
        width=10,
        height=10,
        margin=[10, 10, 10, 10]
    )  # 30
    assert parent.content_width == 46  # 30 + 16


def test_hug_content_width_nested():
    """Same test with above, but 2 levels."""
    parent = Box(name='parent', size_method=(HUG, HUG))
    parent\
        .add_child(
            name='left_panel',
            size_method=(HUG, HUG)
        )\
        .add_child(
            name='left_panel_item_1',
            size_method=(FIXED, FIXED),
            width=20
        )\
        .add_sibling(
            name='left_panel_item_2',
            size_method=(FIXED, FIXED),
            width=20
        )
    parent\
        .add_child(
            name='right_panel',
            size_method=(HUG, HUG)
        )\
        .add_child(
            name='right_panel_item_1',
            size_method=(FIXED, FIXED),
            width=20
        )\
        .add_sibling(
            name='right_panel_item_2',
            size_method=(FIXED, FIXED),
            width=20)

    assert parent.content_width == 80


def test_fill_content_width():
    parent = Box(name='parent', size_method=(FIXED, FIXED),
                 width=400, height=400)
    parent\
        .add_child(
            name='left_child',
            size_method=(FIXED, FILL),
            width=100, margin=[10, 10, 10, 10]
        ).add_sibling(
            name='right_child',
            size_method=(FILL, FILL)
        )
    assert parent.right_child.content_width == 280


def test_fill_content_width_with_shareholders():
    parent = Box(name='parent', size_method=(FIXED, FIXED),
                 width=400, height=400)
    parent\
        .add_child(
            name='left_child',
            size_method=(FIXED, FILL),
            width=100,
            margin=[10, 10, 10, 10]
        ).add_sibling(
            name='right_child_1',
            size_method=(FILL, FILL)
        ).add_sibling(
            name='right_child_2',
            size_method=(FILL, FILL)
        )
    assert parent.right_child_1.content_width == 140
    assert parent.right_child_2.content_width == 140


def test_previous_siblings_list():
    parent = Box('parent')
    child_1 = parent.add_child('child_1')
    child_2 = parent.add_child('child_2')
    child_3 = parent.add_child('child_3')
    assert child_2.previous_siblings_list == [child_1]
    assert child_3.previous_siblings_list == [child_1, child_2]


def test_get_start_pos():
    parent = Box(name='parent', size_method=(FIXED, FIXED),
                 width=400, height=400, padding=[1, 2, 3, 4])
    parent.add_child(
        name='child',
        size_method=(FIXED, FILL),
        width=100, margin=[10, 10, 10, 10]
    )
    assert parent.get_start_pos(HORIZONTAL) == 0
    assert parent.get_start_pos(VERTICAL) == 0
    assert parent.child.get_start_pos(HORIZONTAL) == 4
    assert parent.child.get_start_pos(VERTICAL) == 2


def test_get_start_pos_nested():
    parent = Box(name='parent', size_method=(FIXED, FIXED),
                 width=400, height=400, padding=[1, 2, 3, 4])
    parent.add_child(
        name='child_1',
        size_method=(FIXED, FILL),
        width=100, margin=[10, 10, 10, 10]
    )
    parent.add_child(
        name='child_2',
        size_method=(FILL, FILL),
        margin=[10, 10, 10, 10]
    )
    assert parent.child_2.get_start_pos(HORIZONTAL) == 124
    assert parent.child_2.get_start_pos(VERTICAL) == 2


def test_full_box():
    parent = Box(name='parent', size_method=(FIXED, FIXED),
                 width=400, height=400, padding=[1, 2, 3, 4])
    parent.add_child(
        name='child',
        size_method=(FIXED, FILL),
        width=100, margin=[10, 10, 10, 10]
    )
    assert parent.full_box == (0, 0, 400, 400)
    assert parent.child.full_box == (4, 2, 120, 396)
