import discord
import json
import string
from discord.ext import commands
# from utils import get_channel
from datetime import datetime
intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix=commands.when_mentioned_or("!"), intents=intents, allowed_mentions=discord.AllowedMentions(everyone=False), help_command=None)

@bot.event
async def on_ready(): 
    for guild in bot.guilds:
        print(f'{bot.user} connected to {guild.name}')

@bot.event
async def on_message(ctx):
    if ctx.content.startswith('!') and ctx.author.id != bot.user.id:
        current_time = datetime.utcnow().strftime("%H:%M:%S")
        with open("messages.log", "a") as j:
            j.write(f"({current_time}) {ctx.author.name}: {ctx.content} \n")
    await bot.process_commands(ctx)

class BaseEvent:

    def __init__(self, interval_minutes):
        self.interval_minutes = interval_minutes

    async def run(self, client):
        raise NotImplementedError
  
'''
class ChallengeSolves(BaseEvent):

    def __init__(self):
      interval_minutes = 0  
      super().__init__(interval_minutes)

    async def run(self, client):
      with open('profiles.json') as w:
        profiles = json.load(w)
      if 

      channel = get_channel(client, "challenge-solves")
      await channel.send(msg)
'''
@bot.command(name='help', aliases=['h'])
@commands.guild_only()
async def help(ctx):

    contents = ["Rules", "Commands", "Resources"]
    rules = ['Submit flags using the wackersBot. Flag format is wctf{}', 'No hacking the infrastructure or brute-forcing flags.', 'No flag sharing or collaborative effort. This is a solo ctf.', 'Asking how to solve the challenges on forums is not allowed.', 'Hints will not be given. But, if you think a challenge is broken or have a question, DM the challenge creator. ', 'Keep notes on how you solved the challenges. Writeups may be requested to verify flag submissions.']
    main_embed = discord.Embed(title="Help", color=0x0000FF, timestamp=datetime.utcnow())
    chall_string = ""
    rules_string = ""
    for i in range(len(contents)):
      chall_string += f"{i+1}) {contents[i]}\n"
    for i in range(len(rules)):
      rules_string += f"- {rules[i]}\n"
    main_embed.add_field(name="Available Help List", value=chall_string, inline=False)
    main_embed.add_field(name="Rules:", value=rules_string, inline=False)

    commands_embed = discord.Embed(title="Commands", color=0x0000FF, timestamp=datetime.utcnow())
    commands_embed.add_field(name="!flag (flag)", value="Submit a flag", inline=False)
    commands_embed.add_field(name="!profile", value="Look up any user's stats!", inline=False)
    commands_embed.add_field(name="!leaderboard (!lb)", value="view the current leaderboard", inline=False)
    commands_embed.add_field(name="!challenges [challenge number or title] (!c, !sc, !show_challenges)", value="Show a list of all the challenges", inline=False)
    commands_embed.add_field(name="!add_challenge (!ac) (Admin only command)", value="add your challenge to the bot", inline=False)
    commands_embed.add_field(name="!remove_challenge (!rc) (Admin only command)", value="remove your challenge from the bot", inline=False)
    commands_embed.add_field(name="!help", value="displays this message!", inline=False) 

    resources_embed = discord.Embed(title="Resources", color=0x0000FF, timestamp=datetime.utcnow())
    resources_embed.add_field(name="Ctf checklist for beginners", value="https://fareedfauzi.gitbook.io/ctf-checklist-for-beginner/", inline=False)
    resources_embed.add_field(name="Compiled list of many things used in ctfs", value="https://github.com/JohnHammond/ctf-katana", inline=False)

    contents = [main_embed, commands_embed, resources_embed]
    message = await ctx.send(embed=contents[0])
    await message.add_reaction("1️⃣")
    await message.add_reaction("2️⃣")
    await message.add_reaction("3️⃣")
    def check(reaction, user):
        return user == ctx.author and str(reaction.emoji) in ["1️⃣", "2️⃣", "3️⃣"]
    while True:
        reaction, user = await bot.wait_for("reaction_add", timeout=60, check=check)
        if str(reaction.emoji) == "1️⃣":
            await message.edit(embed=contents[0])
            await message.remove_reaction(reaction, user)
        elif str(reaction.emoji) == "2️⃣":
            await message.edit(embed=contents[1])
            await message.remove_reaction(reaction, user)
        elif str(reaction.emoji) == "3️⃣":
            await message.edit(embed=contents[2])
            await message.remove_reaction(reaction, user)
        else:
            await message.remove_reaction(reaction, user)

