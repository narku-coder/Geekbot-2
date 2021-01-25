import normalFunctions
import json

async def update_data(users, user):
  contains = False
  for emp in users['users']:
	  if emp['user id'] == user.id:
		  contains = True

  if contains == False:
	  y = {'user id':user.id, 'xp':0, 'level':1,
		'coin':0, 'offensive_message_count':0, 'pets':[], 'petNum': 0}
	  users['users'].append(y)

async def add_experience(users, user, exp):
  doubleXp = await active_double_xp(users, user)
  tripleXp = await active_triple_xp(users, user)
  for emp in users['users']:
    if emp['user id'] == user.id:
      if tripleXp:
        emp['xp'] += (3*exp)
      elif doubleXp:
	      emp['xp'] += (2*exp)
      else:
        emp['xp'] += exp

async def level_up(users, user, channel):
  for emp in users['users']:
    if emp['user id'] == user.id:
      experience = emp['xp']
      level = emp['level']
      if experience > (level*100):
        await channel.send('{} has leveled up to level {}'.format(user.mention, level + 1))
        emp['level'] += 1
        emp['xp'] = 0

async def increase_count(users, user):
  for emp in users['users']:
    if emp['user id'] == user.id:
	    emp['offensive_message_count'] += 1
    if emp['offensive_message_count'] > 5:
      await user.send("You have been kicked because you went past the tolerable limit for offensive messages.")
      await user.kick(reason="amount of offensive messages")
    if emp['offensive_message_count'] > 10:
      await user.send("You have been banned because you sent too many offensive messages.")
      await user.ban(reason="Too many offensive messages")

async def view_level(users, user, ctx):
  lvl = -1
  for emp in users['users']:
    if emp['user id'] == user.id:
	    lvl = emp['level']
  await ctx.send(user.mention + " is at level " + str(lvl))

async def check_answer(message, ctx, answer, choices):
  letters = ["A", "B", "C", "D"]
  num = 0
  correct_letter = ""
  while num < 4:
    if answer == choices[num]:
      correct_letter = letters[num]
      break
    num = num + 1;
  if message.content.upper() == correct_letter:
    return True
  else:
    return False

async def can_buy(users, user, amount):
  canBuy = False
  for emp in users['users']:
    if emp['user id'] == user.id:
      if emp['coin'] >= amount:
        canBuy = True
  return canBuy

async def add_pet(users, user, name, kind):
  for emp in users['users']:
    if emp['user id'] == user.id:
      emp['pets'].append({"name": name, "type": kind, "xp": 0, "moves": [], "level": 0, "health": 100})
      emp['petNum'] += 1
  
async def add_coins(users, user, amount):
  doubleCoins = await active_double_coins(users, user)
  for emp in users['users']:
    if emp['user id'] == user.id:
      if doubleCoins:
        emp['coin'] += (2*amount)
      else:
        emp['coin'] += amount

async def subtract_coins(users, user, amount):
  for emp in users['users']:
    if emp['user id'] == user.id:
      emp['coin'] -= amount

async def add_pet_exp(users, user, amount):
  for emp in users['users']:
    if emp['user id'] == user.id:
      num = emp['petNum']
      num2 = 0
      while num2 < num:
        emp['pets'][num2]['xp'] += amount
        num2 = num2 + 1

async def pet_level_up(users, user, channel):
  moves = normalFunctions.addMoves()
  num2 = 0
  for emp in users['users']:
    if emp['user id'] == user.id:
      num = emp['petNum']
      while num2 < num:
        if emp['pets'][num2]['xp'] > 500: 
          name = emp['pets'][num2]['name']
          level = emp['pets'][num2]['level']
          newMove = moves[level]
          await channel.send('{} has leveled up to level {} and has learned {}'.format(name, level + 1, newMove))
          emp['pets'][num2]['level'] += 1
          emp['pets'][num2]['xp'] = 0
          emp['pets'][num2]['moves'].append(newMove)
          emp['pets'][num2]['health'] += 100
        num2 = num2 + 1

async def view_balance(users, user, ctx):
  balance = 0
  for emp in users['users']:
    if emp['user id'] == user.id:
	    balance = emp['coin']
  await ctx.send(user.mention + " currently has " + str(balance) + " coins")

async def get_pets(users, user):
  pets = []
  for emp in users['users']:
    if emp['user id'] == user.id:
      pets = emp['pets']
  return pets

async def get_profile_info(users, user):
  currLevel = 0
  numPets = 0
  balance = 0
  for emp in users['users']:
    if emp['user id'] == user.id:
      currLevel = emp['level']
      balance = emp['coin']
      numPets = emp['petNum']
  return currLevel, numPets, balance

