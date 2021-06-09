import discord
import requests
import json
import random
import normalFunctions
import pymongo

from discord.ext import commands

url = 'mongodb+srv://dbAdminUser:owner127@cluster1.yf6y8.mongodb.net/geekDatabase?retryWrites=true&w=majority'
myclient = pymongo.MongoClient(url)
geekData = myclient["geekDatabase"]
geekMemes = geekData["memes"]
geekEncouragements = geekData["encouragements"]
geekPuns = geekData["puns"]

memes = []
choices = []
fileNum = 1
class CommandsCog(commands.Cog):
  def __init__(self, bot):
        self.bot = bot

  @commands.Cog.listener()
  async def on_ready(self):
    print('The Geekbot is online.')

  @commands.command()
  async def quote(self, ctx):
    response = requests.get("https://zenquotes.io/api/random")
    json_data = json.loads(response.text)
    quote = json_data[0]['q'] + " -" + json_data[0]['a']
    await ctx.send(quote)

  @commands.command()
  async def new(self, ctx,*,message):
    normalFunctions.update_encouragements(message)
    await ctx.send("New encouraging message added.")

  @commands.command()
  async def dogpic(self, ctx):
    print("context guild - " + str(ctx.guild))
    url = "https://api.thedogapi.com/v1/images/search"
    querystring = {"size":"med","order":"random","limit":"1","page":"1","format":"json"}
    headers = {'x-api-key': 'b277d266-6a25-4239-a8c8-df0cde01ad82'}
    response = requests.request("GET", url, headers=headers, params=querystring)
    y = response.text.split(':')[17]
    size = len(y)
    url2 = "https:"+ y[:(size-9)]
    await ctx.send(url2)

  @commands.command()
  async def catpic(self, ctx):
    url = "https://api.thecatapi.com/v1/images/search"
    querystring = {"size":"med","order":"random","limit":"1","page":"1","format":"json"}
    headers = {'x-api-key': '8c44a84b-fe0e-4955-ab66-2e0c21f45c8b'}
    response = requests.request("GET", url, headers=headers, params=querystring)

    y = response.text.split(':')[4]
    size = len(y)
    url2 = "https:"+ y[:(size-9)]
    await ctx.send(url2)

  @commands.command()
  async def meme(self,ctx):
    count = 0
    for meme in geekMemes.find():
       count = count + 1
    randNum = random.randint(0, (count-1))
    count = 0
    for meme in geekMemes.find():
       count = count + 1
       if count == randNum:
        meme_url = meme["url"]
      
  @commands.command()
  async def makememe(self,ctx):
    def check(msg):
      return msg.author == ctx.author and msg.content.isnumeric()
    url = "https://api.imgflip.com/get_memes"
    response = requests.request("GET", url)
    info = response.json()
    memes = info['data']['memes']
    num = 0
    names = []
    image_ID = ""
    while num < 10:
      line = str((num+1)) + " - " + memes[num]["name"]
      names.append(line)
      num = num + 1
    await ctx.send("Select your meme image: \n" + str(names))
    msg = await self.bot.wait_for("message", check = check)
    choice = int(msg.content)
    if choice < 0 or choice > len(names):
      await ctx.send(choice + " is not a valid option. Try again")
    else:
      img_url = memes[(choice-1)]['url']
      image_ID = memes[(choice-1)]['id']
    await ctx.send("Here is your selected image: \n\n" 
    + img_url)
    await ctx.send("What do you want as the top text?")
    def checkTwo(msg):
      return msg.author == ctx.author
    msg = await self.bot.wait_for("message", check = checkTwo)
    topText = msg.content 
    await ctx.send("What do you want as the bottom text?")
    msg = await self.bot.wait_for("message", check = checkTwo)
    bottomText = msg.content
    url2 = 'https://api.imgflip.com/caption_image'
    data1 = {
    'username': 'narku127',
    'password': 'B@53b@11ru135',
    'template_id': image_ID,
    'text0':topText,
    'text1':bottomText
    }
    await ctx.send("It got to response2.")
    response2 = requests.post(url2,data=data1)

    info = response2.json()
    meme_url = info['data']['url']
    #fileName = "userMeme" + str(fileNum)
    print("meme_url: " + str(meme_url))
    await ctx.send("Your user created meme: \n\n" + meme_url)
    normalFunctions.update_meme_list(meme_url)
    await ctx.send("New pun added.") 

  @commands.command()
  async def pun(self, ctx):
    countPun = 0
    for pun in geekPuns.find():
        countPun = countPun + 1
    if countPun == 0:
        await ctx.send("No puns are available right now")
    else:
        randNum = random.randint(0, (countPun-1))
        countPun = 0
        for pun in geekPuns.find():
          countPun = countPun + 1
          if countPun == randNum:
            pun_text = pun["text"]
            await ctx.send(pun_text)
 
  @commands.command()
  async def commands(self, ctx):
    await ctx.send("It got to commands")
    embed = discord.Embed(title="List of commands", description = "A list of available discord commands", color = discord.Colour.red())
    embed.add_field(name = "Inspirational quote", value = "!quote", inline = True)
    embed.add_field(name = "Post new encouraging message", value = "!new <your message>", inline = True)
    embed.add_field(name = "View all profile views", value = "!info", inline = True)
    embed.add_field(name = "View pictures of cute dogs", value = "!dogpic", inline = True)
    embed.add_field(name = "View pictures of adorable cats", value = "!catpic", inline = True)
    embed.add_field(name = "Receive a random meme", value = "!meme", inline = True)
    embed.add_field(name = "Make a custom meme", value = "!makememe", inline = True)
    embed.add_field(name = "View all available games", value = "!games", inline = True)
    embed.add_field(name = "Get all your questions answered", value = "!eightball  <your question>", inline = True)
    embed.add_field(name = "Display all pet related commands", value = "!pet", inline = True)
    embed.add_field(name = "Add new pun to internal database", value = "!newpun <your pun>", inline = True)
    embed.add_field(name = "Receive a random pun", value = "!pun", inline = True)
    embed.add_field(name = "See a list of available items", value = "!items", inline = True)
    embed.add_field(name = "Consume an item from your inventory", value = "!eat", inline = True)
    embed.add_field(name = "View your current inventory", value = "!inventory", inline = True)
    await ctx.send(embed=embed)

#ignore this
  @commands.command()
  async def newpun(self, ctx,*,message):
    normalFunctions.update_pun_list(message)
    await ctx.send("New pun added.")

  def setup(bot):
    bot.add_cog(CommandsCog(bot))
