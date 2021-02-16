#!/usr/bin/env python3
import discord
from secrets import token

client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    
    if message.content == 'ping':
        await message.channel.send('pong')

client.run(token)
