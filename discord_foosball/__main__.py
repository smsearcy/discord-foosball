"""Discord bot to help facilitate foosball games."""
import asyncio
import random

import discord

from .config import config

client = discord.Client()


async def roll_dice(message: discord.Message):
    dice_roll = random.randint(1, 20)
    roller = message.author.nick or message.author.name
    response = f'{roller} rolled a {dice_roll}'
    await client.send_message(message.channel, response)


COMMAND_MAP = {
    'roll': roll_dice,
}


@client.event
async def on_ready():
    print(f'Logged in as {client.user.name} ({client.user.id})')
    print('------')
    print(f'Command prefix is "{config.command_prefix}"')


@client.event
async def on_message(message):
    """Process messages sent to the channel."""
    if not message.content.startswith(config.command_prefix):
        return

    command = message.content[1:].split()[0]

    await COMMAND_MAP[command](message)

    # if message.content.startswith('!test'):
    #     counter = 0
    #     tmp = await client.send_message(message.channel, 'Calculating messages...')
    #     async for log in client.logs_from(message.channel, limit=100):
    #         if log.author == message.author:
    #             counter += 1
    #
    #     await client.edit_message(tmp, 'You have {} messages.'.format(counter))
    # elif message.content.startswith('!sleep'):
    #     await asyncio.sleep(5)
    #     await client.send_message(message.channel, 'Done sleeping')


client.run(config.token)
