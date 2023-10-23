HUG, FILL, FIXED = 'HUG', 'FILL', 'FIXED'
HORIZONTAL, VERTICAL = 'H', 'V'


def get_values_by_indexes(index_list, value_list):
    return [value_list[index] for index in index_list]


class Box:
    def __init__(
        self,
        width=None,
        height=None,
        size_method=(HUG, HUG),
        padding_width=[0, 0, 0, 0],
        margin_width=[0, 0, 0, 0],
        border_width=[0, 0, 0, 0],
    ):
        self.width = width
        self.height = height
        self.size_method = size_method
        self.padding_width = padding_width
        self.margin_width = margin_width
        self.border_width = border_width
        self.children = []

    def get_size_method(self, axis):
        """
        >>> box = Box(size_method=(FILL, FIXED))
        >>> box.get_size_method(HORIZONTAL)
        'FILL'
        >>> box.get_size_method(VERTICAL)
        'FIXED'
        """
        assert axis in (HORIZONTAL, VERTICAL)
        method_index = {HORIZONTAL: 0, VERTICAL: 1}[axis]
        return self.size_method[method_index]

    def _get_axis_width(self, axis, values):
        assert axis in (HORIZONTAL, VERTICAL)
        indexes = [1, 3] if axis == HORIZONTAL else [0, 2]
        return sum(get_values_by_indexes(indexes, values))

    def get_padding_width(self, axis):
        """
        >>> box = Box(padding_width=[1, 2, 3, 4])
        >>> box.get_padding_width(HORIZONTAL)
        6
        >>> box.get_padding_width(VERTICAL)
        4
        """
        return self._get_axis_width(axis, self.padding_width)

    def get_border_width(self, axis):
        """
        >>> box = Box(padding_width=[1, 2, 3, 4])
        >>> box.get_padding_width(HORIZONTAL)
        6
        >>> box.get_padding_width(VERTICAL)
        4
        """
        return self._get_axis_width(axis, self.border_width)

    def get_margin_width(self, axis):
        """
        >>> box = Box(padding_width=[1, 2, 3, 4])
        >>> box.get_padding_width(HORIZONTAL)
        6
        >>> box.get_padding_width(VERTICAL)
        4
        """
        return self._get_axis_width(axis, self.margin_width)

    @property
    def content_width(self):
        """
        >>> box = Box(size_method=(FIXED, FIXED), width=10, height=20)
        >>> box.content_width
        10
        >>> box.width = 20
        >>> box.content_width
        20

        >>> box1 = Box(size_method=(HUG, HUG))
        >>> box2 = Box(size_method=(FIXED, FIXED), width=10, height=10,
        ...     padding_width=[1, 2, 3, 4])
        >>> box3 = Box(size_method=(FIXED, FIXED), width=10, height=10)
        >>> box1.children = [box2, box3]
        >>> box1.content_width
        26
        """
        size_method = self.get_size_method(HORIZONTAL)
        if size_method == FIXED:
            return self.width or 0
        elif size_method == HUG:
            return sum(map(lambda b: b.full_width, self.children))

    @property
    def client_width(self):
        """
        >>> box = Box(size_method=(FIXED, FIXED), width=10, height=20,
        ... padding_width=[1, 2, 3, 4])
        >>> box.client_width
        16
        >>> box.width = 20
        >>> box.client_width
        26
        """
        return self.content_width + \
            self.get_padding_width(HORIZONTAL)

    @property
    def offset_width(self):
        """
        >>> box = Box(size_method=(FIXED, FIXED), width=10, height=20,
        ... padding_width=[1, 2, 3, 4], border_width=[1, 2, 3, 4])
        >>> box.offset_width
        22
        """
        return self.client_width + \
            self.get_border_width(HORIZONTAL)

    @property 
    def full_width(self):
        return self.offset_width + self.get_margin_width(HORIZONTAL)


if __name__ == '__main__':
    import doctest
    doctest.testmod()
