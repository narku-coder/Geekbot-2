import normalFunctions
import json
import pymongo

url = 'mongodb+srv://dbAdminUser:owner127@cluster1.yf6y8.mongodb.net/geekDatabase?retryWrites=true&w=majority'
myclient = pymongo.MongoClient(url)
geekData = myclient["geekDatabase"]
geekMemes = geekData["memes"]
geekMembers = geekData["members"]
geekPets = geekData["pets"]
geekInventory = geekData["inventory"]
geekBoosts = geekData["boosts"]

async def update_data(users, user):
    contains = False
    for emp in users:
        if emp['user_id'] == user.id:
            contains = True
    if contains == False:
        y = {'user_id':user.id, 'xp':0, 'level':1,
	'coin':0, 'offensive_message_count':0, 'petNum': 0}
        new_user = geekMembers.insert_one(y)
        boost_dict = {'user_id': user.id, 'double_xp': False, 'double_xp_timer': 0,
                  'double_coins': False, 'double_coins_timer': 0, 'triple_xp': False,
                  'triple_xp_timer': 0}
        new_boost = geekBoosts.insert_one(boost_dict)

async def add_experience(users, user, exp, boosts):
   doubleXp = await active_double_xp(boosts, user)
   tripleXp = await active_triple_xp(boosts, user)
   for emp in users:
       if emp['user_id'] == user.id:
           if tripleXp:
            emp['xp'] += (3*exp)
           elif doubleXp:
             emp['xp'] += (2*exp)
           else:
             emp['xp'] += exp 
       
async def level_up(users, user, channel):
    for emp in users:
       if emp['user_id'] == user.id:
         experience = emp['xp']
         level = emp['level']
         if experience > (level*100):
             await channel.send('{} has leveled up to level {}'.format(user.mention, level + 1))
             emp['level'] += 1
             emp['xp'] = 0

async def increase_count(users, user):
    for emp in users:
        if emp['user_id'] == user.id:
            emp['offensive_message_count'] += 1
        if emp['offensive_message_count'] > 5:
            await user.send("You have been kicked because you went past the tolerable limit for offensive messages.")
            await user.kick(reason="amount of offensive messages")
        if emp['offensive_message_count'] > 10:
            await user.send("You have been banned because you sent too many offensive messages.")
            await user.ban(reason="Too many offensive messages")

async def view_level(users, user, ctx):
   lvl = -1
   for emp in users:
       if emp['user_id'] == user.id:
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
   for emp in users:
     if emp['user_id'] == user.id:
       if emp['coin'] >= amount:
         canBuy = True
   return canBuy

async def add_pet(users, user, name, kind, pets):
   for emp in pets:
     if emp['user_id'] == user.id:
       emp.append({'name': name, 'type': kind, 'xp': 0, 'move': [], 'level': 0, 'health': 100})
   for emp2 in users:
     if emp2['user_id'] == user.id:
       emp2['petNum'] += 1
  
async def add_coins(users, user, amount, boosts):
   doubleCoins = await active_double_coins(boosts, user)
   for emp in users:
     if emp['user_id'] == user.id:
       if doubleCoins:
         emp['coin'] += (2*amount)
       else:
         emp['coin'] += amount

async def subtract_coins(users, user, amount):
   for emp in users:
     if emp['user_id'] == user.id:
       emp['coin'] -= amount

async def add_pet_exp(pets, user, amount):
   for emp in pets:
     if emp['user_id'] == user.id:
       emp['xp'] += amount

async def pet_level_up(pets, channel):
   moves = normalFunctions.addMoves()
   num = 0
   for emp in pets:
     if emp['xp'] > 500:
       name = emp['name']
       level = emp['level']
       newMove = moves[level]
       await channel.send('{} has leveled up to level {} and has learned {}'.format(name, level + 1, newMove))
       emp['level'] += 1
       emp['xp'] = 0
       emp['moves'].append(newMove)
       emp['health'] += 100

async def view_balance(users, user, ctx):
   balance = 0
   for emp in users:
     if emp['user_id'] == user.id:
       balance = emp['coin']
   await ctx.send(user.mention + " currently has " + str(balance) + " coins")

async def get_pets(pets, user):
   geekPets = []
   for emp in pets:
     if emp['user_id'] == user.id:
       geekPets.append(emp)
   return geekPets

async def get_profile_info(users, user):
   currLevel = 0
   numPets = 0
   balance = 0
   for emp in users:
     if emp['user_id'] == user.id:
       currLevel = emp['level']
       balance = emp['coin']
       numPets = emp['petNum']
   return currLevel, numPets, balance

