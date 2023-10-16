import glob
import yaml
from os.path import basename, splitext
from random import randint
import os

CARDS = {}
for file_path in glob.glob('cards/*.yaml'):
    with open(file_path) as file:
        key = splitext(basename(file_path))[0]
        data = yaml.safe_load(file)
        data['key'] = key
        CARDS[key] = data


class Deck:
    def __init__(self, first_card_id):
        self.card_ids = []
        self.index = None
        self.next_card_id = first_card_id

    def pop(self):
        if not self.next_card_id and not self.card_ids:
            raise ValueError('No cards in the deck')
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


def print_msg_box(msg, indent=1, width=None, title=None):
    """Print message-box with optional title."""
    lines = msg.split('\n')
    space = " " * indent
    if not width:
        width = max(map(len, lines))
    box = f'╔{"═" * (width + indent * 2)}╗\n'  # upper_border
    if title:
        box += f'║{space}{title:<{width}}{space}║\n'  # title
        box += f'║{space}{"-" * len(title):<{width}}{space}║\n'  # underscore
    box += ''.join([f'║{space}{line:<{width}}{space}║\n' for line in lines])
    box += f'╚{"═" * (width + indent * 2)}╝'  # lower_border
    print(box)


def print_card(card):
    print_msg_box(card['text'], title=card['key'].upper())
    print('1)', card['left']['label'] if 'label' in card['left'] else 'No!')
    print('2)', card['right']['label'] if 'label' in card['right'] else 'Yes!')


def parse_signal(lst):
    method_name = lst[0]
    args = lst[1] if len(lst) > 1 else []
    kwargs = lst[2] if len(lst) > 2 else {}
    return method_name, args, kwargs


deck = Deck('wellcome')


class HealthIndicator:
    def __init__(self):
        self.is_blinking = False


health_indicator = HealthIndicator()


def set_next_card(card_id):
    deck.next_card_id = card_id


def set_obj_attr(*names, **values):
    for name in names:
        obj = globals()[name]
        for key, value in values.items():
            setattr(obj, key, value)


inp = None


def signal_callback(signal):
    method, args, kwargs = parse_signal(signal)
    print('Method:', method, 'Args:', args, 'Kwargs:', kwargs)
    globals()[method](*args, **kwargs)


def print_indicators():
    print_msg_box('health: 12/4 charm: 4/12 army:8/12 religion: 12/12')


card = deck.pop()
while inp != 'q':
    os.system('clear')
    print_indicators()
    print_card(card)
    inp = input()
    key = {'1': 'left', '2': 'right'}[inp]
    if not key:
        continue
    for signal in card[key].get('emit', []):
        signal_callback(signal)
    if 'both' in card:
        for signal in card['both'].get('emit', []):
            signal_callback(signal)
    card = deck.pop()
