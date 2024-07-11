import asyncio
from typing import Final
import os

import discord
from discord import Intents, Client, Message
from discord.ui import Button, View
from discord.ext import commands
from dotenv import load_dotenv
from SortFunctions import sort_participants, sort_twenty_members
from TierScore import get_user_tier_score
from TwentyNaejeon import make_twenty_naejeon, magam_twenty_naejeon, jjong_twenty_naejeon
from Naejeon import make_normal_naejeon, magam_normal_naejeon, jjong_normal_naejeon
from MessageCommand import checkMessage

load_dotenv()
TOKEN: Final[str] = os.getenv('DISCORD_TOKEN')
TEST_CHANNEL_ID: Final[str] = os.getenv('TEST_CHANNEL_ID')
TWENTY_CHANNEL_ID: Final[str] = os.getenv('TWENTY_CHANNEL_ID')
NAEJEON_A_CHANNEL_ID: Final[str] = os.getenv('NAEJEON_A_CHANNEL_ID')
NAEJEON_B_CHANNEL_ID: Final[str] = os.getenv('NAEJEON_B_CHANNEL_ID')
NAEJEON_C_CHANNEL_ID: Final[str] = os.getenv('NAEJEON_C_CHANNEL_ID')
NAEJEON_D_CHANNEL_ID: Final[str] = os.getenv('NAEJEON_D_CHANNEL_ID')
NAEJEON_EMERALD_CHANNEL_ID: Final[str] = os.getenv('NAEJEON_EMERALD_CHANNEL_ID')
NAEJEON_DIAMOND_CHANNEL_ID: Final[str] = os.getenv('NAEJEON_DIAMOND_CHANNEL_ID')


intents: Intents = Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

#일반 내전 관련
is_naejeon = False
naejeon_log = None
naejeon_channel = None

#에메랄드 이상 내전 진행 여부
is_emerald_naejeon = False
emerald_naejeon_log = None

#20인 내전 진행 여부
is_twenty_naejeon = False

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

@bot.command(name='내전')
async def make_naejeon(ctx, *, message = '모이면 바로 시작'):
    global is_naejeon, is_emerald_naejeon, is_twenty_naejeon, naejeon_log, emerald_naejeon_log, naejeon_channel

    channel_id = str(ctx.channel.id)

    if channel_id == TWENTY_CHANNEL_ID:
        if not is_twenty_naejeon:
            is_twenty_naejeon = await make_twenty_naejeon(ctx, message)

    if channel_id == NAEJEON_A_CHANNEL_ID or channel_id == NAEJEON_B_CHANNEL_ID or channel_id == NAEJEON_C_CHANNEL_ID or channel_id == NAEJEON_D_CHANNEL_ID or channel_id == TEST_CHANNEL_ID:
        if not is_naejeon:
            naejeon_log = []
            naejeon_channel = channel_id
            is_naejeon = await make_normal_naejeon(ctx, message)

    if channel_id == NAEJEON_EMERALD_CHANNEL_ID:
        if not is_emerald_naejeon:
            emerald_naejeon_log = []
            is_emerald_naejeon = await make_normal_naejeon(ctx, message)


@bot.command(name='마감')
async def magam_naejeon(ctx):
    global is_naejeon, is_emerald_naejeon, is_twenty_naejeon, naejeon_log, emerald_naejeon_log, naejeon_channel

    channel_id = str(ctx.channel.id)

    if channel_id == TWENTY_CHANNEL_ID or channel_id == TEST_CHANNEL_ID:
        if is_twenty_naejeon:
            is_twenty_naejeon = await magam_twenty_naejeon(ctx)

    if channel_id == naejeon_channel:
        is_naejeon = await magam_normal_naejeon(ctx, naejeon_log)
        if not is_naejeon:
            naejeon_log = None
            naejeon_channel = None

    if channel_id == NAEJEON_EMERALD_CHANNEL_ID:
        if is_emerald_naejeon:
            is_emerald_naejeon = await magam_normal_naejeon(ctx, emerald_naejeon_log)
            if not is_emerald_naejeon:
                emerald_naejeon_log = None
                is_emerald_naejeon = None


@bot.command(name='쫑')
async def jjong_naejeon(ctx):
    global is_naejeon, is_emerald_naejeon, is_twenty_naejeon, naejeon_log, emerald_naejeon_log, naejeon_channel

    channel_id = str(ctx.channel.id)

    if channel_id == TWENTY_CHANNEL_ID or channel_id == TEST_CHANNEL_ID:
        if is_twenty_naejeon:
            await jjong_twenty_naejeon(ctx)

    if channel_id == naejeon_channel:
        await jjong_normal_naejeon(ctx)
        naejeon_log = None
        naejeon_channel = None
        is_naejeon = False

    if channel_id == NAEJEON_EMERALD_CHANNEL_ID:
        if is_emerald_naejeon:
            await jjong_normal_naejeon(ctx)
            emerald_naejeon_log = None
            is_emerald_naejeon = None


@bot.event
async def on_message(message):
    global is_naejeon, is_emerald_naejeon, naejeon_log, emerald_naejeon_log

    if message.author == bot.user:
        return

    if is_naejeon:
        naejeon_log.append({
            'id': message.id,
            'name': message.author.display_name,
        })

    if is_emerald_naejeon:
        emerald_naejeon_log.append({
            'id': message.id,
            'name': message.author.display_name,
        })

    msg = checkMessage(message.content)

    if msg:
        await message.channel.send(msg)
    else:
        await bot.process_commands(message)

@bot.event
async def on_message_delete(message):
    global is_naejeon, is_emerald_naejeon, naejeon_log, emerald_naejeon_log

    if is_naejeon:
        naejeon_log = [log for log in naejeon_log if log['id'] != message.id]

    if is_emerald_naejeon:
        emerald_naejeon_log = [log for log in emerald_naejeon_log if log['id'] != message.id]

@bot.command(name='비상비상종료종료')
@commands.has_permissions(administrator=True)
async def shutdown(ctx):
    await ctx.send("BYE BYE")
    await bot.close()

def main() -> None:
    bot.run(token=TOKEN)

if __name__ == '__main__':
    main()