async def get_pet_num(users, user):
  num = 0
  for emp in users['users']:
    if emp['user id'] == user.id:
      num = emp['petNum']
  return num

async def get_user_data(guild):
  if str(guild) == "Geek Culture Club":
    with open('geeks.json', 'r') as f:
      members = json.load(f)
  elif str(guild) == "Narku Vesuba's Bot server":
    with open('users.json', 'r') as f:
      members = json.load(f)
  return members

async def update_file(guild, users):
  if str(guild) == "Geek Culture Club":
    with open('geeks.json', 'w') as f:
      json.dump(users, f)
  elif str(guild) == "Narku Vesuba's Bot server":
    with open('users.json', 'w') as f:
      json.dump(users, f)

async def has_account(users, user):
  has_bank = False
  for emp in users['users']:
    if emp['user id'] == user.id:
      if 'bank' in emp:
        has_bank = True
  return has_bank

async def add_account(users, user, amount):
  for emp in users['users']:
    if emp['user id'] == user.id:
      emp.update({'bank':amount})

async def deposit_coins(users, user, amount):
  for emp in users['users']:
    if emp['user id'] == user.id:
      emp['bank'] += amount

async def withdraw_coins(users, user, amount):
  for emp in users['users']:
    if emp['user id'] == user.id:
      emp['bank'] -= amount

async def can_withdraw(users, user, amount):
  is_possible = False
  for emp in users['users']:
    if emp['user id'] == user.id:
      if emp['bank'] >= amount:
        is_possible = True
  return is_possible

async def get_account_balance(users, user):
  balance = 0
  for emp in users['users']:
    if emp['user id'] == user.id:
      balance = emp['bank']
  return balance

async def add_interest(users):
  for emp in users['users']:
    if 'bank' in emp:
      emp['bank'] += .05*emp['bank']

async def add_item(users, user, item):
  items = []
  found = False
  for emp in users['users']:
    if emp['user id'] == user.id:
      if 'inventory' in emp:
        items = emp['inventory']
        for thing in items:
          if thing['name'] == item:
            thing['num'] += 1
            found = True
        if not found:
          items.append({'name': item, 'num': 1})
      else:
        emp.update({'inventory': [{'name': item, 'num': 1}], 'boosts':[{'doubleXp': False, 'cooldown':0}, {'doubleCoins': False, 'cooldown':0},  {'tripleXp': False, 'cooldown':0}]})

async def get_inventory(users, user):
  has_items = False
  items = []
  usable_items = []
  for emp in users['users']:
    if emp['user id'] == user.id:
      if 'inventory' in emp:
        has_items = True
        items = emp['inventory']
  if has_items:
    for thing in items:
      if thing['num'] > 0:
        usable_items.append(thing)
  return has_items, usable_items

async def activate_boost(users, user, num):
  for emp in users['users']:
    if emp['user id'] == user.id:
      print("boosts - " + str(emp['boosts']))
      if int(num) == 0:
        emp['boosts'][0]['doubleXp'] = True
        emp['boosts'][0]['cooldown'] = 14400
      elif int(num) == 1:
        emp['boosts'][1]['doubleCoins'] = True
        emp['boosts'][1]['cooldown'] = 14400
      elif int(num) == 2:
        emp['boosts'][2]['tripleXp'] = True
        emp['boosts'][2]['cooldown'] = 14400

async def active_double_coins(users, user):
  is_active = False
  for emp in users['users']:
    if emp['user id'] == user.id:
      if 'boosts' in emp:
        is_active = emp['boosts'][1]['doubleCoins']
  return is_active

async def active_double_xp(users, user):
  is_active = False
  for emp in users['users']:
    if emp['user id'] == user.id:
      if 'boosts' in emp:
        is_active = emp['boosts'][0]['doubleXp']
       
  return is_active

async def active_triple_xp(users, user):
  is_active = False
  for emp in users['users']:
    if emp['user id'] == user.id:
      if 'boosts' in emp:
        is_active = emp['boosts'][2]['tripleXp']
  return is_active

async def decrease_item_count(users, user, item):
  for emp in users['users']:
    if emp['user id'] == user.id:
      for thing in emp['inventory']:
        if thing['name'] == item:
          thing['num'] -= 1

async def reset_cooldown(users):
  for emp in users['users']:
    if 'boosts' in emp:
      num = 0
      while num < 3:
        if emp['boosts'][num]['cooldown'] > 0:
           emp['boosts'][num]['cooldown'] -= 60
           if emp['boosts'][num]['cooldown'] == 0:
              if num == 0:
                emp['boosts'][num]['doubleXp'] = False
              elif num == 1:
                emp['boosts'][num]['doubleCoins'] = False
              elif num == 2:
                emp['boosts'][num]['tripleXp'] = False
        num = num + 1

    