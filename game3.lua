-- title:   game title
-- author:  game developer, email, etc.
-- desc:    short description
-- site:    website link
-- license: MIT License (change this to your license of choice)
-- version: 0.1
-- script:  lua

FL = 'FL'

local ip=ipairs
local insert=table.insert
local FL='FL'
local SIDES = {'t', 'r', 'b', 'l'}

local function merge(...)
 local result = {}
  for _, tbl in ipairs({...}) do
    for key, value in pairs(tbl) do
      result[key] = value
    end
  end
  return result
end


local debugger={
 ['x']=0,
 ['y']=8,
 ['indent']=2,
 ['dsx']=nil, -- Drag start x
 ['dsy']=nil, -- Drag start y
 ['dsmx']=nil,-- Drag start mouse x
 ['dsmy']=nil,-- Drag start mouse y
 ['a']=false, -- Active or not.
 ['k']=48, --... Key to activate
 ['bgc']=11, --. background color
 ['values']={1},
}

function debugger:_print(
 tbl, indent, printed
)
 indent = indent or 0
 printed = printed or {}
 for k, v in pairs(printed) do
  trace(tostring(k)..':'..tostring(v))
 end
 if indent > 5 then return 'Handbrake', printed end
 local r = ''
 local prefix
 for k, v in pairs(tbl) do
  if
    type(v) == 'function' or
    string.sub(k, 1, 2) == '__'
  then
    goto continue
  end

  prefix = string.rep(" ", indent)..k..": "
  r = r..prefix
  if type(v) == "table" then
   if not printed[v] then
    local _r, _printed= self:_print(
     v, indent+1, printed
    )
    printed = merge(
      printed, _printed, {[v]=true}
    )
    r = r..'\n'.. _r
   else

    r = r..'\n'..tostring(v)
   end
  elseif type(v) == 'boolean' then
   r = r..tostring(v).. '\n'
  else
   r = r..v..'\n'
  end
  :: continue ::
 end
 --[[
 local metatable = getmetatable(tbl)
 if metatable then
  prefix = prefix..'Metatable: \n'
  r = r..prefix..self:_print(metatable, indent)
 end
 ]]--
 return r, printed
end

function debugger:tic()
 if keyp(self.k) then
  self.a =not self.a
 end
 if not self.a then return end
 local mx, my, clk, _, _, _, _=mouse()
 if clk then
  if not self.dsx then
   self.dsx=self.x
   self.dsy=self.y
   self.dsmx=mx
   self.dsmy=my
  end
  self.x=self.dsx - (self.dsmx - mx)
  self.y=self.dsy - (self.dsmy - my)
 else
  self.dsx=nil
 end
 if self.bgc then
  rect(0, 0, 240, 138, self.bgc)
 end
 print(self:_print(self.values), self.x, self.y)
 rect(0, 0, 240, 6, 6)
 print('DEBUGGER', 0, 0)
end


S = {}

function S:new(w, c)
  local o = {['w'] = w or 0, ['c'] = c}
  setmetatable(o, self)
  self.__index = S
  return o
end

F = {['t'] = S:new(), ['r'] = S:new(),
     ['b'] = S:new(), ['l'] = S:new()}

function F:new(props)
  -- Frame
  -- f = F:new({t={c:4}})
  local o = o or {}
  for _, k in ipairs(SIDES) do
    local pval = props[k]
    if not pval then goto continue end
    o[k] = S:new(pval['w'], pval['h'])
    ::continue::
  end
  setmetatable(o, self)
  self.__index = F
  return o
end


function F:wth(iv)
if iv then return self.t.w + self.b.w
else return self.l.w + self.r.w end
end

local f = F:new({['t']={['c']=3}})

-- Box Class -------------------------

B = {
  w=nil,
  h=nil,
  frs={F:new(). F:new(), F:new()},
}

function B:new(o)
  o = o or {}
  setmetatable(o, self)
  self.__index = B
  return o
end

function TIC()
  cls()
  debugger.values = {
    ['a'] = 1, f=f
  }
  debugger:tic()
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
-- 000:000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000304000000000
-- </SFX>

-- <TRACKS>
-- 000:100000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
-- </TRACKS>

-- <PALETTE>
-- 000:1a1c2c5d275db13e53ef7d57ffcd75a7f07038b76425717929366f3b5dc941a6f673eff7f4f4f494b0c2566c86333c57
-- </PALETTE>

