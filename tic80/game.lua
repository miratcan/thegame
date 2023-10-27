-- title:   game title
-- author:  game developer, email, etc.
-- desc:    short description
-- site:    website link
-- license: MIT License (change this to your license of choice)
-- version: 0.1
-- script:  lua

local H = 'H' -- Horizontal
local V = 'H' -- Vertical
local FX --..... Fixed Size
local FL --..... Auto Fill 

-- Frame class ----------------------
local F = {}

function F.n(v)
 return setmetatable({ s = v }, F)
end

F.__index = function(self, i)
 return self.s[i % #self.s + 1]
end

-- Box class ------------------------

local B = {}

function B:n(n, w, h, p, m, b, pt, d)
 self.__index = self -- WHY AMK?
 return setmetatable({
  n   = n, --...... Name
  w   = w, --...... Width
  h   = h, --...... Height
  p   = F.n(p),--.. Padding Width
  m   = F.n(m),--.. Margin Width
  b   = F.n(b),--.. Border Width
  pt  = pt, --..... Parent
  d   = d, --...... Direction
  chn = {}, --..... Chilren
  bgr = nil, --.... Background render
  fgr = nil --..... Foreground render
 }, B)
end

function B.ac(self, name, ...)
 -- Append child box by providing
 -- params.
 self.chn[name] = B:n(name, ...)
 self.chn[name].pt = self
 return self.chn[name]
end

function B.aco(self, ...)
 -- Append previously instantinated 
 -- box object.
 for _, o in ipairs{...} do
  o.pt = self
  self.chn[o.n] = o
  return o
 end
end

function B.as(self, name, ...)
 -- Append sibling by providing 
 -- params.
 return self.parent:ac(name, ...)
end

function B.rt(self)
 -- Root of the box.
 local rt = self
 while rt.pt ~= nil do
  rt = rt.pt
 end
 return rt
end

function B.ss(self)
 -- Siblings of the box.
 local r = {}
 for _, b in pairs(self.pt.chn) do
  if b ~= self then
   table.insert(r, b)
  end
 end
 return r
end

function B.ps(self)
 -- Previous siblings of the box.
 local r = {}
 for _, s in pairs(self.pt.chn) do
  if s == self then
   break
  end
  table.insert(r, s)
 end
 return r
end

function B.gsm(self, a)
 -- Get size method on axis.
 local m = (a==H) and 'w' or 'h'
 return type(self[m]) == 'number'and
        FX or self[m]
end

function B.gfw(f, a)
 -- Get total frame width in given 
 -- axis.
 local i=(a==H) and {1,3} or {0, 2}
 local w = 0
 for _, j in ipairs(i) do
  w = w + f[j + 1]
 end
 return w
end

function B.gpw(self, a)
 -- Get padding width in given axis.
 return self:gfw(a, self.p)
end

function B.gmw(self, a)
 -- Get margin width in given axis.
 return self:gfw(a, self.m)
end

function B.gbw(self, a)
 -- Get border width in given axis.
 return self:gfw(a, self.b)
end

function B.gas(self, a)
 -- Get available space to expand
 -- in given axis.
 local c = self.pt:_gs(a, 3)
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

function B.r(self) 
 if self.r_bg ~= nil then
  x, y, w, h = self.get_
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
   assert(scr.gsm(H) == 'FL')
  end,
  test_zoo = function()
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
   local n, f = table.unpack(self._tests[self.idx])
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

