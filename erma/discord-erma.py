#!/usr/bin/python3
#Script to bridge ERMA to discord. Make sure ERMA is running with BRIDGE_ACTIVE set to True

import os
import discord
import time
from discord.ext import commands
from dotenv import load_dotenv
from erma import wait_modified, string_save

load_dotenv()
intents = discord.Intents().all()
client = commands.Bot(command_prefix=',', intents=intents)

def start(discord_bot_token, triggers):
    """Function to start the discord bot portion.
    DISCORD_BOT_TOKEN is the discord bot token, and should be a string.
    TRIGGERS is the list of trigger phrases, and should be a list of strings"""
    @client.event
    async def on_ready():
        print('online')
    @client.event 
    async def on_message(message):
        if message.author == client.user:
            return
        if message.author.bot: return
        for i in range(len(triggers)):
            if triggers[i].lower() in message.content.lower():
                print('User input received!')
                string_save('neuralcloud_user.file', message.content) #write to USER_FILE, triggers ERMA to continue
                response = wait_modified('neuralcloud_ai.file') #then wait for AI_FILE to be written by ERMA
                print('AI response sent!')
                await message.channel.send(response)
    client.run(discord_bot_token)

start(os.getenv('DISCORD_API_KEY'), ["hey gpt"]) #change TRIGGERS as you want