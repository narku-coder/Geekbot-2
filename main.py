import requests
import os
import random
import functions
import normalFunctions
import pymongo

from keep_alive import keep_alive
from discord.ext import commands, tasks

url = 'mongodb+srv://dbAdminUser:owner127@cluster1.yf6y8.mongodb.net/geekDatabase?retryWrites=true&w=majority'
myclient = pymongo.MongoClient(url)
geekData = myclient["geekDatabase"]
geekMemes = geekData["memes"]
geekMembers = geekData["members"]
geekEncouragements = geekData["encouragements"]

sad_words = ["sad", "depressed", "unhappy", "angry", "miserable", "sucks", "shitty", "shit", "anxious", "worried", "stressed", "despondent", "hopeless",
            "scared", "afraid"]
deleted_messages = []
client = commands.Bot(command_prefix='!')
earnCoins = True

def generate_coin_word():
  animals_list = open('./textFiles/animals.txt', 'r')
  content = animals_list.read()
  animals = content.split('\n')
  animals_list.close()
  randNum = random.randint(0, (len(animals)-1))
  coin_word = animals[randNum]
  return coin_word

@client.command()
async def load(ctx, extension):
  client.load_extension(f'cogs.{extension}')

@client.command()
async def unload(ctx, extension):
  client.unload_extension(f'cogs.{extension}')
 
for file in os.listdir('./cogs'):
  if file.endswith('.py'):
    client.load_extension(f'cogs.{file[:-3]}')

coin_word = ['owl']
@tasks.loop(hours=5)
async def coin_message_sender():
  print("Message is sending")
  if client.is_ready():
    print("Client is ready.")
    coin_word[0] = generate_coin_word()
    print("spec word - " + coin_word[0])
    channel = client.get_channel(800835935490539541)
    await channel.send("Here is an opportunity to earn 100 coins. The first person to type a message with this animal - " + str(coin_word[0]) + " - will earn 100 coins.")
    earnCoins = True
    print("earnCoins at message sent - " + str(earnCoins))
#Bot event functions

@client.event
async def on_message(message):
  if message.author == client.user:
    return
  
  guild = message.guild
  user = message.author
  msg = message.content
  chan = client.get_channel(800835935490539541)
  await client.process_commands(message)
  pets = await functions.get_pet_data()
  boosts = await functions.get_boosts_data()
           
  global earnCoins
  print("earnNum - " + str(earnCoins))
  print("msg - " + msg)
  print("coin word - " + str(coin_word[0]))
  lowMsg = msg.lower()
  if coin_word[0] in lowMsg and earnCoins == True:
    await message.channel.send("Congratulations " + message.author.mention + ". You have earned 100 coins for being the first person to type a message containing " + str(coin_word[0]) + ".")
    print("earnNum in if - " + str(earnCoins))
    print("coin message author - " + message.author.name)
    members = await functions.get_user_data(guild)
    await functions.add_coins(members, user, 100, boosts)
    await functions.update_db(members, pets, boosts)
    earnCoins = False
    await message.channel.send("This event has ended.")
  
  options = []
  for message in geekEncouragements.find():
    options.append(message['message'])
  if any(word in msg for word in sad_words):
    await message.channel.send(random.choice(options))

  members = await functions.get_user_data(guild)
  await functions.update_data(members, user)
  members = await functions.get_user_data(guild)
  await functions.add_experience(members, user, 10, boosts)
  members = await functions.get_user_data(guild)
  await functions.add_coins(members, user, 10, boosts)
  members = await functions.get_user_data(guild)
  await functions.level_up(members, user, chan)
  await functions.update_db(members, pets, boosts)
  members = await functions.get_user_data(guild)
  petNum = await functions.get_pet_num(members, user)
  if petNum > 0:
    await functions.add_pet_exp(pets, user, 25)
    await functions.update_db(members, pets, boosts)
    await functions.pet_level_up(pets, chan)
    await functions.update_db(members, pets, boosts)
  
@client.event
async def on_member_join(member):
  guild = client.get_guild()
  if str(guild) == "Geek Culture Club":
    await member.send("Welcome to the " + str(guild) + ". The best server in Discord.")
    channel = client.get_channel(743572677285117982)
    await channel.send(member.mention + " has joined the " + str(guild) + " server")
  else:
    await member.send("Welcome to the " + str(guild) + ". The best server in Discord.")
  members = await functions.get_user_data(guild)
  pets = await functions.get_pet_data()
  boosts = await functions.get_boosts_data()
  await functions.update_data(members, member)
  await functions.update_db(members, pets, boosts)

@tasks.loop(hours=8)
async def interest_gainer():
   print("Interest is generating.")
   guilds = client.guilds
   num = 0
   while num < len(guilds):
     print("Inside the interest while loop")
     guild = guilds[num]
     pets = await functions.get_pet_data()
     members = await functions.get_user_data(guild)
     boosts = await functions.get_boosts_data()
     await functions.add_interest(members)
     await functions.update_db(members, pets, boosts)
     num = num + 1

@tasks.loop(minutes=1)
async def lower_cooldown():
  guilds = client.guilds
  num = 0
  while num < len(guilds):
    guild = guilds[num]
    members = await functions.get_user_data(guild)
    pets = await functions.get_pet_data()
    boosts = await functions.get_boosts_data()
    await functions.reset_cooldown(boosts)
    await functions.update_db(members, pets, boosts)
    num = num + 1

def addMemesToDB():
  url = "https://meme-api.herokuapp.com/gimme/50"
  response = requests.request("GET", url)
  info = response.json()
  memes = info['memes']
  num = 0
  while num < 50:
    normalFunctions.update_meme_list(memes[num]["url"])
    num = num + 1

#addMemesToDB()
#addMemesToDB()
interest_gainer.start()
coin_message_sender.start()
lower_cooldown.start()
client.run(os.getenv('DISCORD_TOKEN'))
