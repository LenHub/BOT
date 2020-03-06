import discord
from discord.ext import commands, tasks
from datetime import datetime
import asyncio

def read_token():
    with open('token.txt','r') as t:
        line = t.readline()
        return line.strip()


client = commands.Bot(command_prefix= '!')

messages = joined = invites = chan = 0

async def update_stats():
    await client.wait_until_ready()
    global messages, joined, invites,chan
    date = datetime.now().strftime("%d/%m/%Y %H") + 'h'
    while not client.is_closed():
        try:
            with open("stats.txt",'a') as f:
                f.write("{} Nouveaux membres: {} Messages: {} Vocaux: {} Invitations: {}\n".format(date,joined,messages,chan,invites))
            messages = joined = invites = chan = 0
            await asyncio.sleep(3600)
        except Exception as e:
            print(e)
            await asyncio.sleep(10)

@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.online, activity=discord.Game('surveiller le serveur'))
    print('Bot en ligne')

@client.event
async def on_message(message):
    global messages
    messages+=1
    await client.process_commands(message)

@client.event
async def on_invite_create(invite):
    global invites
    invites+=1

@client.event
async def on_groupe_join(channel,user):
    global chan
    chan+=1

@client.event
async def on_member_join(member):
    global joined
    joined += 1

@client.event
async def on_member_remove(member):
    global joined
    joined -= 1

@client.command()
async def ping(ctx):
    await ctx.send("Pong! {}ms".format(round(client.latency*1000)))


token = read_token()

client.loop.create_task(update_stats())
client.run(token)