@bot.command(name="profile", aliases=['stats'])
@commands.guild_only()
async def profile(ctx, search: discord.Member=None):
    with open("challenges.json") as w:
      challenges = json.load(w)
    with open("templateprofile.json") as w:
      templateprofile = json.load(w)
    if search is None:
        search = ctx.author
    else:
        search = search
    with open("profiles.json") as j:
        profiles = json.load(j)
    for user in profiles:
        if search.id == user["id"]:
          solved_chall_string = ""
          unsolved_chall_string = ""
          for challenge in challenges:
            if user[f"{challenge['title']}"] == "Solved":
              solved_chall_string += f"{challenge['title']} \n"
            elif user[f"{challenge['title']}"] == "Unsolved":
              unsolved_chall_string += f"{challenge['title']} \n"
          embed = discord.Embed(title=f"{user['name']}'s stats", color=0x0000FF, timestamp=datetime.utcnow())
          embed.add_field(name="Score", value=f"{user['points']}", inline=True)
          if solved_chall_string != "":
            embed.add_field(name="Solved Challenges", value=solved_chall_string, inline=False)
            if len(solved_chall_string.splitlines()) != len(challenges):
              embed.add_field(name="Unsolved Challenges", value=unsolved_chall_string, inline=False)
          else:
            embed.add_field(name="Unsolved Challenges", value=unsolved_chall_string, inline=False)
          embed.set_thumbnail(url=search.avatar_url)
          return await ctx.send(embed=embed)
    else:
        templateprofile["name"] = search.name
        templateprofile["id"] = search.id
        profiles.append(templateprofile)
        embed = discord.Embed(title="Profile initialized!", color=0x0000FF, timestamp=datetime.utcnow())
        embed.add_field(name="Please run !profile again to check your profile", value='\u200b')
        embed.set_thumbnail(url="https://avatars.githubusercontent.com/u/86629756?s=400&u=6923f73c46cf0f9ac047bdceda49d8cb4df0a844&v=4")
        await ctx.send(embed=embed)
        with open("profiles.json", "w") as j:
            json.dump(profiles, j)

@bot.command(name="flag", help="submit the flag")
@commands.guild_only()
async def flag(ctx, flag: str="default flag"):
  with open("challenges.json") as w:
    challenges = json.load(w)
  with open("profiles.json") as w:
    profiles = json.load(w)
  for challenge in challenges:
    if challenge["flag"] == flag:
      for profile in profiles:
        if profile["id"] == ctx.author.id:
          if profile[f"{challenge['title']}"] == "Unsolved":
            profile["solves"] = profile["solves"] + 1
            profile["points"] = profile["points"] + challenge["points"]
            profile[f"{challenge['title']}"] = "Solved"
            with open("profiles.json", "w") as w:
              json.dump(profiles, w)
            return await ctx.send(f"Good job! You have solved {challenge['title']}")
          else:
            return await ctx.send("You already solved that challenge!")
      else:
        return await ctx.send("You don't have a profile yet! This flag is correct, but please create a profile first")
  else:
    return await ctx.send("Your flag is incorrect")

@bot.command(name="challenges", aliases=['c', 'sc', 'show_challenges'])
@commands.guild_only()
async def show_challenges(ctx, selection=None):
  with open("challenges.json") as w:
    challenges = json.load(w)
  if (not selection):
    embed = discord.Embed(title="Challenges", color=0x00FFFF)
    crypto_chall_string = ""
    misc_chall_string = ""
    rev_chall_string = ""
    web_chall_string = ""
    pwn_chall_string = ""
    for i in range(len(challenges)):
      if challenges[i]['category'] == "crypto":
        crypto_chall_string += f"{i+1}) {challenges[i]['title']} ({challenges[i]['points']} points)\n"
    for i in range(len(challenges)):
      if challenges[i]['category'] == "misc":
        misc_chall_string += f"{i+1}) {challenges[i]['title']} ({challenges[i]['points']} points)\n"
    for i in range(len(challenges)):
      if challenges[i]['category'] == "rev":
        rev_chall_string += f"{i+1}) {challenges[i]['title']} ({challenges[i]['points']} points)\n"
    for i in range(len(challenges)):
      if challenges[i]['category'] == "web":
        web_chall_string += f"{i+1}) {challenges[i]['title']} ({challenges[i]['points']} points)\n"
    for i in range(len(challenges)):
      if challenges[i]['category'] == "pwn":
        pwn_chall_string += f"{i+1}) {challenges[i]['title']} ({challenges[i]['points']} points)\n"
    embed.add_field(name="--- Crypto ---", value=crypto_chall_string, inline=False)
    embed.add_field(name="--- Misc ---", value=misc_chall_string, inline=False)
    embed.add_field(name="--- Pwn ---", value=pwn_chall_string, inline=False)
    embed.add_field(name="--- Rev ---", value=rev_chall_string, inline=False)
    embed.add_field(name="--- Web ---", value=web_chall_string, inline=False)
    return await ctx.send(embed=embed)
  else:
    for i in range(len(challenges)):
      if selection.isdigit():
        if (i+1) == int(selection):
          embed = discord.Embed(title=f"{challenges[i]['title']}", color=0x0000FF, timestamp=datetime.utcnow())
          embed.add_field(name="Description", value=challenges[i]["description"], inline=False)
          embed.add_field(name="Author", value=challenges[i]["author"], inline=False)
          embed.add_field(name="Points", value=challenges[i]["points"], inline=False)
          embed.add_field(name="Attachments", value=challenges[i]["attachments"], inline=False)
          return await ctx.send(embed=embed)
      else:
        if challenges[i]["title"] == selection:
          embed = discord.Embed(title=f"{challenges[i]['title']}", color=0x0000FF, timestamp=datetime.utcnow())
          embed.add_field(name="Description", value=challenges[i]["description"], inline=False)
          embed.add_field(name="Author", value=challenges[i]["author"], inline=False)
          embed.add_field(name="Points", value=challenges[i]["points"], inline=False)
          embed.add_field(name="Attachments", value=challenges[i]["attachments"], inline=False)
          return await ctx.send(embed=embed)
    else:
      return await ctx.send("Invalid challenge title or number!")

