# title:   game title
# author:  game developers, email, etc.
# desc:    short description
# site:    website link
# license: MIT License
# version: 0.1
# script:  python

from math import pow as p

line = globals()['line']
rect = globals()['rect']
spr = globals()['spr']
clip = globals()['clip']
cls = globals()['cls']

fc         = 0   # Frame counter
SW         = 240 # Screen width
SH         = 136 # Screen height
CX         = 120 # Screen center x
CY         = 68  # Screen center y
CW         = 6   # Character width
CH         = 4   # Character height
APP_STATES = [
 'MENU',         # 0
 'INGAME',       # 1
 'GMOVER',       # 2
]

astate_ttf = 60
astate_tcf = 0
astate_c   = None
astate_n   = 1

gstate_ttf = 120
gstate_tcf = 0
gstate_c   = {
 'health':50,
 'army': 25
}
gstate_n   = gstate_c.copy()

chars = {
 'kenan': {
  'sid': 17,
  'nm': 'General Kenan'
 },
 'eren': {
  'sid': 21,
  'nm': 'Eren'
 }
}

card_bps = {
 'kenan': {
  'char': 'eren',
  'text': 'Oyuna Hosgeldin'
 }
}

def card_factory(bpk, x, y, tx=None,
                 ty=None):
 global fc
 bp = card_bps[bpk]
 char = chars[bp['char']]
 return {
  'sid': char['sid'],
  'text': bp['text'],
  'x': x, 'y': y,
  'ts': [{
   'sx': x, 'sy': y,
   'tx': tx or x, 'ty': ty or y,
   'sf': fc, 'tf': fc+60 if tx else None
  }]
 }

def card_transition_processer(card):
 global fc
 if not card['ts']: return
 ts = card['ts'][0] # Transition
 tf = ts['tf'] # Target Frame
 if not tf or fc > tf:
  card['ts'].pop()
  return
 sf = ts['sf'] # Start frame
 ft = tf - sf # Total frames
 cr = ease((fc-sf)/ft) # Complete ratio
 vx, vy = (ts['tx']-ts['sx'],
           ts['ty']-ts['sy'])
 trace((vx, vy))
 nx, ny = norm(vx, vy)
 trace((nx, ny))
 card['x'] = ts['sx'] + (nx * cr) * vx
 card['y'] = ts['sy'] + (ny * cr) * vy


card_c = card_factory(
 'kenan', 2, SH, 2, 16)

# Renderer functions ------------------

def void_r():
 rect(0,0,SW,SH,0)

def menu_r():
 rect(0,0,W,SH,4)
 print('menu',CX,CY)

def _stat_frame_r(fx,fy,fw,fh):
 line(fx+1,fy,fx+fw-1,fy,15)
 line(fx+1,fy+fh,fx+fw-1,fy+fh,13)
 line(fx,fy+1,fx,fy+fh-1,15)
 line(fx+fw,fy+1,fx+fw,fy+fh-1,13)

def _stat_pbar_r(fx,fy,fw,fh,gskey):
 global gstate_c
 v=int((fw-1)/100*gstate_c[gskey])
 rect(fx+1,fy+1,v,fh-1,3)
 rect(fx+v+1,fy,fw-v-1,fh,0)

def stat_r(title,gskey,slot,pad=2):
 global gstate_c,gstate_n,\
  _state_frame_r
 x=60*slot
 fx,fy,fw,fh = x+pad,2,60-(pad*2),8
 _stat_frame_r(fx,fy,fw,fh)
 _stat_pbar_r(fx,fy,fw,fh,gskey)
 print(title, x+pad+2, 4,4)

def card_r(card):
 x,y=int(card['x']), int(card['y'])
 w,h=16,10
 for xi in range(w):
  for yi in range(h):
   s=9
   if yi==0:
    s=7
    if xi==0:s=1
    elif xi==w-1:s=2
   elif yi == h-1:
    s=5
    if xi==0:s=3
    elif xi==w-1:s=4
   else:
    if xi==0:s=6
    elif xi==w-1:s=8
   sx,sy=x+(xi*8),y+(yi*8)
   spr(s,sx,sy,0)
 spr(card['sid'],x,y+8,9,1,0,0,4,4)
 print(card['text'],x+32, y+8, 15,False,1,False,False)

def ingame_r():
 cls(7)
 print('game',CX,CY)
 stat_r('HEALTH',  'health', 0)
 stat_r('DICTA',   'army',   1)
 stat_r('ARMY',    'army',   2)
 stat_r('RELIGION','army',   3)
 card_transition_processer(card_c)
 card_r(card_c)

def norm(x, y):
 if x>y: return (1,y/x)
 if y<x: return (x/y,1)
 return 1.0,1.0

def ease(x):
 global p
 return 4 * x * x * x \
  if x < 0.5 else \
  1 - p(-2 * x + 2, 3) / 2

