import discord
from discord.ext import commands
import json

intents = discord.Intents.all()

bot = commands.Bot(command_prefix='!', intents=intents)
bot_token = "" # Your Bot Token
owner_id = 111111111111111 # Owner ID

with open('sites.json', 'r') as file:
    blocked_sites = json.load(file)

@bot.event
async def on_ready():
    print(f'[+] Bot connected as {bot.user.name}')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if any(site in message.content for site in blocked_sites):
        await message.delete()
        embed = discord.Embed(title="Blocked Site Detected", description=f"`🚫` {message.author.mention}, your message contains a blocked site.", color=discord.Color.red())
        await message.channel.send(embed=embed)

    await bot.process_commands(message)

@bot.command()
async def block(ctx, site):
    if ctx.author.id == owner_id:
        if site not in blocked_sites:
            blocked_sites.append(site)
            update_blocked_sites()
            embed = discord.Embed(title="Site Blocked Successfully", description=f"`✅` The site `https://{site}/` has been added to the list of blocked sites.", color=discord.Color.green())
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title="Site Already Blocked", description=f"`❌` The site `https://{site}/` is already in the list of blocked sites.", color=discord.Color.red())
            await ctx.send(embed=embed)
    else:
        embed = discord.Embed(title="Permission Denied", description="`🚫` You don't have permission to use this command.", color=discord.Color.red())
        await ctx.send(embed=embed)


@bot.command()
async def blocked(ctx):
    blocked_sites_formatted = '\n'.join(f"https://{site}" for site in blocked_sites)
    embed = discord.Embed(title="`🤖` List of Blocked Sites", description=f"```\n{blocked_sites_formatted}```", color=discord.Color.blue())
    await ctx.send(embed=embed)

def update_blocked_sites():
    with open('sites.json', 'w') as file:
        json.dump(blocked_sites, file)

bot.run(bot_token)