@bot.command(name="add_challenge", aliases=['ac'])
@commands.guild_only()
@commands.has_permissions(administrator=True)
async def add_challenge(ctx):
  def check(msg):
    return msg.author == ctx.author and msg.channel == msg.channel and msg.content.lower()[0] in string.printable
  with open("challenges.json") as w:
    challenges = json.load(w)
  with open("profiles.json") as w:
    profiles = json.load(w)
  with open("templateprofile.json") as w:
    templateprofile = json.load(w)
  await ctx.send("Challenge title: ")
  chall_title = await bot.wait_for("message", check=check)
  await ctx.send("Category: ")
  category = await bot.wait_for("message", check=check)
  category.content = category.content.lower()
  await ctx.send("Author: ")
  author = await bot.wait_for("message", check=check)
  await ctx.send("Flag: ")
  flag = await bot.wait_for("message", check=check)
  await ctx.send("Points: ")
  points = await bot.wait_for("message", check=check)
  await ctx.send("Description: ")
  description = await bot.wait_for("message", check=check)
  await ctx.send("Attachments: ")
  attachments = await bot.wait_for("message", check=check)
  challenges.append({"title": chall_title.content, "category": category.content, "author": author.content, "flag": flag.content, "points": int(points.content), "description": description.content, "attachments": attachments.content})
  for profile in profiles:
    profile[f"{chall_title.content}"] = "Unsolved"
  templateprofile[f"{chall_title.content}"] = "Unsolved"
  await ctx.send("Challenge created!")
  with open("challenges.json", "w") as w:
    json.dump(challenges, w)
  with open("profiles.json", "w") as w:
    json.dump(profiles, w)
  with open("templateprofile.json", "w") as w:
    json.dump(templateprofile, w)

@bot.command(name="remove_challenge", aliases=['rc'])
@commands.guild_only()
@commands.has_permissions(administrator=True)
async def remove_challenge(ctx):
  with open("challenges.json") as w:
    challenges = json.load(w)
  with open("profiles.json") as w:
    profiles = json.load(w)
  def check(msg):
    return msg.author == ctx.author and msg.channel == msg.channel and msg.content.lower()[0] in string.printable
  await ctx.send("Title of challenge to remove: ")
  chall_title = await bot.wait_for("message", check=check)
  for profile in profiles:
    for challenge in challenges:
      if challenge["title"] == chall_title.content:
        profile.pop(f"{chall_title.content}", None)
        challenges[:] = [w for w in challenges if w.get("title") != f"{chall_title.content}"]
  await ctx.send("Challenge removed!")
  with open("challenges.json", "w") as w:
    json.dump(challenges, w)
  with open("profiles.json", "w") as w:
    json.dump(profiles, w)

@bot.command(name="leaderboard", aliases=['lb'])
@commands.guild_only()
async def leaderboard(ctx):
  with open("profiles.json") as w:
    profiles = json.load(w)
  pointslist = []
  for profile in profiles:
    pointslist.append({"name": profile['name'], "points": profile['points']})
  pointslist = sorted(pointslist, key = lambda i: i['points'],reverse=True)
  embed = discord.Embed(title="Leaderboard", color=0x00FFFF)
  lb_string = ""
  for i in range(len(pointslist)):
    lb_string += f"{i+1}) **{pointslist[i]['name']}** - {pointslist[i]['points']} points\n"
  embed.add_field(name="\u200b", value=lb_string)
  embed.set_thumbnail(url="https://avatars.githubusercontent.com/u/86629756?s=400&u=6923f73c46cf0f9ac047bdceda49d8cb4df0a844&v=4")
  return await ctx.send(embed=embed)

bot.run("no")
