# title:   game title
# author:  game developers, email, etc.
# desc:    short description
# site:    website link
# license: MIT
# version: 0.1
# script:  python
from random import randint
MENU_SCR, GAME_SCR = list(range(2))

GAME_STATE = {
    'screen': MENU_SCR
}

CHARACTERS = {
  'walter-white': {
    "name": 'Walter White'
  }
}

CARDS = {
  'wellcome': {
    'text': 'Wellcome commander! Do you want me to teach the game?',
    'left': {
      'text': 'NO!',
      'signals': [
      ]
    },
    'right': {
      'text': 'Yes!',
      'signals': [
          ('set_next_card', {'card_id': 'teach_1'})
      ]
    },
  },
  'teach_1': {
    'text': 'You\'re the king of an empire.'
  }
}


class Deck:
    def __init__(self, card_ids, first_card_id):
        self.card_ids = card_ids or []
        self.index = None
        self.next_card_id = first_card_id

    def pop(self):
        if self.next_card_id:
            card = CARDS[self.next_card_id]
            self.next_card_id = None
            return card
        card = CARDS[self.card_ids[self.index]]
        del self.card_ids[self.index]
        self.index = randint(0, len(self.card_ids))
        return card

    def append(self, card_ids):
        card_ids = card_ids or []
        for card_id in card_ids:
            if card_id not in self.card_ids:
                self.card_ids.append(card_id)


class EventObserver:
    def __init__(self):
        self._registry = {}

    def register(self, event_key, func):
        if event_key not in self._registry:
            self._registry[event_key] = []
        self._registry[event_key].append(func)

    def notify(self, event_key, kwargs):
        for observer in self._registry[event_key]:
            observer(kwargs)


events = EventObserver()
deck = Deck(['wellcome'], 'wellcome')


def set_next_card(kwargs):
    deck.next_card_id = kwargs['card_id']


events.register('set_next_card', set_next_card)


card = deck.pop()


def TIC():
    global card
    cls(0)
    print(card['text'], 10, 10)
    if btnp(2):
        for event_key, kwargs in card['right']['signals']:
            events.notify(event_key, kwargs)
        card = deck.pop()
    trace(card)

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

