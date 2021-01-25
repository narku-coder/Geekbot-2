import random

from replit import db

def update_encouragements(encouraging_message):
  if "encouragements" in db.keys():
    encouragements = db["encouragements"]
    encouragements.append(encouraging_message)
    db["encouragements"] = encouragements
  else:
    db["encouragements"] = [encouraging_message]

def delete_encouragment(index):
  encouragements = db["encouragements"]
  if len(encouragements) > index:
    del encouragements[index]
  db["encouragements"] = encouragements

def verify(message, word):
  guess = message.content
  print("verify guess - " + guess)
  if guess.lower() in word:
    return True
  else:
    return False

def fill_mystery(message, word, mystery):
  pos = []
  num = 0
  guess = message.content
  while num < len(word):
    if word[num] == guess.lower():
      pos.append(num)
    num = num + 1 
  size = len(pos)
  num = 0
  while num < size:
    num_two = pos[num]
    mystery = mystery[:(num_two)] + guess.lower() + mystery[(num_two+1):] 
    num = num + 1
  print("mystery - " + mystery)
  return mystery

def update_pun_list(new_pun):
  if "puns" in db.keys():
    puns = db["puns"]
    puns.append(new_pun)
    db["puns"] = puns
  else:
    db["puns"] = [new_pun]

def addMoves():
  moves = []
  move_set = open('./textFiles/moves.txt', 'r')
  content = move_set.read()
  moves = content.split('\n')
  move_set.close()
  return moves

def getDailyWord():
  words = []
  word_set = open('./textFiles/animals.txt', 'r')
  content = word_set.read()
  words = content.split('\n')
  word_set.close()
  max = len(words)
  randNum = random.randint(0, (max-1))
  daily_word = words[randNum]
  return daily_word

def update_meme_list(new_url):
  if "memes" in db.keys():
    memes = db["memes"]
    memes.append(new_url)
    db["memes"] = memes
  else:
    db["memes"] = [new_url]
