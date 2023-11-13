-- title:   game title
-- author:  game developer, email, etc.
-- desc:    short description
-- site:    website link
-- license: MIT License (change this to your license of choice)
-- version: 0.1
-- script:  lua
SW = 240
SH = 136
MENU, GAME, SETTINGS, OVER =
  'M', 'G', 'S', 'O'
GAME_SCREEN = MENU

MENU_SCREEN = {
  ['bgc'] = 0, -- Background color
  ['options'] = {'START', 'OPTIONS',
                 'EXIT'},
  ['selected'] = 1,
  ['ic'] = 4, -- Item color
  ['sic'] = 5 -- Selected item color
}

function MENU_SCREEN:update()
  if btnp(0) then
    self.selected = self.selected - 1
  end
  if btnp(1) then
    self.selected = self.selected + 1
  end
  if btnp(2) then
    GAME_SCREEN = SETTINGS_SCREEN
  end
  self.selected = self.selected % 4
end

function MENU_SCREEN:draw()
  rect(0, 0, SW, SH, self.bgc)
  for i, o in ipairs(self.options) do
    local ow = print(o, 320, 0)
    local x = (SW / 2) - (ow / 2)
    local c
    local yo = 0
    if i == self.selected then
      c = self.sic
      yo = 1
    else
      c = self.ic
    end
    print(o, x, (i*20) + 1, 0)
    print(o, x, (i*20) + yo , c)
  end
end

function MENU_SCREEN:tic()
  self:update()
  self:draw()
end

SETTINGS_SCREEN = {
  ['bgc'] = 9,
}

function SETTINGS_SCREEN:update()
end

function SETTINGS_SCREEN:draw()
  rect(0, 0, SW, SH, self.bgc)
end

function SETTINGS_SCREEN:tic()
  SETTINGS_SCREEN:update()
  SETTINGS_SCREEN:draw()
end

function TIC()
  if GAME_SCREEN == MENU then
    MENU_SCREEN:tic()
  elseif GAME_SCREEN == SETTINGS_SCREEN then
    SETTINGS_SCREEN:tic()
  end
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