async def get_pet_num(users, user):
   num = 0
   for emp in users:
     if emp['user_id'] == user.id:
       num = emp['petNum']
   return num

async def get_user_data(guild):
   if str(guild) == "Geek Culture Club":
     members = []
     for member in geekMembers.find():
       members.append(member)
   elif str(guild) == "Narku Vesuba's Bot server":
     with open('users.json', 'r') as f:
       members = json.load(f)
   return members

async def get_pet_data():
   pets = []
   for pet in geekPets.find():
     pets.append(pet)
   return pets

async def get_item_data():
   items = []
   for item in geekInventory.find():
     items.append(item)
   return items

async def update_db(users, pets):
   for user in users:
     user_query = {'user_id': user['user_id']}
     user_dict = {'xp': user['xp'], 'level': user['level'], 'coin': user['coin'],
                 'petNum': user['petNum']}
     if 'bank' in user:
       user_dict['bank'] = user['bank']
     user_updated = {"$set": user_dict}
     curMember = geekMembers.update_one(user_query, user_updated)
   for pet in pets:
     pet_query = {'_id': pet['_id']}
     pet_dict = {"$set" : {'name': pet['name'], 'species': pet['species'], 'moves': pet['moves'],
                 'level': pet['level'], 'health': pet['health'], 'xp': pet['xp']}}
     curPet = geekPets.update_one(pet_query, pet_dict)

async def update_db_items(items):
   for item in items:
     item_query = {'_id': item['_id']}
     item_dict = {"$set": {'name': item['name'], 'amount': item['amount']}}
     curItem = geekInventory.update_one(item_query, item_dict)
    
async def has_account(users, user):
   has_bank = False
   for emp in users:
     if emp['user_id'] == user.id:
       if 'bank' in emp:
         has_bank = True
   return has_bank

async def add_account(users, user, amount):
   for emp in users:
     if emp['user_id'] == user.id:
       emp.update({'bank':amount})

async def deposit_coins(users, user, amount):
   for emp in users:
     if emp['user_id'] == user.id:
       emp['bank'] += amount

async def withdraw_coins(users, user, amount):
   for emp in users:
     if emp['user_id'] == user.id:
       emp['bank'] -= amount

async def can_withdraw(users, user, amount):
   is_possible = False
   for emp in users:
     if emp['user_id'] == user.id:
       if emp['bank'] >= amount:
         is_possible = True
   return is_possible

async def get_account_balance(users, user):
   balance = 0
   for emp in users:
     if emp['user_id'] == user.id:
       balance = emp['bank']
   return balance

async def add_interest(users):
   for emp in users:
     if 'bank' in emp:
       emp['bank'] += .05*emp['bank']
	
async def add_item(items, user, item):
   found = False
   for emp in items:
     if emp['user_id'] == user.id:
       if emp['name'] == item:
         emp['amount'] += 1
         found = True
   if not found:
     items.append({'user_id': user.id, 'name': item, 'num': 1})
             
async def get_inventory(items, user):
   has_items = False
   items = []
   usable_items = []
   for emp in items:
     if emp['user_id'] == user.id:
       items.append(emp)
       has_items = True
   if has_items:
     for thing in items:
       if thing['amount'] > 0:
         usable_items.append(thing)
   return has_items, usable_items

async def activate_boost(boosts, user, num):
   for emp in boosts:
     if emp['user_id'] == user.id:
       if int(num) == 0:
         emp['boosts'][0]['doubleXp'] = True
         emp['boosts'][0]['cooldown'] = 14400
       elif int(num) == 1:
         emp['boosts'][1]['doubleCoins'] = True
         emp['boosts'][1]['cooldown'] = 14400
       elif int(num) == 2:
         emp['boosts'][2]['tripleXp'] = True
         emp['boosts'][2]['cooldown'] = 14400

async def active_double_coins(boosts, user):
   is_active = False
   for emp in boosts:
     if emp['user_id'] == user.id:
         is_active = emp['double_coins']
   return is_active

async def active_double_xp(boosts, user):
   is_active = False
   for emp in boosts:
     if emp['user_id'] == user.id:
        is_active = emp['double_xp']     
   return is_active

async def active_triple_xp(boosts, user):
   is_active = False
   for emp in boosts:
     if emp['user_id'] == user.id:
         is_active = emp['triple_xp']
   return is_active

async def decrease_item_count(users, user, item):
   for emp in users:
     if emp['user id'] == user.id:
       for thing in emp['inventory']:
         if thing['name'] == item:
           thing['num'] -= 1

async def reset_cooldown(users):
   for emp in users:
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
