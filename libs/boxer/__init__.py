
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

    def _get_size_method(self, axis):
        assert axis in (HORIZONTAL, VERTICAL)
        method_index = {HORIZONTAL: 0, VERTICAL: 1}[axis]
        return self.size_method[method_index]

    def _get_axis_width(self, axis, values):
        assert axis in (HORIZONTAL, VERTICAL)
        indexes = [1, 3] if axis == HORIZONTAL else [0, 2]
        return sum(get_values_by_indexes(indexes, values))

    def _get_padding_width(self, axis):
        return self._get_axis_width(axis, self.padding)

    def _get_border_width(self, axis):
        return self._get_axis_width(axis, self.border)

    def _get_margin_width(self, axis):
        return self._get_axis_width(axis, self.margin)

    def get_size(self, axis, reduce_margin=False, reduce_border=False,
                 reduce_padding=False):
        result = self._get_size(axis)
        if reduce_margin:
            result -= self._get_padding_width(axis)
        if reduce_border:
            result -= self._get_border_width(axis)
        if reduce_padding:
            result -= self._get_padding_width(axis)
        return min(result, 0)

    def get_available_space(self, axis):
        parent_size = self.parent._get_size(axis)
        non_fill_siblings = filter(
            lambda b: b._get_size_method(axis) != FILL, self.siblings
        )
        size_of_siblings = sum(map(
            lambda b: b.get_size(axis), non_fill_siblings
        ))
        space_around = self._get_margin_width(axis) + \
            self._get_border_width(axis) + self._get_padding_width(axis)
        return parent_size - size_of_siblings - space_around

    def _get_size(self, axis):
        size_method = self._get_size_method(axis)
        fixed_size_attr = {HORIZONTAL: 'width', VERTICAL: 'height'}[axis]
        if size_method == FIXED:
            return getattr(self, fixed_size_attr)
        elif size_method == HUG:
            return sum([
                b._get_size(axis) for b in self.children.values()
            ])
        elif size_method == FILL:
            if not self.parent:
                raise AssertionError('Can not use FILL if there\'s no parent')
            available_space = self.get_available_space(axis)
            num_of_shareholders = 1
            if self.direction == axis:
                num_of_shareholders = len(list(filter(
                    lambda box: box._get_size_method(axis) == FILL,
                    self.siblings
                ))) + 1
            return int(available_space / num_of_shareholders)

    def _get_pos(self, direction):
        if not self.parent:
            return 0
        offset = 0
        if direction == self.parent.direction:
            offset = sum([
                sibling.get_size(axis)
                for sibling in self.previous_siblings_list
            ])
        index = 3 if direction == HORIZONTAL else 1
        return self.parent._get_pos(axis) + \
               self.parent.margin[index] + \
               self.parent.border[index] + \
               self.parent.padding[index] + \
               offset

    def get_box(self, reduce_margin=False, reduce_border=False,
                reduce_padding=False):
        return (
            self._get_pos(HORIZONTAL),
            self._get_pos(VERTICAL),
            self._get_size(HORIZONTAL),
            self._get_size(VERTICAL)
        )
