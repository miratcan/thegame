
# script: python

HUG, FILL, FIXED = 'HUG', 'FILL', 'FIXED'
HORIZONTAL, VERTICAL = 'H', 'V'
FRAME_TYPES = 'margin', 'border', 'padding'


def get_values_by_indexes(index_list, value_list):
    return [value_list[index] for index in index_list]


def attr_getter(d, key):
    def inner(key):
        return d[key]


class Box(object):
    def __init__(
        self,
        name=None,
        width=HUG,
        height=HUG,
        padding=[0, 0, 0, 0],
        margin=[0, 0, 0, 0],
        border=[0, 0, 0, 0],
        parent=None,
        direction=HORIZONTAL
    ):
        self.name = name
        self.width = width
        self.height = height
        self.padding = padding
        self.margin = margin
        self.border = border
        self.parent = parent
        self.direction = direction
        self.children = {}

    def __repr__(self):
        if self.name:
            return '<Box: %s>' % self.name
        return super().__str__(self)

    def __getattr__(self, name):
        if name in self.children:
            return self.children[name]
        return object.__getattribute__(self, name)

    def add_child(self, name, *args, **kwargs):
        self.children[name] = Box(name, *args, **kwargs, parent=self)
        self.children[name].parent = self
        return self.children[name]

    def add_child_obj(self, *objs):
        for obj in objs:
            obj.parent = self
            self.children[obj.name] = obj

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
        method = {HORIZONTAL: 'width', VERTICAL: 'height'}[axis]
        if type(getattr(self, method)) == int:
            return FIXED
        return getattr(self, method)

    def _get_frame_width(self, axis, frame):
        assert axis in (HORIZONTAL, VERTICAL)
        indexes = [1, 3] if axis == HORIZONTAL else [0, 2]
        return sum(get_values_by_indexes(indexes, frame))

    def _get_padding_width(self, axis):
        return self._get_frame_width(axis, self.padding)

    def _get_border_width(self, axis):
        return self._get_frame_width(axis, self.border)

    def _get_margin_width(self, axis):
        return self._get_frame_width(axis, self.margin)

    def _get_size(self, axis, inner_level=0):
        result = self._get_full_size(axis)
        methods = ['_get_%s_width' % s for s in FRAME_TYPES]
        for method in methods[:inner_level]:
            result -= getattr(self, method)(axis)
        return max(result, 0)

    def get_available_space(self, axis):
        parent_content_size = self.parent._get_size(axis, inner_level=3)
        non_fill_siblings = filter(
            lambda b: b._get_size_method(axis) != FILL, self.siblings
        )
        size_of_siblings = sum(map(
            lambda b: b._get_size(axis), non_fill_siblings
        ))
        return parent_content_size - size_of_siblings

    def _get_full_size(self, axis):
        size_method = self._get_size_method(axis)
        fixed_size_attr = {HORIZONTAL: 'width', VERTICAL: 'height'}[axis]
        if size_method == FIXED:
            return getattr(self, fixed_size_attr)
        elif size_method == HUG:
            return \
                sum([b._get_full_size(axis)
                     for b in self.children.values()]) + \
                self._get_margin_width(axis) + \
                self._get_border_width(axis) + \
                self._get_padding_width(axis)
        elif size_method == FILL:
            if not self.parent:
                raise AssertionError('Can not use FILL if there\'s no parent')
            available_space = self.get_available_space(axis)
            num_of_shareholders = len(list(filter(
                lambda box: box._get_size_method(axis) == FILL,
                self.parent.children.values()
            ))) if self.parent.direction == axis else 1
            return int(available_space / num_of_shareholders)

    def _get_pos(self, axis, inner_level=0):
        index = 3 if axis == HORIZONTAL else 0
        push_from_frames = sum([
            frame[index] for frame in
            [self.margin, self.border, self.padding][:inner_level]
        ])
        if not self.parent:
            return push_from_frames
        push_from_siblings = 0
        if axis == self.parent.direction:
            push_from_siblings = sum([
                sibling._get_size(axis)
                for sibling in self.previous_siblings_list
            ])
        push_from_parent = sum([
            frame[index] for frame in
            [self.parent.margin, self.parent.border, self.parent.padding]
        ])
        return \
            self.parent._get_pos(axis) + \
            push_from_parent + \
            push_from_siblings + \
            push_from_frames

    @property
    def x(self):
        return self._get_pos(HORIZONTAL)

    @property
    def y(self):
        return self._get_pos(VERTICAL)

    def get_bounding_box(self, inner_level=0):
        return (
            self._get_pos(HORIZONTAL, inner_level),
            self._get_pos(VERTICAL, inner_level),
            self._get_size(HORIZONTAL, inner_level),
            self._get_size(VERTICAL, inner_level)
        )

    def _render(self):
        print('render:', self.name)
        x, y, w, h = self.get_bounding_box(inner_level=3)
        self.render(x, y, w, h)
        for child in self.children.values():
            child._render()

    def render(self, x, y, w, h):
        pass
