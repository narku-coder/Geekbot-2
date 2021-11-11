import discord 
import random
import uno
import functions
import requests
import gofish
import normalFunctions

from discord.ext import commands

choices = []
Hangman_Pics = [
  '''
      +---+
        |
        |
        |
      ===
     ''', 
  '''
      +----+
  O    |
        |
        |
      ===
  ''', 
  '''
      +----+
  O    |
  |     |
        |
      ===
  ''', 
  '''
      +----+
  O     |
 /|      |
         |
      ===
  ''', 
  '''
       +----+
  O     |
 /|\     |
         |
      ===
  ''', 
  '''
       +----+
  O     |
 /|\     |
 /       |
      ===
  ''', 
  '''
       +----+
  O     |
 /|\     |
 / \     |
      ===
  ''']
unoDeck = []
goFishDeck = []

class gameCog(commands.Cog):
  def __init__(self, bot):
        self.bot = bot

  @commands.command()
  async def games(self, ctx):
    embed = discord.Embed(title="List of games", description = "A list of available games to play", color = discord.Colour.blue())
    embed.add_field(name = "To play some hangman", value = "!hangman", inline = True)
    embed.add_field(name = "To answer trivia questions", value = "!trivia", inline = True)
    embed.add_field(name = "To guess a random number", value = "!guessnumber", inline = True)
    embed.add_field(name = "To play Uno with a fellow member", value = "!uno <User>", inline = True)
    embed.add_field(name = "To play Go Fish with a fellow member", value = "!gofish <User>", inline = True)
    embed.set_footer(text = "Games list")
    await ctx.send(embed=embed)

  @commands.command()
  async def trivia(self, ctx):
    guild = ctx.guild
    member = ctx.author
    url = "https://opentdb.com/api.php"
    querystring = {"amount":"1","type":"multiple"}
    choices = []
    response = requests.get(url, params=querystring)
    trivia = response.json()
    question = trivia["results"][0]["question"]
    print("question - " + question)
    correct_answer = trivia["results"][0]["correct_answer"]
    print("correct_answer - " + correct_answer)
    wrong_answers = trivia["results"][0]["incorrect_answers"]
    choices.append(correct_answer)
    t = 0
    while (t < 3):
      choices.append(wrong_answers[t])
      t = t + 1
    embed = discord.Embed(title="Your Trivia Question", description = question, color = discord.Colour.red())
    letters = ["A. ", "B. ", "C. ", "D. "]
    num = 0
    random.shuffle(choices)
    while (num < 4):
      embed.add_field(name = letters[num], value = choices[num], inline = False)
      num = num + 1
    await ctx.send(embed=embed)
    def check(msg):
      return msg.author == ctx.author and msg.channel == ctx.channel
    msg = await self.bot.wait_for("message", check = check)
    gotCorrect = await functions.check_answer(msg, ctx, correct_answer, choices)
    if gotCorrect:
      await ctx.send("Congratulations, you got it correct. You just earned 100 coins.", tts = False)
      members = await functions.get_user_data(guild)
      pets = await functions.get_pet_data()
      boosts = await functions.get_boosts_data()
      await functions.add_coins(members, member, 100, boosts)
      await functions.update_db(members, pets, boosts)
    else:
      await ctx.send("You got it wrong. Try again next time")

  @commands.command()
  async def hangman(self,ctx):
    guild = ctx.guild
    member = ctx.author
    words = []
    random_words = open('./textFiles/words.txt', 'r')
    content = random_words.read()
    words = content.split('\n')
    random_words.close()
    size = 200
    randNum = random.randint(0, (size-1))
    random_word = words[randNum]
    mystery = []
    num = 0
    size_word = len(random_word)
    print("random_word size - " + str(size_word))
    mystery_two = ""
    while num < (size_word):
      mystery.append("-")
      num = num + 1
    for let in mystery:  
      mystery_two += let
    print("mystery_two size - " + str(len(mystery_two)))
    print("random word - " + random_word) 
    attempts = 0
    def check(msg):
      return msg.author == ctx.author and msg.channel == ctx.channel and msg.content.lower() in ["a", "b", "c","d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n","o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
    guesses = []
    while True:
      try:
        word_two = ""
        for let in mystery_two:  
          word_two += let + " "
        await ctx.send(Hangman_Pics[attempts] + "\n" + "Your guesses - " + str(guesses) + "\n" + "Here is your mystery word : " + word_two)
        msg = await self.bot.wait_for("message", check = check)
        guesses.append(msg.content)
        print("msg - " + str(msg.content))
        isIn = normalFunctions.verify(msg, random_word)
        if isIn:
          mystery_two = normalFunctions.fill_mystery(msg, random_word, mystery_two)
        else:
          attempts = attempts + 1
        print("attempts - " + str(attempts))
        if ((mystery_two == random_word) or (attempts == 6)): 
          break
      except Exception as e:
        print(e)
    if mystery_two == random_word:
      print("It got to correct if")
      await ctx.send("Great job guessing the mystery word " + random_word + ". You just earned 25 coins.")
      members = await functions.get_user_data(guild)
      pets = await functions.get_pet_data()
      boosts = await functions.get_boosts_data()
      await functions.add_coins(members, member, 25, boosts)
      await functions.update_db(members, pets, boosts)
    if attempts == 6:
       print("It got to fail if")
      await ctx.send("Nice Try. You will get it next time. The mystery word was " + str(random_word))

  @commands.command()
  async def guessnumber(self, ctx):
    guild = ctx.guild
    member = ctx.author
    randNum = random.randint(0, 100)
    attempts = 0
    def check(msg):
      return msg.author == ctx.author and msg.channel == ctx.channel and msg.content.isnumeric()
    while True:
      try:
        await ctx.send("Guess a number between 1 and 100")
        msg = await self.bot.wait_for("message", check = check)
        guessNum = int(msg.content)
        if guessNum < randNum:
          attempts = attempts + 1
          await ctx.send("Think bigger")
        elif guessNum > randNum:
          attempts = attempts + 1
          await ctx.send("Think smaller")
        if ((guessNum == randNum) or (attempts == 3)): 
          break
      except Exception as e:
        print(e)
    if guessNum == randNum:
      await ctx.send("Great job guessing the mystery number " + randNum + ". You just earned 60 coins.")
      pets = await functions.get_pet_data()
      members = await functions.get_user_data(guild)
      boosts = await functions.get_boosts_data()
      await functions.add_coins(members, member, 60, boosts)
      await functions.update_db(members, pets, boosts)
    if attempts == 3:
      await ctx.send("Nice Try. You will get it next time. The mysterious number was " + str(randNum))

  @commands.command()
  async def eightball(self, ctx,*,message): 
    eight_ball_responses = []
    responses = open('./textFiles/eightBall.txt', 'r')
    content = responses.read()
    eight_ball_responses = content.split('\n')
    responses.close()
    randNum = random.randint(0, 20)
    await ctx.send(eight_ball_responses[randNum])

  @commands.command()
  async def uno(self, ctx, user: discord.User):
    guild = ctx.guild
    users = await functions.get_user_data(guild)
    unoDeck = uno.buildDeck()
    player1 = ctx.author
    player2 = user
    player1_hand = []
    player2_hand = []
    playerTurn = 0
    discards = []
    playing = True
    print("the selected user is - " + user.name)
    await user.send("You have been challenged to a game of Uno by " + ctx.author.mention + ". Do you accept? Type y or yes to accept.")
    def check(msg):
      return msg.author == user
    msg = await self.bot.wait_for("message", check = check)
    resp = msg.content
    if resp.lower() == "y" or resp.lower() == "yes":
      await ctx.send("Let's play some uno.")
      unoDeck = uno.shuffleDeck(unoDeck, 108)
      player1_hand = uno.drawCards(5, unoDeck)
      player2_hand = uno.drawCards(5, unoDeck)
      player1_hand_display = []
      player2_hand_display = []
      discards.append(unoDeck.pop(0))
      discardSize = 0
      player1_hand_display = gofish.printHand(player1_hand)
      player2_hand_display = gofish.printHand(player2_hand)
      await player2.send("\n\nYour hand - " + str(player2_hand_display))
      while playing:
        if playerTurn == 0:
          await ctx.send("It is " + player1.mention + " turn.\n\n")
          await ctx.send("Card on top of pile: {}".format(discards[discardSize]) + "\n Player 1 hand size - " + str(len(player1_hand)) + "\n Player 2 hand size - " + str(len(player2_hand)))
          player1_hand_display = gofish.printHand(player1_hand)
          await player1.send("\n\nYour hand - " + str(player1_hand_display))
          await ctx.send("Choose a card to play by typing the number to the left off the card, type 0 to draw a card or -1 to call uno")
          def checkTwo(msg):
            return msg.author == player1
          msg = await self.bot.wait_for("message", check = checkTwo)
          resp = int(msg.content)
          if resp <= len(player1_hand) and resp > 0:
            current_card = player1_hand.pop((resp-1))
            if len(player1_hand) == 0:
               ctx.send(player1.mentions + " wins. Congratulations you earned 25 coins!")
               members = await functions.get_user_data(guild)
               await functions.add_coins(members, player1, 25)
               await functions.update_file(guild, members)
               playing = False
            card_splits = current_card.split(" ")
            current_color = card_splits[0]
            current_value = card_splits[1]
            discards.append(current_card)
            discardSize = discardSize + 1
            if current_value == "Skip" or current_value == "Reverse":
              playerTurn = 0
            elif current_value == "Draw":
              if current_color == "Wild":
                drawnCards = uno.drawCards(4, unoDeck)
                num = 0
                while num < len(drawnCards):
                  player2_hand.append(drawnCards[num])
                  num = num + 1
                await ctx.send("Choose a color")
                msg = await self.bot.wait_for("message", check = checkTwo)
                await ctx.send("The chosen color is: " + msg.content)
                playerTurn = 0
              else:
                drawnCards = uno.drawCards(2, unoDeck)
                num = 0
                while num < len(drawnCards):
                  player2_hand.append(drawnCards[num])
                  num = num + 1
                playerTurn = 0
            elif current_color == "Wild":
              await ctx.send("Choose a color")
              msg = await self.bot.wait_for("message", check = checkTwo)
              await ctx.send("The chosen color is: " + msg.content)
              playerTurn = 1
            else:
              playerTurn = 1
          elif resp == 0:
            drawnCards = uno.drawCards(1, unoDeck)
            num = 0
            while num < len(drawnCards):
              player1_hand.append(drawnCards[num])
              num = num + 1
            playerTurn = 1
          elif resp == -1:
            if len(player2_hand) > 1:
              await ctx.send("That was an illegal uno call. You will now draw 2 cards.")
              drawnCards = uno.drawCards(2, unoDeck)
              num = 0
              while num < len(drawnCards):
                player2_hand.append(drawnCards[num])
                num = num + 1
              playerTurn = 0
            else:
              await ctx.send(player1.mention + " has Uno.")
              playerTurn = 1
          else:
            await ctx.send("The number was invalid. Try again")
        elif playerTurn == 1:
          await ctx.send("It is " + player2.mention + " turn.\n\n")
          await ctx.send("Card on top of pile: {}".format(discards[discardSize]) + "\n Player 1 hand size - " + str(len(player1_hand)) + "\n Player 2 hand size - " + str(len(player2_hand)))
          player2_hand_display = gofish.printHand(player2_hand)
          await player2.send("\n\nYour hand - " + str(player2_hand_display))
          await ctx.send("Choose a card to play by typing the number to the left off the card, type 0 to draw a card or -1 to call uno")
          def checkTwo(msg):
            return msg.author == player2
          msg = await self.bot.wait_for("message", check = checkTwo)
          resp = int(msg.content)
          if resp <= len(player2_hand) and resp > 0:
            current_card = player2_hand.pop((resp-1))
            if len(player1_hand) == 0:
               ctx.send(player2.mentions + " wins. Congratulations!")
               members = await functions.get_user_data(guild)
               await functions.add_coins(members, player2, 25)
               await functions.update_file(guild, members)
               playing = False
            card_splits = current_card.split(" ")
            current_color = card_splits[0]
            current_value = card_splits[1]
            discards.append(current_card)
            discardSize = discardSize + 1
            if current_value == "Skip" or current_value == "Reverse":
              playerTurn = 1
            elif current_value == "Draw":
              if current_color == "Wild":
                drawnCards = uno.drawCards(4, unoDeck)
                num = 0
                while num < len(drawnCards):
                  player1_hand.append(drawnCards[num])
                  num = num + 1
                await ctx.send("Choose a color")
                msg = await self.bot.wait_for("message", check = checkTwo)
                await ctx.send("The chosen color is: " + msg.content)
                playerTurn = 1
              else:
                drawnCards = uno.drawCards(2, unoDeck)
                num = 0
                while num < len(drawnCards):
                  player1_hand.append(drawnCards[num])
                  num = num + 1
                playerTurn = 1
            elif current_color == "Wild":
              await ctx.send("Choose a color")
              msg = await self.bot.wait_for("message", check = checkTwo)
              await ctx.send("The chosen color is: " + msg.content)
              playerTurn = 0
            else:
              playerTurn = 0
          elif resp == 0:
            drawnCards = uno.drawCards(1, unoDeck)
            num = 0
            while num < len(drawnCards):
              player2_hand.append(drawnCards[num])
              num = num + 1
            playerTurn = 0
          elif resp == -1:
            if len(player2_hand) > 1:
              await ctx.send("That was an illegal uno call. You will now draw 2 cards.")
              drawnCards = uno.drawCards(2, unoDeck)
              num = 0
              while num < len(drawnCards):
                player2_hand.append(drawnCards[num])
                num = num + 1
              playerTurn = 0
            else:
              await ctx.send(player1.mention + " has Uno.")
              playerTurn = 1
          else:
            await player2.send("The number was invalid. Try again")
    else:
      await ctx.send(player2.mention + " has denied your request for Uno. Try again later")
  
  @commands.command()
  async def gofish(self, ctx, user: discord.User):
    guild = ctx.guild
    users = await functions.get_user_data(guild)
    goFishDeck = gofish.buildDeck()
    player1 = ctx.author
    player2 = user
    player1_hand = []
    player2_hand = []
    player1_points = 0
    player2_points = 0
    playerTurn = 0
    playing = True
    possibleSet1 = False
    possibleSet2 = False
    chosenRank = ""
    canDiscard = 1
    ranks = ["ace", "2", "3", "4", "5", "6", "7", "8", "9", "10", "jack", "queen", "king"]
    await user.send("You have been challenged to a game of Go Fish by " + ctx.author.mention + ". Do you accept? Type y or yes to accept.")
    def check(msg):
      return msg.author == player2
    msg = await self.bot.wait_for("message", check = check)
    resp = msg.content
    if resp.lower() == "y" or resp.lower() == "yes":
      await ctx.send("Let's play Go Fish")
      goFishDeck = uno.shuffleDeck(goFishDeck, 52)
      player1_hand = uno.drawCards(7, goFishDeck)
      player2_hand = uno.drawCards(7, goFishDeck)
      player2_hand_display = gofish.printHand(player2_hand)
      await player2.send("\n\nYour hand - " + str(player2_hand_display))
      while playing:
        if playerTurn == 0:
          player1_hand_display = gofish.printHand(player1_hand)
          await player1.send("\n\n\n\nYour hand - " + str(player1_hand_display))
          await ctx.send(player1.mention + "points: " + str(player1_points) + player2.mention + "points: " + str(player1_points) + "\n\nIt is " + player1.mention + " turn. \nRequest a rank: ")
          def checkTwo(msg):
            return msg.author == player1 and msg.content.lower() in ranks
          msg = await self.bot.wait_for("message", check = checkTwo)
          rank = msg.content
          if gofish.verifyRequest(rank, player1_hand) == False:
            await ctx.send("That is not a valid request. Try again")
          else:
            await ctx.send(player2.mention + " do you have any " + rank + "s. Type y or yes if you do")
            def checkTwo(msg):
              return msg.author == player2
            msg = await self.bot.wait_for("message", check = checkTwo)
            resp = msg.content
            if resp.lower() == "y" or resp.lower() == "yes":
              while True:
                player2_hand_display = gofish.printHand(player2_hand)
                await player2.send("Your hand - " + str(player2_hand_display))
                await ctx.send(player2.mention + " select a card to give away by typing the number to the left of the card")
                print("it got to player2 card giveaway")
                def checkFour(msg):
                  return msg.author == player2 and msg.content.isnumeric()
                msg = await self.bot.wait_for("message", check = checkFour)
                resp = int(msg.content)
                if resp <= len(player2_hand):
                  selected_card = player2_hand[(resp-1)]
                  player2_hand.pop((resp-1))
                  player1_hand.append(selected_card)
                  await ctx.send("Type d or done if finished if not type any other key.")
                  def checkFive(msg):
                    return msg.author == player2
                  msg = await self.bot.wait_for("message", check = checkFive)
                  if msg.content.lower() == "d" or msg.content.lower() == "done":
                    break
              playerTurn = 0
            else:
              drawnCards = uno.drawCards(1, goFishDeck)
              num = 0
              while num < len(drawnCards):
                player1_hand.append(drawnCards[num])
                num = num + 1
              possibleSet1,chosenRank = gofish.canMakeSet(player1_hand)
              if possibleSet1:
                player1_hand = gofish.makeSet(player1_hand, chosenRank)
                player1_points = player1_points + 1
              playerTurn = 1
        if playerTurn == 1:
          player2_hand_display = gofish.printHand(player2_hand)
          await player2.send("\n\n\nYour hand - " + str(player2_hand_display))
          await ctx.send(player1.mention + "points: " + str(player1_points) + player2.mention + "points: " + str(player1_points) + "\n\nIt is " + player2.mention + " turn. \n Request a rank: ")
          def checkTwo(msg):
            return msg.author == player2 and msg.content.lower() in ranks
          msg = await self.bot.wait_for("message", check = checkTwo)
          rank = msg.content
          if not gofish.verifyRequest(rank, player2_hand):
            await ctx.send("That is not a valid request. Try again")
          else:
            await ctx.send(player1.mention + " do you have any " + rank + "s. Type y or yes if you do")
            def checkThree(msg):
              return msg.author == player1
            msg = await self.bot.wait_for("message", check = checkThree)
            resp = msg.content
            if resp.lower() == "y" or resp.lower() == "yes":
              while True:
                player1_hand_display = gofish.printHand(player1_hand)
                await player1.send("\n\n\nYour hand - " + str(player1_hand_display))
                await ctx.send(player1.mention + " select a card to give away")
                def checkFour(msg):
                  return msg.author == player1 and msg.content.isnumeric()
                msg = await self.bot.wait_for("message", check = checkFour)
                resp = int(msg.content)
                if resp <= len(player1_hand):
                  selected_card = player1_hand[(resp-1)]
                  player1_hand.pop((resp-1))
                  player2_hand.append(selected_card)
                  await ctx.send("Type d or done if finished if not type any other key.")
                  def checkFive(msg):
                    return msg.author == player1
                  msg = await self.bot.wait_for("message", check = checkFive)
                  if msg.content.lower() == "d" or msg.content.lower() == "done":
                    break
              playerTurn = 1
            else:
              drawnCards = uno.drawCards(1, goFishDeck)
              num = 0
              while num < len(drawnCards):
                player2_hand.append(drawnCards[num])
                num = num + 1
              possibleSet2,chosenRank = gofish.canMakeSet(player2_hand)
              if possibleSet2:
                player2_hand = gofish.makeSet(player2_hand, chosenRank)
                player2_points = player2_points + 1
              playerTurn = 0
        if len(player1_hand) == 0 or len(player2_hand) == 0 or len(goFishDeck) == 0:
          playing = False
          if len(player1_hand) == 0:
            await ctx.send("Congratulations. " + player1.mention + " wins. You scored " + str(player1_points) + " points. You won 25 coins")
            members = await functions.get_user_data(guild)
            await functions.add_coins(members, player1, 25)
            await functions.update_file(guild, members)
          elif len(player2_hand) == 0:
            await ctx.send("Congratulations. " + player2.mention + " wins. You scored " + str(player2_points) + " points. You won 25 coins")
            members = await functions.get_user_data(guild)
            await functions.add_coins(members, player1, 25)
            await functions.update_file(guild, members) 
          elif len(goFishDeck) == 0:
            await ctx.send("Y'all ran out of cards. Better luck next time")
    else:
      await ctx.send(player2.mention + " has denied your request for Go Fish. Try again later")

def setup(bot):
    bot.add_cog(gameCog(bot)) 
