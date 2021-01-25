
def buildDeck():
  deck = []
  suits = ["Diamond", "Clubs", "Hearts", "Spades"]
  ranks = ["Ace", "2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King"]
  for suit in suits:
    for rank in ranks:
      cardVal = "{} {}".format(suit, rank)
      deck.append(cardVal)
  return deck

def verifyRequest(rank, hand):
  verified = False
  for card in hand:
    card_splits = card.split(" ")
    if card_splits[1].lower() == rank.lower():
      verified = True
      break
  return verified

def printHand(hand):
  display = []
  num = 1
  for card in hand:
    card2 = str(num) + " - " + str(card)
    display.append(card2)
    num = num + 1
  return display

def canMakeSet(hand):
  ranks = ["Ace", "2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King"]
  chosenRank = ""
  num = 0
  for rank in ranks:
    for card in hand:
      card_splits = card.split(" ")
      currRank = card_splits[1]
      if currRank.lower() == rank.lower():
        num = num + 1
    if num >= 4:
      canMake = True
      chosenRank = rank
      break
  canMake = False
  return canMake, chosenRank

def makeSet(hand, rank):
  hand2 = hand
  removedCards = []
  for card in hand:
    card_splits = card.split(" ")
    if card_splits[1] == rank:
      removedCards.append(card)
  num = 0
  while num < 4:
    hand2.remove(removedCards[num])
    num = num + 1
  return hand2