# title:   game title
# author:  game developers, email, etc.
# desc:    short description
# site:    website link
# license: MIT License (change this to your license of choice)
# version: 0.1
# script:  python

HORIZONTAL = 'h'
VERTICAL = 'v'


def _obj_to_str(obj, *keys):
    output = ''
    if obj.name:
        output = obj.name + '\n'
    width = len(sorted(keys, key=len)[-1]) + 2
    for i, k in enumerate(keys):
        needed_dots = width - len(k)
        key = k + '.' * needed_dots + ': '
        output += key + str(getattr(obj, k)) + '\n'
    return output


def _trace_obj(obj, *keys):
    text = '\n' + _obj_to_str(obj, *keys)
    trace(text)


def _print_obj(obj, *keys):
    text = _obj_to_str(obj, *keys)
    print(text, obj.x + 2, obj.y + 2)


class Box:
 def __init__(
  slf,              # Self
  dir='h',          # Direction
  nme=None,         # Name
  pnt=None,         # Anchestor
  wth=None,         # Width (None: Auto)
  hgt=None,         # Height (None: Auto)
  gap=0,            # Gap
  pwt=None,         # Padding width 
  bwt=None,         # Border width
  mwt=None          # Margin width
 ):
  pwt = pwt or [0, 0, 0, 0]
  bwt = bwt or [0, 0, 0, 0]
  mwt = mwt or [0, 0, 0, 0]
  for key in ('dur', 'nme', 'pnt', 'gap', 'pwt',
              'bwt', 'mwt'):
   setattr(s, key, locals()[key])
  self.slts = []

  def _slot_cnt(s, axs): # Slot Count
   # If box is horizontal, and asked for vertical
   # slot count, it always 1.
   if axs != self.dir: return 1
   return len(self.slts)

  def _size(self, a):
   if not self.s:
    return {HORIZONTAL: 240, VERTICAL: 136}[axis]
   parent_slot_count = self.parent._slot_count(axis)
   return self.parent._size(axis) / parent_slot_count

    def _pos(self, axis):
        """
        x parent.size 320
        """
        index = 0
        if axis == self.parent.d:
            index = self.index
        multiplier = self.parent._size(axis) / self.parent._slot_count(axis)
        trace(self.gap)
        return (multiplier * index) + self.parent.gap

    def _slot_index(self, box):
        return self.slots.index(box)

    @property
    def index(self):
        return self.parent._slot_index(self)

    @property
    def x(self):
        return int(self._pos(HORIZONTAL))

    @property
    def y(self):
        return int(self._pos(VERTICAL))

    @property
    def slot_count(self):
        return self._slot_count(self, self.axis)

    @property
    def w(self):
        return int(self._size(HORIZONTAL))

    @property
    def h(self):
        return int(self._size(VERTICAL))

    def append(self, box):
        box.parent = self
        self.slots.append(box)

    def render(self):
        if self.parent:
            rectb(self.x, self.y, self.w, self.h, self.index+3)
            _print_obj(self, 'x', 'y', 'w', 'h', 'index')
            _trace_obj(self, 'x', 'y', 'w', 'h', 'index')
        for slot in self.slots:
            slot.render()


screen = Box(gap=20)

left_panel = Box(name='Left Panel')
left_panel2 = Box(name='Left Panel')
right_panel = Box(name='Right Panel')

screen.append(left_panel)
screen.append(left_panel2)
screen.append(right_panel)


def TIC():
    cls(0)
    screen.render()


# <TILES>
# 001:eccccccccc888888caaaaaaaca888888cacccccccacc0ccccacc0ccccacc0ccc
# 002:ccccceee8888cceeaaaa0cee888a0ceeccca0ccc0cca0c0c0cca0c0c0cca0c0c
# 003:eccccccccc888888caaaaaaaca888888cacccccccacccccccacc0ccccacc0ccc
# 004:ccccceee8888cceeaaaa0cee888a0ceeccca0cccccca0c0c0cca0c0c0cca0c0c
# 017:cacccccccaaaaaaacaaacaaacaaaaccccaaaaaaac8888888cc000cccecccccec
# 018:ccca00ccaaaa0ccecaaa0ceeaaaa0ceeaaaa0cee8888ccee000cceeecccceeee
# 019:cacccccccaaaaaaacaaacaaacaaaaccccaaaaaaac8888888cc000cccecccccec
# 020:ccca00ccaaaa0ccecaaa0ceeaaaa0ceeaaaa0cee8888ccee000cceeecccceeee
# </TILES>

# <WAVES>
# 000:00000000ffffffff00000000ffffffff
# 001:0123456789abcdeffedcba9876543210
# 002:0123456789abcdef0123456789abcdef
# </WAVES>

# <SFX>
# 000:000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000304000000000
# </SFX>

# <TRACKS>
# 000:100000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# </TRACKS>

# <PALETTE>
# 000:1a1c2c5d275db13e53ef7d57ffcd75a7f07038b76425717929366f3b5dc941a6f673eff7f4f4f494b0c2566c86333c57
# </PALETTE>