def transition_r():
 global W, H,astate_tcf,astate_ttf,\
  astate_c,astate_n
 e = ease(astate_tcf/astate_ttf)
 x = int(e*SW)
 clip(0,0,x,SH)
 astate_r(astate_n)
 clip(x,0,SW-x,SH)
 astate_r(astate_c)
 astate_tcf+=1
 if astate_tcf>=astate_ttf:
  astate_c=astate_n
  astate_n=None
  clip(0,0,SW,SH)

def astate_r(astate):
 if not astate:
  return void_r()
 [menu_r,ingame_r][astate]()

def TIC():
 global astate_c, astate_n, fc,\
  astate_c,astate_n,astate_ttf,\
  astate_tcf,CX,CY
 if astate_tcf<astate_ttf:
  transition_r()
 astate_r(astate_c)
 fc+=1

# <TILES>
# 001:000fffff00fddddd0fdcccccfdccccccfdccccccfdccccccfdccccccfdcccccc
# 002:fffff000dddddf00cccccdf0ccccccdfccccccdfccccccdfccccccdfccccccdf
# 003:fdccccccfdccccccfdccccccfdccccccfdcccccc0fdccccc00fddddd000fffff
# 004:ccccccdfccccccdfccccccdfccccccdfccccccdfcccccdf0dddddf00fffff000
# 005:ccccccccccccccccccccccccccccccccccccccccccccccccddddddddffffffff
# 006:fdccccccfdccccccfdccccccfdccccccfdccccccfdccccccfdccccccfdcccccc
# 007:ffffffffddddddddcccccccccccccccccccccccccccccccccccccccccccccccc
# 008:ccccccdfccccccdfccccccdfccccccdfccccccdfccccccdfccccccdfccccccdf
# 009:cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
# 017:9999999999999990999999009999990099999000999990009999900099999000
# 018:0000000000000000000000000000000000000000000000000000000200000023
# 019:0000000000002000000222000022322002233320223333202333332033333320
# 020:9999999909999999009999990099999900099999000999990009999900099999
# 021:9999999999999999999999999999999099999990999999009999900099999000
# 022:9999900099000000000000000000033300033333003333330334333333433333
# 023:0009999900000099000000003330000033333000333333003333333033333333
# 024:9999999999999999999999990999999909999999009999990009999900099999
# 025:9999999999999999999999999999999999999999999999999999999999999999
# 026:9999999999999999999999999999999999999999999999999999999999999999
# 027:9999999999999999999999999999999999999999999999999999999999999999
# 028:9999999999999999999999999999999999999999999999999999999999999999
# 033:9999900099999000999990009999900099999000999990009999900099999000
# 034:000022332222333333333333333000033333e033333300333333333333333333
# 035:3333332033333332333333333000033333e03333330033333333333333333333
# 036:0009999900099999000999990009999900099999000999990009999900099999
# 037:9999900099999003999990039999900399999003999990039999900399999003
# 038:3333333333333333333333333000003330000033333333333333333333330333
# 039:3333333333333333333333333300000333000003333332233333333323303333
# 040:0009999930099999300999993009999930099999300999993009999930099999
# 041:9999999999999999999999999999999999999999999999999999999999999999
# 042:9999999999999999999999999999999999999999999999999999999999999999
# 043:9999999999999999999999999999999999999999999999999999999999999999
# 044:9999999999999999999999999999999999999999999999999999999999999999
# 049:9999990099999900999999009999999099999990999999909999999999999999
# 050:3333333333333333333333003333332233333333333311110333333303333333
# 051:3333333333333333003333332233333333333333111133333333333033333330
# 052:0099999900999999009999990999999909999999099999999999999999999999
# 053:9999903399999033999999039999990399999903999999909999999099999999
# 054:3333333333443333334433333333330033333322333333333333000003333333
# 055:2333333333334433333344330033333322333333333333330000333333333330
# 056:3309999933099999309999993099999930999999099999990999999999999999
# 057:9999999999999999999999999999999999999999999999999999999999999999
# 058:9999999999999999999999999999999999999999999999999999999999999999
# 059:9999999999999999999999999999999999999999999999999999999999999999
# 060:9999999999999999999999999999999999999999999999999999999999999999
# 065:9999999999999999999999999999999999999999999999999999999999999999
# 066:9033333399033333999033339999000099999999999999999999999999999999
# 067:3333330933333099333309990000999999999999999999999999999999999999
# 068:9999999999999999999999999999999999999999999999999999999999999999
# 069:9999999999999999999999999999999999999999999999999999999999999999
# 070:9033333399033333999033339999003399999900999999999999999999999999
# 071:3333330933333099333309993300999900999999999999999999999999999999
# 072:9999999999999999999999999999999999999999999999999999999999999999
# 073:9999999999999999999999999999999999999999999999999999999999999999
# 074:9999999999999999999999999999999999999999999999999999999999999999
# 075:9999999999999999999999999999999999999999999999999999999999999999
# 076:9999999999999999999999999999999999999999999999999999999999999999
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
# 000:1a1c2c5d275db13e53ef8d65ffcd75a7f07038b76425717929366f3b5dc941a6f673eff7f4f4f494b0c2566c86333c57
# </PALETTE>

