-- Constants
local H, V = 'H', 'V'
local F, FX, HG = 'F', 'FX', 'HG'

-- Frame class
local Frame = {}

function Frame.n(v)
 return setmetatable({ s = v }, Frame)
end

Frame.__index = function(self, i)
 return self.s[i % #self.s + 1]
end

-- B class (formerly Box)
local B = {}

function B.n(name, w, h, p, m, b, parent, d)
 return setmetatable({
  name = name,
  w = w,
  h = h,
  p = Frame.n(p),
  m = Frame.n(m),
  b = Frame.n(b),
  parent = parent,
  direction = d,
  children = {},
  bg_renderer = nil,
  fg_renderer = nil
 }, B)
end

B.__index = function(self, name)
 return self.children[name]
end

function B.ac(self, name, ...)
 self.children[name] = B.n(name, ...)
 self.children[name].parent = self
 return self.children[name]
end

function B.aco(self, ...)
 for _, o in ipairs{...} do
  o.parent = self
  self.children[o.name] = o
 end
end

function B.as(self, name, ...)
 return self.parent:ac(name, ...)
end

function B.r(self)
 local r = self
 while r.parent do
  r = r.parent
 end
 return r
end

function B.ss(self)
 local r = {}
 for _, b in pairs(self.parent.children) do
  if b ~= self then
   table.insert(r, b)
  end
 end
 return r
end

function B.ps(self)
 local r = {}
 for _, s in pairs(self.parent.children) do
  if s == self then
   break
  end
  table.insert(r, s)
 end
 return r
end

function B.gsm(self, a)
 local m = (a == H) and 'w' or 'h'
 return type(self[m]) == 'number' and FX or self[m]
end

function B.gfw(a, f)
 local i = (a == H) and {1, 3} or {0, 2}
 local w = 0
 for _, j in ipairs(i) do
  w = w + f[j + 1]
 end
 return w
end

function B.gpw(self, a)
 return self:gfw(a, self.p)
end

function B.gmw(self, a)
 return self:gfw(a, self.m)
end

function B.gbw(self, a)
 return self:gfw(a, self.b)
end

function B.gas(self, a)
 local c = self.parent:_gs(a, 3)
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

function B.gfs(self, a)
 local sm = self:gsm(a)
 local m = (a == H) and 'w' or 'h'
 if sm == FX then
  return self[m]
 elseif sm == HG then
  local hs = self:gmw(a) + self:gmw(a) + self:gpw(a)
  for _, c in pairs(self.children) do
   hs = hs + c:gfs(a)
  end
  return hs
 elseif sm == F then
  if not self.parent then
   error('No parent for FILL')
  end
  local as = self:gas(a)
  local n = 0
  for _, s in pairs(self.parent.children) do
   if s:gsm(a) == F then
    n = n + 1
   end
  end
  return math.floor(as / n)
 end
end

function B.gp(self, a, i)
 local j = (a == H) and 3 or 0
 local f = (i == 1) and self.m or (i == 2) and self.b or self.p
 local pf = f[j + 1]
 if not self.parent then
  return pf
 end
 local ps = 0
 if a == self.parent.direction then
  for _, s in pairs(self:ps()) do
   ps = ps + s:_gs(a)
  end
 end
 local pp = (self.parent.m or self.parent.b or self.parent.p)[j + 1]
 return self.parent:_gp(a) + pp + ps + pf
end

function B.gb(self, il)
 local x = self:_gp(H, il)
 local y = self:_gp(V, il)
 local w = self:_gs(H, il)
 local h = self:_gs(V, il)
 return x, y, w, h
end

function B.r(self)
 if self.bg_renderer then
  local x, y, w, h = self:gb(2)
  self.bg_renderer(self

