# title:   game title
# author:  game developers, email, etc.
# desc:    short description
# site:    website link
# license: MIT License (change this to your license of choice)
# version: 0.1
# script:  python

t=0
x=96
y=24

class Canvas:
 
 size = (0, 0)
 
 def __init__(slf, ox=0, oy=0):
  slf.ox = ox # Offset x 
  slf.oy = oy # Offset y

 @property
 def draw(slf):
  slf.size = (0, 0)
  return slf

 def rect(slf, x, y, w, h, c, dry=False):
  if not dry:
   rect(x + slf.ox, y + slf.oy, w, h, c)
  slf.size = (
   max(slf.size[0], x + w)
   max(slf.size[1], y + h)
  )
  return slf

"""
def render(slf, dry=False):
 return self.canvas
  .draw('rect', 10, 10, 40, 40, 3)
  .draw('rect', 0, 0, 40, 40, 12)
"""
  

class Box:
 def __init__(
  slf, dir='H', nme=None, prt=None,
  wth=None, hgt=None,
  pwt=None, bwt=None, mwt=None, gap=0):
  pwt = pwt or [0, 0, 0, 0]
  bwt = bwt or [0, 0, 0, 0]
  mwt = mwt or [0, 0, 0, 0]
  slf.dir, slf.nme, slf.prt, slf.wth, \
   slf.hgt, slf.pwt, slf.bwt, slf.mwt = [
   dir, nme, prt, wth, hgt, pwt, bwt, mwt]
  slf.canvas = Canvas()
   
  def calc_wth(slf, incl_m=True, incl_b=True, \
               incl_p=True):
   pass
   
  def rect(x, y, w, h, c, dry=False):
   tw = x + w # Total Width
   th = y = h # Total Height
  
  def render(slf, dry=False):
   return slf.c.rect(0, 0, 10, 10, 4)
 
box = Box()
trace(box.canvas.draw.rect(0, 0, 30, 30, 4).rect(30, 0, 30, 30, 2).t_wth)

def TIC():
 t+=1

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

