import discord
from discord.ext import commands
import random
import string

# ======================
# CONFIG
# ======================
TOKEN = "YOUR_BOT_TOKEN_HERE"  # Ganti dengan token botmu
OWNER_ID = 1432668350126886958  # Discord ID kamu

# Dictionary apikey di memori
apikeys = {}  # {"ZYYRO_xxxx": "unverified" atau "verified"}

# ======================
# BOT SETUP
# ======================
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="/", intents=intents)

# ======================
# HELPERS
# ======================
def generate_apikey():
    random_part = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
    return f"ZYYRO_{random_part}"

def is_owner(ctx):
    return ctx.author.id == OWNER_ID

# ======================
# COMMANDS
# ======================

# Create new apikey
@bot.command()
async def createapikey(ctx, expire_days: int = 0):
    if not is_owner(ctx):
        await ctx.send("❌ You are not allowed to use this command!")
        return
    key = generate_apikey()
    apikeys[key] = "unverified"
    await ctx.send(f"✅ New API Key created: `{key}` (expires in {expire_days} day(s))")

# Verify apikey
@bot.command()
async def verify(ctx, key: str):
    if not is_owner(ctx):
        await ctx.send("❌ You are not allowed to use this command!")
        return
    if key in apikeys:
        apikeys[key] = "verified"
        await ctx.send(f"✅ API Key `{key}` has been verified!")
    else:
        await ctx.send(f"❌ API Key `{key}` not found!")

# Send message to a channel
@bot.command()
async def ht(ctx, channel_name: str, *, txt: str):
    if not is_owner(ctx):
        await ctx.send("❌ You are not allowed to use this command!")
        return
    channel = discord.utils.get(ctx.guild.text_channels, name=channel_name)
    if channel:
        await channel.send(f"📢 {txt}")
        await ctx.send(f"✅ Message sent to #{channel_name}")
    else:
        await ctx.send(f"❌ Channel `{channel_name}` not found!")

# ======================
# ON READY
# ======================
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} | ID: {bot.user.id}")
    print("------")

# ======================
# RUN BOT
# ======================
bot.run(TOKEN)
