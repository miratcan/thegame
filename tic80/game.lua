-- title:   game ==  == 100100 title
-- author:  game developer, email, etc.
-- desc:    short description
-- site:    website link
-- license: MIT License 
-- version: 0.1
-- script:  lua

local H = 'H' --..Horizontal
local V = 'V' --..Vertical
local FX = 'FX' --Fixed Size
local FL = 'FL' --Auto Fill 

-- Frame class ----------------------
-- Define the class table
F = {}

function F:n(t, r, b, l)
  local o = {
  	t or 0, r or 0, b or 0, l or 0
  }
  self.__index = self
  setmetatable(o, self)
  return o
end

function F.__add(f1, f2)
  local r = F:n(0, 0, 0, 0)
  for i = 1, 4 do
    r[i] = f1[i] + f2[i]
  end
  return r
end

function F:w(a)
  local r = 0
  for i = 1, 4 do
    if a == H and (i == 2 or i == 4) then
      r = r + self[i]
    elseif a == V and (i == 1 or i == 3) then
      r = r + self[i]
    end
  end
  return r
end


-- Box class ------------------------

local B = {}

function B:n(n, w, h, m, b, p, pt, d)
 -- Box model for the game.
 -- It supports two sizing methods:
 -- Fixed (FX) and Fill (FL)
 self.__index = self

 m = F:n(table.unpack(m or {0}))
 b = F:n(table.unpack(b or {0}))
 p = F:n(table.unpack(p or {0}))
 
 return setmetatable({
  n   = n, --...... Name
  w   = w or FL,--. Width
  h   = h or FL,--. Height
  m   = m,--....... Margin Width
  b   = b,--....... Border Width
  p   = p,--....... Padding Width
  pt  = pt, --..... Parent
  d   = d or H, --. Direction
  chn = {}, --..... Chilren
  chni= {}, --..... Children indexes
  bgr = nil, --.... Background render
  fgr = nil --..... Foreground render
 }, B)
end

function B.aco(self, o)
 -- Append previously instantinated 
 -- box object.
 o.pt = self
 self.chn[o.n] = o
 table.insert(self.chni, o)
 return o
end

function B.ac(self, name, ...)
 -- Append child box by providing
 -- params.
 local o = B:n(name, ...)
 return self:aco(o)
end

function B.as(self, name, ...)
 -- Append sibling by providing 
 -- params.
 return self.pt:ac(name, ...)
end

function B.rt(self)
 -- Root of the box.
 local rt = self
 while rt.pt ~= nil do
  rt = rt.pt
 end
 return rt
end

function B:ss(break_on_hit)
 -- Get sisters by creation order.
 -- St at self if break_on_hit is 
 -- true
 break_on_hit = break_on_hit or false
 local r = {}
 local s
 for i=1, #self.pt.chni do
 	s = self.pt.chni[i]
  if s == self then
   if break_on_hit then
    break
   else
    goto continue
   end
  end
  table.insert(r, s)
  ::continue::
 end
 return r
end

function B.ps(self)
 -- Previous siblings of the box.
 return self:ss(true)
end

function B.gsm(self, a)
 -- Get size method on axis.
 local m = (a == H) and 'w' or 'h'
 local v = self[m]
 if v == FL then return FL end
 return FX
end

function B:gas(a)
 -- Get available space to expand
 -- in given axis.
 local r = self.pt:gis(a)
 local ss = self:ss() -- sisters
 for i=1, #ss do
  local s = ss[i]
  if s:gsm(a) == FX then
   r = r - s:gs(a)
  end
 end
 return r
end

function B:gs(a)
 local sm = self:gsm(a)
 if sm == FX then
  local attr = a == H and 'w' or 'h'
  return self[attr]
 elseif sm == FL then
  assert(self.pt ~= nil)
  local as = self:gas(a)
  if self.pt.d ~= a then
   return as
  end
  local nos = 0 -- num of shares
  for i=1, #self.pt.chni do
   local c = self.pt.chni[i]
   if c:gsm(a) == FL then
    nos = nos + 1
   end
  end
  return math.floor(as / nos)
 end
end

function B:gis(a, l)
 -- Get inner size.
 l  = l or 3
 local r = self:gs(a)
 local ms = {'m', 'b', 'p'}
 for i=1, #ms[3] do
  local m = ms[i] -- Method
  local f = self[m] -- Frame
  r = r - f:w(a)
 end
 return r
end

function B:pos(l)
 -- Build bounding box
 -- Only parent must call this.
 l = l or 0
 local r = {x=0, y=0}
 if not self.pt then return r end

 local ms = {'m', 'b', 'p'}
 local p = self.pt
 -- Get inner position of parent.
 repeat
 	for i=1, #ms do
   local f = p[ms[i]]
   r['x'] = r['x'] + f[4]
   r['y'] = r['y'] + f[1]
  end
  p = p.pt
 until(p == nil)

 -- Add push from previous siblings
 local pss = self:ps()

 -- TODO: This can be shorter imo.
 local k
	if self.pt.d == H then k = 'x'
	elseif self.pt.d == V then k = 'y'
	else error('WTF') end

 for i=1, #pss do
 	local ps = pss[i]
  r[k] = r[k] + ps:gs(self.pt.d)
 end

 return r
end

