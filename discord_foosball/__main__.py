"""Discord bot to help facilitate foosball games."""
import asyncio
from datetime import datetime, timedelta
from operator import attrgetter
import random
import typing as t

import attr
import discord

from .config import config

client = discord.Client()

ROLL_TIMEOUT = timedelta(seconds=config.roll_timeout)


def roll_d20():
    return random.randint(1, 20)


@attr.s(slots=True)
class DiceRoll:
    roller = attr.ib()
    result = attr.ib(factory=roll_d20)
    timestamp = attr.ib(factory=datetime.now)

    def __str__(self):
        return f'{self.roller} rolled a {self.result} at {self.timestamp:%H:%M:%S}'


CURRENT_ROLLS: t.Dict[str, DiceRoll] = {}


def purge_old_rolls():
    """Purge old rolls."""
    purge_date = datetime.now() - timedelta(seconds=config.roll_timeout * 2)
    expired_keys = [
        roller
        for roller, roll in CURRENT_ROLLS.items()
        if roll.timestamp < purge_date
    ]
    for key in expired_keys:
        del CURRENT_ROLLS[key]
    if expired_keys:
        print(f'Deleted {len(expired_keys)} rolls prior to {purge_date}')


async def print_rolls(message: discord.Message):

    summary = '\n'.join(
        str(roll)
        for roll in CURRENT_ROLLS.values()
    ) or 'No one has recently rolled.'
    await client.send_message(message.channel, summary)


async def roll_dice(message: discord.Message):
    roller = message.author.nick or message.author.name
    if roller in CURRENT_ROLLS:
        if datetime.now() - CURRENT_ROLLS[roller].timestamp <= ROLL_TIMEOUT:
            await client.send_message(
                message.channel,
                f'Sorry {roller}, you already rolled a {CURRENT_ROLLS[roller].result}'
            )
            return

    new_roll = DiceRoll(roller=roller)
    CURRENT_ROLLS[roller] = new_roll
    await client.send_message(message.channel, f'{roller} rolled a {new_roll.result}')


async def teams(message: discord.Message):
    if len(CURRENT_ROLLS) < 4:
        await client.send_message(message.channel, 'Not enough people to form teams')
        return
    sorted_rolls = sorted(CURRENT_ROLLS.values(), key=attrgetter('result'))
    team1 = ' and '.join(
        roll.roller
        for roll in sorted_rolls[:2]
    )
    team2 = ' and '.join(
        roll.roller
        for roll in sorted_rolls[-2:]
    )
    await client.send_message(message.channel, f'It is {team1} versus {team2} (ties decided by the computer)')


async def background_task():
    while True:
        await asyncio.sleep(10)
        purge_old_rolls()


COMMAND_MAP = {
    'roll': roll_dice,
    'list': print_rolls,
    'teams': teams,
}


@client.event
async def on_ready():
    print(f'Logged in as {client.user.name} ({client.user.id})')
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


client.loop.create_task(background_task())
client.run(config.token)
