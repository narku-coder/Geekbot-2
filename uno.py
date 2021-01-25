import random

def buildDeck():
  deck = []
  colors = ["Red", "Blue", "Yellow", "Green"]
  values = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, "Skip", "Draw Two", "Reverse"]
  wilds = ["Wild", "Wild Draw Four"]
  for color in colors:
    for val in values:
      cardVal = "{} {}".format(color, val)
      deck.append(cardVal)
      if val != 0:
        deck.append(cardVal)
  for i in range(4):
    deck.append(wilds[0])
    deck.append(wilds[1])
  return deck

def shuffleDeck(deck, size):
  for cardPos in range(len(deck)):
    randPos = random.randint(0,(size-1))
    deck[cardPos], deck[randPos] = deck[randPos], deck[cardPos]
  return deck

def drawCards(num, deck):
  cardsDrawn = []
  for x in range(num):
    cardsDrawn.append(deck.pop(0))
  return cardsDrawn