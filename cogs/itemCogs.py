import discord
import functions
import random

from discord.ext import commands

class itemCog(commands.Cog):
  def __init__(self, bot):
        self.bot = bot

  @commands.command()
  async def items(self, ctx):
    embed = discord.Embed(title="List of items", description = "A list of available items and its ability", color = discord.Colour.blue())
    embed.add_field(name = "Add coins to your wallet", value = "soda", inline = True)
    embed.add_field(name = "Gives xp", value = "cookie", inline = True)
    embed.add_field(name = "Doubles the amount of xp you earn for 4 hours", value = "brownies", inline = True)
    embed.add_field(name = "Doubles the amount of coins you earn for 4 hours", value = "pizza", inline = True)
    embed.add_field(name = "Triples the amount of xp you earn for 4 hours", value = "cake", inline = True)
    embed.set_footer(text = "Items list")
    await ctx.send(embed=embed)

  @commands.command()
  async def eat(self, ctx):
    guild = ctx.guild
    users = await functions.get_user_data(guild)
    member = ctx.author
    items = ['cookie','soda', 'brownies', 'pizza', 'cake']
    user_items = []
    has_items = False
    has_items, user_items = await functions.get_inventory(users, member)
    item_display = []
    if has_items:
      num = 0
      while num < len(user_items):
        line = str((num + 1)) + " - " + user_items[num]['name']
        item_display.append(line)
        num = num + 1
      await ctx.send(str(item_display) + " Type the number for the item you want to consume.")
      def check(msg):
          return msg.author == ctx.author and msg.content.isnumeric()
      msg = await self.bot.wait_for("message", check = check)
      index = int(msg.content)
      if index > len(user_items):
        await ctx.send(str(index) + " is not a valid option. Try again")
      else:
        chosenItemName = user_items[(index-1)]['name']
        if chosenItemName == items[0]:
          randomXp = random.randint(0, 100)
          await functions.add_experience(users, member, randomXp)
          await ctx.send("Your cookie has granted you " + str(randomXp) + " xp.")
          await functions.decrease_item_count(users, member, chosenItemName)
          await functions.update_file(guild, users)
        elif chosenItemName == items[1]:
          randomCoins = random.randint(0, 100)
          await functions.add_coins(users, member, randomCoins)
          await ctx.send("Your soda has granted you " + str(randomCoins) + " coins.")
          await functions.decrease_item_count(users, member, chosenItemName)
          await functions.update_file(guild, users)
        elif chosenItemName == items[2]:
          await functions.activate_boost(users, member, 0)
          await ctx.send("You activate your temporary double xp boost")
          await functions.decrease_item_count(users, member, chosenItemName)
          await functions.update_file(guild, users)
        elif chosenItemName == items[3]:
          await functions.activate_boost(users, member, 1)
          await ctx.send("You activate your temporary double coin boost")
          await functions.decrease_item_count(users, member, chosenItemName)
          await functions.update_file(guild, users)
        elif chosenItemName == items[4]:
          await functions.activate_boost(users, member, 2)
          await ctx.send("You activate your temporary triple xp boost")
          await functions.decrease_item_count(users, member, chosenItemName)
          await functions.update_file(guild, users)

  @commands.command()
  async def inventory(self, ctx):
    guild = ctx.guild
    users = await functions.get_user_data(guild)
    member = ctx.author
    user_items = []
    has_items, user_items = await functions.get_inventory(users, member)
    if has_items:
      await ctx.send("Here is your inventory - " + str(user_items))
    else:
      await ctx.send("You have no inventory.")

def setup(bot):
    bot.add_cog(itemCog(bot))
