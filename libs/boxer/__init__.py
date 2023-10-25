
# script: python

HUG, FILL, FIXED = 'HUG', 'FILL', 'FIXED'
HORIZONTAL, VERTICAL = 'H', 'V'


def get_values_by_indexes(index_list, value_list):
    return [value_list[index] for index in index_list]


def attr_getter(d, key):
    def inner(key):
        return d[key]


class Box(object):
    def __init__(
        self,
        name=None,
        width=None,
        height=None,
        size_method=(HUG, HUG),
        padding=[0, 0, 0, 0],
        margin=[0, 0, 0, 0],
        border=[0, 0, 0, 0],
        parent=None,
        direction=HORIZONTAL
    ):
        self.name = name
        self.width = width
        self.height = height
        self.size_method = size_method
        self.padding = padding
        self.margin = margin
        self.border = border
        self.parent = parent
        self.direction = direction
        self.children = {}

    def __getattr__(self, name):
        if name in self.children:
            return self.children[name]
        return object.__getattribute__(self, name)

    def add_child(self, name, *args, **kwargs):
        self.children[name] = Box(*args, **kwargs, parent=self)
        return self.children[name]

    def add_sibling(self, name, *args, **kwargs):
        self.parent.children[name] = Box(name, *args, **kwargs,
                                         parent=self.parent)
        return self.parent.children[name]

    @property
    def siblings(self):
        return filter(
            lambda box: box != self,
            self.parent.children.values()
        )

    @property
    def previous_siblings_list(self):
        result = []
        for sibling in self.parent.children.values():
            if sibling == self:
                break
            result.append(sibling)
        return result

    def get_size_method(self, axis):
        assert axis in (HORIZONTAL, VERTICAL)
        method_index = {HORIZONTAL: 0, VERTICAL: 1}[axis]
        return self.size_method[method_index]

    def _get_axis_width(self, axis, values):
        assert axis in (HORIZONTAL, VERTICAL)
        indexes = [1, 3] if axis == HORIZONTAL else [0, 2]
        return sum(get_values_by_indexes(indexes, values))

    def get_padding(self, axis):
        return self._get_axis_width(axis, self.padding)

    def get_border(self, axis):
        return self._get_axis_width(axis, self.border)

    def get_margin(self, axis):
        return self._get_axis_width(axis, self.margin)

    def get_client_size(self, axis):
        return self.get_content_size(axis) + self.get_padding(axis)

    def get_offset_size(self, axis):
        return self.get_client_size(axis) + self.get_border(axis)

    def get_full_size(self, axis):
        return self.get_offset_size(axis) + self.get_margin(axis)

    def get_available_space(self, axis):
        parent_size = self.parent.get_content_size(axis)
        non_fill_siblings = filter(
            lambda b: b.get_size_method(axis) != FILL, self.siblings
        )
        size_of_siblings = sum(map(
            lambda b: b.get_full_size(axis), non_fill_siblings
        ))
        space_around = self.get_margin(axis) + \
            self.get_border(axis) + self.get_padding(axis)
        return parent_size - size_of_siblings - space_around

    def get_content_size(self, axis):
        size_method = self.get_size_method(axis)
        fixed_size_attr = {HORIZONTAL: 'width', VERTICAL: 'height'}[axis]
        if size_method == FIXED:
            size = getattr(self, fixed_size_attr)
            padding = self.get_padding(axis)
            return size - padding
        elif size_method == HUG:
            full_size_attr = 'full_' + fixed_size_attr
            return sum([
                getattr(b, full_size_attr) for b in self.children.values()
            ])
        elif size_method == FILL:
            if not self.parent:
                raise AssertionError('Can not use FILL if there\'s no parent')
            available_space = self.get_available_space(axis)
            num_of_shareholders = 1
            if self.direction == axis:
                num_of_shareholders = len(list(filter(
                    lambda box: box.get_size_method(axis) == FILL,
                    self.siblings
                ))) + 1
            return int(available_space / num_of_shareholders)
        elif size_method == HUG:
            pass

    def get_start_pos(self, axis):
        if not self.parent:
            return 0
        index = 3 if axis == HORIZONTAL else 1
        offset = 0
        if axis == self.parent.direction:
            offset = sum([sibling.get_full_size(axis)
                          for sibling in self.previous_siblings_list])
        return self.parent.get_start_pos(axis) + self.parent.padding[index] + \
            offset

    @property
    def content_width(self):  # Width for the inner content.
        return self.get_content_size(HORIZONTAL)

    @property
    def content_height(self):  # Height for the inner content.
        return self.get_content_size(VERTICAL)

    @property
    def client_width(self):  # Width with padding.
        return self.get_client_size(HORIZONTAL)

    @property
    def client_height(self):  # Height with padding.
        return self.get_client_size(VERTICAL)

    @property
    def offset_width(self):
        return self.get_offset_size(HORIZONTAL)

    @property
    def offset_height(self):
        return self.get_offset_size(VERTICAL)

    @property
    def full_width(self):
        return self.get_full_size(HORIZONTAL)

    @property
    def full_height(self):
        return self.get_full_size(VERTICAL)

    @property
    def content_box(self):
        return (self.get_start_pos(HORIZONTAL) + self.padding[3],
                self.get_start_pos(VERTICAL) + self.padding[0],
                self.content_width, self.content_height)

    @property
    def full_box(self):
        return (self.get_start_pos(HORIZONTAL), self.get_start_pos(VERTICAL),
                self.full_width, self.full_height)
