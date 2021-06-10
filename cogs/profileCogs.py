import functions
import datetime as dt
import discord
import normalFunctions

from discord.ext import commands

class profileCog(commands.Cog):
  def __init__(self, bot):
        self.bot = bot

  @commands.command()
  async def info(self, ctx):
    embed = discord.Embed(title="Profile Commands", description = "A list of commands to provide various info", color = discord.Colour.green())
    embed.add_field(name = "Display current level", value = "!level", inline = True)
    embed.add_field(name = "Display current balance", value = "!balance", inline = True)
    embed.add_field(name = "To view the profile of a fellow member", value = "!profile <User>", inline = True)
    embed.add_field(name = "To open a new bank account", value = "!openaccount", inline = True)
    embed.add_field(name = "To deposit money to your bank account", value = "!deposit", inline = True)
    embed.add_field(name = "To withdraw money from your bank account", value = "!withdraw", inline = True)
    await ctx.send(embed=embed)

  @commands.command()
  async def level(self,ctx):
    guild = ctx.guild
    users = await functions.get_user_data(guild)
    member = ctx.author

    await functions.view_level(users, member, ctx)

  @commands.command()
  async def balance(self,ctx):
    guild = ctx.guild
    users = await functions.get_user_data(guild)
    member = ctx.author

    await functions.view_balance(users, member, ctx)

  @commands.command()
  async def profile(self, ctx, user: discord.User):
    currLevel = 0
    numPets = 0
    bal = 0
    guild = ctx.guild
    member = user
    users = await functions.get_user_data(guild)
    account_available = await functions.has_account(users,member)
    has_items, user_items = await functions.get_inventory(users, member)
    currLevel,numPets,bal = await functions.get_profile_info(users, member)
    embed = discord.Embed(title=user.name + "'s profile", description = "Basic profile information about " + user.name, color = discord.Colour.red())
    embed.add_field(name = "Current Level", value = str(currLevel), inline = True)
    embed.add_field(name = "Number of pets owned", value = str(numPets), inline = True)
    embed.add_field(name = "Current wallet", value = str(bal), inline = True)
    if account_available:
      account_bal = await functions.get_account_balance(users, member)
      embed.add_field(name = "Current account balance", value = str(account_bal), inline = True)
    if has_items:
      embed.add_field(name = "Current inventory", value = str(user_items), inline = True)
    embed.set_thumbnail(url = user.avatar_url)
    embed.set_footer(text = user.name + "'s profile")
    await ctx.send(embed=embed)


  @commands.command()
  async def wordHour(self,ctx):
    await ctx.send("Message received. Let's earn some coins")
    word = ""
    num = 0
    while True:
      hour = dt.datetime.now().hour
      if hour % 6 == 0:
        while num < 1:
          word = normalFunctions.getDailyWord()
          await ctx.send("@everyone The first person who types a message with this animal: " + word + " will get 100 coins.")
          num = num + 1
      else:
        num = 0

  @commands.command()
  async def openaccount(self,ctx):
    guild = ctx.guild
    users = await functions.get_user_data(guild)
    pets = await functions.get_pet_data()
    member = ctx.author
    has_account = await functions.has_account(users, member)
    can_deposit = False
    if has_account:
      await ctx.send("You already have a bank account.")
    else:
      await ctx.send("How many coins do want to deposit into your new account?")
      def check(msg):
        return msg.author == ctx.author and msg.content.isnumeric() and msg.channel == ctx.channel
      msg = await self.bot.wait_for("message", check = check)
      amount = int(msg.content)
      can_deposit = await functions.can_buy(users, member,amount)
      if can_deposit:
        await functions.add_account(users, member,amount)
        await functions.subtract_coins(users, member,amount)
        await functions.update_db(members, pets)
        await ctx.send("You now have a bank account with a balance of " + str(amount) + " coins")
      else:
        await ctx.send("You don't have that amount of money in your wallet. Try again")

  @commands.command()
  async def deposit(self,ctx):
    guild = ctx.guild
    users = await functions.get_user_data(guild)
    pets = await functions.get_pet_data()
    member = ctx.author
    has_account = await functions.has_account(users, member)
    can_deposit = False
    if has_account:
      await ctx.send("How many coins do want to deposit into your new account?")
      def check(msg):
        return msg.author == ctx.author and msg.content.isnumeric() and msg.channel == ctx.channel
      msg = await self.bot.wait_for("message", check = check)
      amount = int(msg.content)
      can_deposit = await functions.can_buy(users, member,amount)
      if can_deposit:
        await functions.deposit_coins(users, member,amount)
        await functions.subtract_coins(users, member,amount)
        await functions.update_db(members, pets)
        await ctx.send("You now deposited " + str(amount) + " coins into your bank account.")
      else:
        await ctx.send("You don't have that amount of money in your wallet. Try again")
    else:
      await ctx.send("You don't have a bank account")

  @commands.command()
  async def withdraw(self,ctx):
    guild = ctx.guild
    users = await functions.get_user_data(guild)
    pets = await functions.get_pet_data()
    member = ctx.author
    has_account = await functions.has_account(users, member)
    withdraw_legal = False
    if has_account:
      await ctx.send("How many coins do want to withdraw from your account?")
      def check(msg):
        return msg.author == ctx.author and msg.content.isnumeric() and msg.channel == ctx.channel
      msg = await self.bot.wait_for("message", check = check)
      amount = int(msg.content)
      withdraw_legal = await functions.can_withdraw(users, member,amount)
      if withdraw_legal:
        await functions.withdraw_coins(users, member,amount)
        await functions.add_coins(users, member,amount)
        await functions.update_db(members, pets)
        await ctx.send("You now withdrawn " + str(amount) + " coins from your bank account.")
      else:
        await ctx.send("You don't have that amount of money in bank account. Try again")
    else:
      await ctx.send("You don't have a bank account")

def setup(bot):
    bot.add_cog(profileCog(bot))
