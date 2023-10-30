-- title:   game title
-- author:  game developer, email, etc.
-- desc:    short description
-- site:    website link
-- license: MIT License 
-- version: 0.1
-- script:  lua

local H = 'H' -- Horizontal
local V = 'V' -- Vertical
local FX --..... Fixed Size
local FL --..... Auto Fill 

local min = math.min
local max = math.max
-- Frame class ----------------------
-- Define the class table
local F = {}

function F.n(t, r, b, l)
 local instance = { t, r, b, l }
 setmetatable(instance, F)
 F.__index = F
 return instance
end

function F.w(self, a)
 if a == H then 
  return self[2] + self[4]
 elseif a == V then
  return self[1] + self[3]
 end
end

-- Box class ------------------------

local B = {}

function B:n(n, w, h, p, m, b, pt, d)
 -- Box model for the game.
 -- It supports two sizing methods:
 -- Fixed (FX) and Fill (FL)
 self.__index = self
 return setmetatable({
  n   = n, --...... Name
  w   = w or FL,--. Width
  h   = h or FL,--. Height
  m   = F.n(m),--.. Margin Width
  b   = F.n(b),--.. Border Width
  p   = F.n(p),--.. Padding Width
  pt  = pt, --..... Parent
  d   = d, --...... Direction
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

function B.ss(self, break_on_hit)
 -- Get sisters by creation order.
 -- Stop at self if break_on_hit is 
 -- true
 break_on_hit = break_on_hit or false
 local r = {}
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
 if type(v) == 'number' then
 	return FX
 else
  return FL
 end
end

function B.gas(self, a)
 -- Get available space to expand
 -- in given axis.
 local c = self.pt:gs(a, 3)
 local nfs = {}
 for _, b in pairs(self:ss()) do
  if b:gsm(a) ~= F then
   table.insert(nfs, b)
  end
 end
 local ss = 0
 for _, b in pairs(nfs) do
  ss = ss + b:_gs(a)
 end
 return c - ss
end

function B.gs(self, a)
	trace(self.w)
 local sm = self:gsm(a)
 if sm == FX then
  local attr = a == H and 'w' or 'h'
  return self[attr]
 elseif sm == FL then
  assert(self.pt ~= nil)
  local as = self:gas(axis)
  local nos = 0 -- num of shares
  for i=1, i >= #self.pt.chni do 
   c = self.pt.chni[i]
   if c:gsm(axis) == FL then
    nos = nos + 1
   end
  end
  if self.pt.d == a then
   return floor(as / nos)
  end
  return as
 end
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
  test_gsm = function()
   local scr = B:n('scr')
   assert(scr.gsm(H) == FL)
   scr.width = 10
   assert(scr.gsm(H) == FX)
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
   local f = F.n(1, 2, 3, 4)
   assert(f[1] == 1)
   assert(f[2] == 2)
   assert(f[3] == 3)
   assert(f[4] == 4)
   assert(f:w(H) == 6)
   assert(f:w(V) == 4)
  end,
  test_gs_fx = function()
   local b = B:n('b', 100, 100)
   assert(b:gs(H) == 100)
   assert(b:gs(V) == 100)
  end,
  test_gs_fl = function()
   local p = B:n('p', 100, 100, 5, 5)
   local c = p:ac('c', FL, FL)
   assert(c.n == 'c')
   assert(c:gsm(H) == FL)
   assert(c:gsm(V) == FL)
   assert(c:gs(H) == 100)
  end
 },
 init = function(self)
  self._tests = {}
  for n, f in pairs(self.tests) do
   table.insert(self._tests, {n, f})
  end
 end,
 idx = 1,
 fail = false,
 tic = function(self)
  if self.idx <= #self._tests then
   local n, f = table.unpack(
    self._tests[self.idx]
   )
   local s, e = pcall(f)
   if s then
    trace("Testing " .. n .. " passed.", 5)
   else
    trace("Testing " .. n .. " failed: ", 3)
    trace(e, 3)
    self.fail = true
   end 
   self.idx = self.idx + 1
   name, func = next(self.tests)
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

