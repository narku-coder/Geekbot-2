import random
import pymongo
import json

url = 'mongodb+srv://dbAdminUser:owner127@cluster1.yf6y8.mongodb.net/geekDatabase?retryWrites=true&w=majority'
myclient = pymongo.MongoClient(url)
geekData = myclient["geekDatabase"]
geekMemes = geekData["memes"]
geekEncouragements = geekData["encouragements"]
geekPuns = geekData["puns"]

def update_encouragements(encouraging_message):
  message_dict = {'message': encouraging_message}
  newMessage = geekEncouragements.insert_one(message_dict)
  print("new message added.")

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
  pun_dict = {'text': str(new_pun)}
  newPun = geekPuns.insert_one(pun_dict)
  print("new pun added.")

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
  meme_dict = {'url': new_url}
  newMeme = geekMemes.insert_one(meme_dict)
  
def get_total_exp(lvl, exp):
  num = lvl-1
  total = 0
  while num > 0:
    total += num*100
    num = num - 1
  total += exp
  return total
