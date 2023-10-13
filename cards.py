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
