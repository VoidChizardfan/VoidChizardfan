import discord
from discord.ext import commands
from flask import Flask
from threading import Thread

# Configuration du bot Discord
intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

# Définition des rôles et des canaux
mod_role_name = 'Chief Mod'
ticket_category_name = 'Modmail Tickets'
bug_fix_channel_id = 1242866751998525481

role_ids = {
    'Owner': 1234259771532509225,
    'Admins': 1232350098516873296,
    'Chief Mod': 1236386209480052737,
    'Moderators': 1234245705426669628,
    'Tempo Mod': 1235602782535549032
}

# Flask pour garder le bot en ligne
app = Flask('')

@app.route('/')
def home():
    return "Hello. I am alive!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# Événement on_ready
@bot.event
async def on_ready():
    print(f'Bot is online as {bot.user}')
    channel = bot.get_channel(bug_fix_channel_id)
    if channel:
        await channel.send('Colette is now online and ready to assist!')

# Gestion des messages directs
@bot.event
async def on_message(message):
    if isinstance(message.channel, discord.DMChannel) and message.author != bot.user:
        response = ("Hello, I am Colette the servant modmail of the Blue Army, thank you for opening a ticket. "
                    "Please wait for one of the moderation members to take note of your message and respond to you within 5 minutes. "
                    "If you want to close your ticket, reply to my message. Thank you for your collaboration and your patience. "
                    "Please reply to my message to close your ticket!")
        await message.author.send(response)
    await bot.process_commands(message)

# Commandes Discord
@bot.command()
@commands.has_role(mod_role_name)
async def close(ctx):
    if ctx.channel.category and ctx.channel.category.name == ticket_category_name:
        await ctx.channel.delete()

@bot.command()
@commands.has_role(mod_role_name)
async def reject(ctx, user: discord.Member, *, reason):
    await user.send(f'Your ticket has been rejected for the following reason: {reason}')
    await ctx.channel.delete()

@bot.command()
@commands.has_role(mod_role_name)
async def confirm(ctx, user: discord.Member):
    await user.send('Your ticket has been accepted. A moderator will assist you shortly.')
    await ctx.channel.delete()

@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, user: discord.Member, *, reason=None):
    await user.ban(reason=reason)
    invite = await ctx.channel.create_invite(max_uses=1, unique=True)
    await user.send(f'You have been banned for the following reason: {reason}. Here is an invite to rejoin the server if necessary: {invite}')

# Démarrage du serveur web Flask et du bot Discord
keep_alive()
bot.run('YOUR_BOT_TOKEN')