local testRunner = {
 tests = {
  test_crate_boxes = function()
   local scr = B:n('scr'):ac('hdr'):rt()
   assert(scr.n == 'scr')
   assert(scr.chn.hdr.n == 'hdr')
   local b = B:n('bdy')
   assert (b.n == 'bdy')
   scr:aco(b)
   assert(scr.chn.bdy.n == 'bdy')
  end,
  test_ac = function()
   local p = B:n('p')
   local c = p:ac('c')
   assert(c.pt == p)
  end,
  test_aco = function()
   local p = B:n('p')
   local c = B:n('c')
   p:aco(c)
   assert(c.pt == p)
  end,
  test_gsm_fl = function()
   local b = B:n('b')
   assert(b:gsm(H) == FL)
   assert(b:gsm(V) == FL)
  end,
  test_gsm_fx = function()
   local b= B:n('b', 100, 100)
   assert(b:gsm(H) == FX)
   assert(b:gsm(V) == FX)
  end,
  test_ps = function()
   local pt = B:n('pt')
   pt:ac('c1'):as('c2'):as('c3')
   assert(#pt.chn.c1:ps() == 0)
   assert(#pt.chn.c2:ps() == 1)
   assert(#pt.chn.c3:ps() == 2)
  end,
  test_ss= function()
   local pt = B:n('pt')
   pt:ac('c1'):as('c2'):as('c3')
   assert(#pt.chn.c1:ss() == 2)
   assert(#pt.chn.c2:ss() == 2)
   assert(#pt.chn.c3:ss() == 2)
  end,
  test_f = function()
   local f = F:n(1, 2, 3, 4)
   assert(f[1] == 1)
   assert(f[2] == 2)
   assert(f[3] == 3)
   assert(f[4] == 4)
   assert(f:w(H) == 6)
   assert(f:w(V) == 4)
   f = F:n()
  end,
  test_gs_fx = function()
   local b = B:n('b', 100, 100)
   assert(b:gs(H) == 100)
   assert(b:gs(V) == 100)
  end,
  test_gs_fl = function()
   -- Test get fill type size
   local p = B:n('p', 100, 100)
   local c = p:ac('c1')
   assert(c:gs(H) == 100)
   assert(c:gs(V) == 100)
  end,
  test_gs_fl_ws = function()
   -- Test fill type size with
   -- siblings.
   local p = B:n('p', 100, 100)
   local c1 = p:ac('c1')
   p:ac('c2')
   assert(c1:gs(H) == 50)
  end,
  test_pos = function()
   local p = B:n('p', 100, 100, {10, 2, 10, 2})
   local c = p:ac('c')
   local pos = c:pos()
   assert(pos['x'] == 2)
   assert(pos['y'] == 10)
  end,
  test_pos_ws = function()
   local p = B:n('p', 100, 100, {10, 2, 10, 2})
   local c1 = p:ac('c1')
   local c2 = p:ac('c2')
   local pos = c1:pos()
   assert(pos['x'] == 2)
   assert(pos['y'] == 10)
   pos = c2:pos()
   trace(pos['x'], 12)
   trace(pos['y'], 12)
  end
 },
 init = function(self)
  self._tests = {}
  for n, f in pairs(self.tests) do
   if self.isolate and n ~= self.isolate then
     goto continue
   end
   table.insert(self._tests, {n, f})
   ::continue::
  end
  self.m = 320 / #self._tests
 end,
 idx = 1,
 fail = false,
 tic = function(self)
  if self.idx <= #self._tests then
   local n, f = table.unpack(
    self._tests[self.idx]
   )
   cls()
   rect(0, 0, self.idx * self.m, 1, 4)
   print('Running Tests:' .. n, 8, 8)
   local s, e = pcall(f)
   if s then
    trace("Testing " .. n .. " passed.", 5)
   else
    trace("Testing " .. n .. " failed: ", 3)
    trace(e, 3)
    self.fail = true
   end 
   self.idx = self.idx + 1
  else
   if self.fail then
    cls(3)
    print('Tests are failed, check traceback')
    return 'FAILED'
   else
    return 'COMPLETED'
   end
  end
 end
}
-- TODO: Boomkark ?
-- Initialize tests -----------------

local READY = false
testRunner:init()
screen = B:n('screen', 240, 139)

function TIC()
 if READY == false then
  READY = testRunner:tic() == 'COMPLETED'
  return
 end
 cls()
 print("HELLO WORLD!",84,84)
end

-- <TILES>
-- 001:eccccccccc888888caaaaaaaca888888cacccccccacc0ccccacc0ccccacc0ccc
-- 002:ccccceee8888cceeaaaa0cee888a0ceeccca0ccc0cca0c0c0cca0c0c0cca0c0c
-- 003:eccccccccc888888caaaaaaaca888888cacccccccacccccccacc0ccccacc0ccc
-- 004:ccccceee8888cceeaaaa0cee888a0ceeccca0cccccca0c0c0cca0c0c0cca0c0c
-- 017:cacccccccaaaaaaacaaacaaacaaaaccccaaaaaaac8888888cc000cccecccccec
-- 018:ccca00ccaaaa0ccecaaa0ceeaaaa0ceeaaaa0cee8888ccee000cceeecccceeee
-- 019:cacccccccaaaaaaacaaacaaacaaaaccccaaaaaaac8888888cc000cccecccccec
-- 020:ccca00ccaaaa0ccecaaa0ceeaaaa0ceeaaaa0cee8888ccee000cceeecccceeee
-- </TILES>

-- <WAVES>
-- 000:00000000ffffffff00000000ffffffff
-- 001:0123456789abcdeffedcba9876543210
-- 002:0123456789abcdef0123456789abcdef
-- </WAVES>

-- <SFX>
-- 000:000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000303000000000
-- </SFX>

-- <TRACKS>
-- 000:100000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
-- </TRACKS>

-- <PALETTE>
-- 000:1a1c2c5d275db13e53ef7d57ffcd75a7f07038b76425717929366f3b5dc941a6f673eff7f4f4f494b0c2566c86333c57
-- </PALETTE>

