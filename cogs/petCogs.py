import functions
import discord
import random

from discord.ext import commands

pets = []
items = []
def fillPetsList():
    pets_list = open('./textFiles/pets.txt', 'r')
    content = pets_list.read()
    pets = content.split('\n')
    pets_list.close()
    return pets

def fillItemsList():
    items_list = open('./textFiles/items.txt', 'r')
    content = items_list.read()
    items = content.split('\n')
    items_list.close()
    return items

class petCog(commands.Cog):
  def __init__(self, bot):
        self.bot = bot

  @commands.command()
  async def pet(self, ctx):
    embed = discord.Embed(title="Pet Commands", description = "A list of commands to provide various info", color = discord.Colour.green())
    embed.add_field(name = "Buy a new pet", value = "!buy pet", inline = True)
    embed.add_field(name = "To battle another member's pets", value = "!fight <User>", inline = True)
    embed.add_field(name = "View profiles of your pets", value = "!petinfo", inline = True)
    await ctx.send(embed=embed)
  
  @commands.command()
  async def buy(self, ctx, *, arg):
    guild = ctx.guild
    users = await functions.get_user_data(guild)
    pets = await functions.get_pet_data()
    items = await functions.get_item_data()
    boosts = await functions.get_boosts_data()
    member = ctx.author
    petsList = fillPetsList()
    itemsList = fillItemsList()
    pet_display = []
    item_display = []
    num = 0
    while num < len(petsList):
      line = str((num + 1)) + " - " + petsList[num]
      pet_display.append(line)
      num = num + 1
    num2 = 0
    while num2 < len(itemsList):
      line = str((num2 + 1)) + " - " + itemsList[num2]
      item_display.append(line)
      num2 = num2 + 1
    canBuy = False
    kind = ''
    name = ''
    if arg == "pet":
      canBuy = await functions.can_buy(users, member, 1000)
      if(canBuy):
        await functions.subtract_coins(users, member, 1000)
        print("after 1000 subtract coin")
        await functions.update_db(users, pets, boosts)
        await ctx.send("Choose one from the available options." + str(pet_display) + " Type the number for the pet you want to own.")
        def check(msg):
          return msg.author == ctx.author and msg.content.isnumeric()
        msg = await self.bot.wait_for("message", check = check)
        index = int(msg.content)
        while index > len(petsList):
          await ctx.send(str(index) + " is not a valid option. Try again")
          await ctx.send(str(pet_display) + " Type the number for the item you want to buy.")
          msg = await self.bot.wait_for("message", check = check)
          index = int(msg.content)
        kind = petsList[(index-1)]
        await ctx.send("What name do you want to give your pet?")
        def checkTwo(msg):
          return msg.author == ctx.author
        msg = await self.bot.wait_for("message", check = checkTwo)
        name = msg.content
        users = await functions.get_user_data(guild)
        await functions.add_pet(users, member, name, kind, pets)
        await functions.update_db(users, pets, boosts)
        await ctx.send("Congratulations on your new pet " + name + " the " + kind + ". I wish y'all lots of fun and happy time together")
    elif arg == "item":
      await ctx.send(str(item_display) + " Type the number for the item you want to buy.")
      def check(msg):
        return msg.author == ctx.author and msg.content.isnumeric()
      msg = await self.bot.wait_for("message", check = check)
      index = int(msg.content)
      while index > len(items):
          await ctx.send(str(index) + " is not a valid option. Try again")
          await ctx.send(str(item_display) + " Type the number for the item you want to buy.")
          msg = await self.bot.wait_for("message", check = check)
          index = int(msg.content)
      chosenItem = itemsList[(index-1)]
      item_splits = chosenItem.split(" ")
      itemName = item_splits[0]
      itemPrice = item_splits[1]
      canBuy = await functions.can_buy(users, member, int(itemPrice))
      if canBuy:
        await functions.subtract_coins(users, member, int(itemPrice))
        print("after item price subtract coin")
        await functions.update_db(users, pets, boosts)
        users = await functions.get_user_data(guild)
        print("before add item")
        await functions.add_item(items, member, itemName)
        print("after add item")
        await functions.update_db_items(items)
        await ctx.send(itemName + " has been added to your inventory")
      else:
        await ctx.send("You don't have enough coins to purchase a " + itemName)
    elif arg == 'menu':
      embed = discord.Embed(title="Shop commands", description = "A list of available shop commands", color = discord.Colour.blue())
      embed.add_field(name = "Purchase a pet for 1000 coins", value = "#buy pet", inline = True)
      embed.add_field(name = "Purchase an item from the item shop", value = "#buy item", inline = True)
      await ctx.send(embed=embed)

  @commands.command()
  async def fight(self,ctx, user: discord.User):
    guild = ctx.guild
    users = await functions.get_user_data(guild)
    player1 = ctx.author
    player1_moves = []
    player1_moves_display = []
    player1_pets = await functions.get_pets(users, player1)
    player1_pets_display = []
    num = 0
    while num < len(player1_pets):
      line = str(num+1) + " - " + player1_pets[num]["name"]
      player1_pets_display.append(line)
      num = num + 1
    player2 = user
    player2_moves = []
    player2_moves_display = []
    player2_pets = await functions.get_pets(users, player2)
    player2_pets_display = []
    num2 = 0
    while num2 < len(player2_pets):
      line = str(num2+1) + " - " + player2_pets[num2]["name"]
      player2_pets_display.append(line)
      num = num2 + 1
    playerTurn = 0
    fighting = True
    await player2.send("You have been challenged to a fight by " + ctx.author.mention + ". Do you accept? Type y or yes to accept.")
    def check(msg):
      return msg.author == player2
    msg = await self.bot.wait_for("message", check = check)
    resp = msg.content
    if resp.lower() == "y" or resp.lower() == "yes":
      pet1 = ""
      pet2 = ""
      pet1_health = 0
      pet2_health = 0
      await ctx.send("Let's get ready to rumble\n\n " + player1.mention + "choose your pet: " + str(player1_pets_display))
      def checkTwo(msg):
        return msg.author == player1 and msg.isnumeric()
      msg = await self.bot.wait_for("message", check = checkTwo)
      choice = msg.content
      if choice > len(player1_pets):
        await ctx.send("Your choice is invalid try again")
      else:
        pet1 = player1_pets[(choice-1)]
        pet1_health = pet1['health']
      await ctx.send(player2.mention + "choose your pet: " + str(player2_pets_display))
      def checkThree(msg):
        return msg.author == player2 and msg.isnumeric()
      msg = await self.bot.wait_for("message", check = checkThree)
      choice = msg.content
      if choice > len(player2_pets):
        await ctx.send("Your choice is invalid try again")
      else:
        pet2 = player2_pets[(choice-1)]
        pet2_health = pet2['health']
      num3 = 0
      player1_moves = pet1["moves"]
      while num3 < len(player1_moves):
        line = str(num3+1) + " - " + player1_moves[num3]
        player1_moves_display.append(line)
        num3 = num3 + 1
      await player1.send(pet1["name"] + "'s move set: " + str(player1_moves_display))
      num4 = 0
      player2_moves = pet2["moves"]
      while num4 < len(player2_moves):
        line = str(num4+1) + " - " + player2_moves[num4]
        player2_moves_display.append(line)
        num4 = num4 + 1
      await player1.send(pet2["name"] + "'s move set: " + str(player2_moves_display))
      while fighting:
        if playerTurn == 0:
          await ctx.send(player1.mention + " select your attack")
          msg = await self.bot.wait_for("message", check = checkTwo)
          choice = msg.content
          if choice > len(player1_moves):
            await ctx.send("Your choice is invalid try again")
          else:
            damage = random.randint(0, 20) * int(choice)
            pet2_health = pet2_health - damage
            await ctx.send(pet1['name'] + " inflicted " + str(damage) + " damage with " + player1_moves[(choice-1)] + "\n\n " + pet2['name'] + "'s health: " + str(pet2_health))
            playerTurn = 1
        if playerTurn == 1:
          await ctx.send(player2.mention + " select your attack")
          msg = await self.bot.wait_for("message", check = checkThree)
          choice = msg.content
          if choice > len(player2_moves):
            await ctx.send("Your choice is invalid try again")
          else:
            damage = random.randint(0, 20) * int(choice)
            pet1_health = pet1_health - damage
            await ctx.send(pet2['name'] + " inflicted " + str(damage) + " damage with " + player2_moves[(choice-1)] + "\n\n " + pet1['name'] + "'s health: " + str(pet2_health))
            playerTurn = 0
        if pet1_health <= 0 or pet2_health <= 0:
          fighting = False
          if pet1_health <= 0:
            await ctx.send(pet1['name'] + " has been defeated. Congratulations " + player2.mention + " is the winner. You just won 100 coins")
            members = await functions.get_user_data(guild)
            await functions.add_coins(members, player2, 100)
            await functions.update_file(guild, members)
          if pet2_health <= 0:
            await ctx.send(pet2['name'] + " has been defeated. Congratulations " + player1.mention + " is the winner. You just won 100 coins")
            members = await functions.get_user_data(guild)
            await functions.add_coins(members, player1, 100)
            await functions.update_file(guild, members)        
    else:
      await ctx.send(player2.mention + " has declined your challenge.")

  @commands.command()
  async def petinfo(self, ctx):
     print("It got to the petinfo function.")
     guild = ctx.guild
     users = await functions.get_user_data(guild)
     member = ctx.author
     pets = await functions.get_pet_data()
     petNum = await functions.get_pet_num(users, member)
     if petNum == 0:
       await ctx.send("You currently own no pets")
     else:
       user_pets = await functions.get_pets(pets, member)
       print("It obtained the list of pets")
       user_pets_display = []
       num = 0
       while num < len(user_pets):
         line = str(num+1) + " - " + user_pets[num]['name']
         user_pets_display.append(line)
         num = num + 1
       await ctx.send("choose a pet to view its profile: " + str(user_pets_display))
       def checkTwo(msg):
         return msg.author == ctx.author and msg.content.isnumeric()
       msg = await self.bot.wait_for("message", check = checkTwo)
       choice = int(msg.content)
       if choice > len(user_pets):
         await ctx.send("Your choice is invalid try again")
       else:
         currPet = user_pets[(choice-1)]
         petHealth = currPet['health']
         petLevel = currPet['level']
         petName = currPet['name']
         petMoves = currPet['moves']
         embed = discord.Embed(title="Current Pet Profile", description = "The profile of your selected pet", color = discord.Colour.gold())
         embed.add_field(name = "Pet's name: ", value = petName, inline = True)
         embed.add_field(name = "Pet's level: ", value = str(petLevel), inline = True)
         embed.add_field(name = "Pet's health: ", value = str(petHealth), inline = True)
         embed.add_field(name = "Pet's move set: ", value = str(petMoves), inline = True)
         embed.set_footer(text = petName + "'s profile'")
         await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(petCog(bot))
