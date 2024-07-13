import asyncio
from typing import Final
import os

import discord
from discord import Intents
from discord.ext import commands
from dotenv import load_dotenv
from TwentyNaejeon import make_twenty_naejeon, magam_twenty_naejeon, jjong_twenty_naejeon
from FourtyNaejeon import make_fourty_naejeon, magam_fourty_naejeon, jjong_fourty_naejeon
from Naejeon import make_normal_naejeon, magam_normal_naejeon, jjong_normal_naejeon
from MessageCommand import checkMessage

# env 파일 변수 불러오기
load_dotenv()
TOKEN: Final[str] = os.getenv('DISCORD_TOKEN')
TEST_CHANNEL_ID: Final[str] = os.getenv('TEST_CHANNEL_ID')
TWENTY_CHANNEL_ID: Final[str] = os.getenv('TWENTY_CHANNEL_ID')
FOURTY_CHANNEL_ID: Final[str] = os.getenv('FOURTY_CHANNEL_ID')
NAEJEON_A_CHANNEL_ID: Final[str] = os.getenv('NAEJEON_A_CHANNEL_ID')
NAEJEON_B_CHANNEL_ID: Final[str] = os.getenv('NAEJEON_B_CHANNEL_ID')
NAEJEON_C_CHANNEL_ID: Final[str] = os.getenv('NAEJEON_C_CHANNEL_ID')
NAEJEON_D_CHANNEL_ID: Final[str] = os.getenv('NAEJEON_D_CHANNEL_ID')
NAEJEON_EMERALD_CHANNEL_ID: Final[str] = os.getenv('NAEJEON_EMERALD_CHANNEL_ID')
NAEJEON_DIAMOND_CHANNEL_ID: Final[str] = os.getenv('NAEJEON_DIAMOND_CHANNEL_ID')

# 디스코드 봇 설정 (뭔지 모름 ㅇㅅㅇ)
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

#40인 내전 진행 여부
is_fourty_naejeon = False

#긴급
fourty_jikjak_flag = True

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

@bot.command(name='내전')
async def make_naejeon(ctx, *, message = '모이면 바로 시작'):
    global is_naejeon, is_emerald_naejeon, is_twenty_naejeon, is_fourty_naejeon, naejeon_log, emerald_naejeon_log, naejeon_channel

    channel_id = str(ctx.channel.id)

    if channel_id == TWENTY_CHANNEL_ID:
        if not is_twenty_naejeon:
            is_twenty_naejeon = await make_twenty_naejeon(ctx, message)

    if channel_id == FOURTY_CHANNEL_ID:
        if not is_fourty_naejeon:
            is_fourty_naejeon = await make_fourty_naejeon(ctx, message)

    if channel_id == NAEJEON_A_CHANNEL_ID  or channel_id == TEST_CHANNEL_ID or channel_id == NAEJEON_B_CHANNEL_ID or channel_id == NAEJEON_C_CHANNEL_ID or channel_id == NAEJEON_D_CHANNEL_ID:
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
    global is_naejeon, is_emerald_naejeon, is_twenty_naejeon, is_fourty_naejeon, naejeon_log, emerald_naejeon_log, naejeon_channel

    channel_id = str(ctx.channel.id)

    if channel_id == TWENTY_CHANNEL_ID or channel_id == TEST_CHANNEL_ID:
        if is_twenty_naejeon:
            is_twenty_naejeon = await magam_twenty_naejeon(ctx)

    if channel_id == FOURTY_CHANNEL_ID:
        if is_fourty_naejeon:
            is_fourty_naejeon = await magam_fourty_naejeon(ctx)

    if channel_id == naejeon_channel  or channel_id == TEST_CHANNEL_ID:
        if is_naejeon:
            is_naejeon = await magam_normal_naejeon(ctx, naejeon_log)
            if not is_naejeon:
                naejeon_log = None
                naejeon_channel = None

    if channel_id == NAEJEON_EMERALD_CHANNEL_ID:
        if is_emerald_naejeon:
            is_emerald_naejeon = await magam_normal_naejeon(ctx, emerald_naejeon_log)
            if not is_emerald_naejeon:
                emerald_naejeon_log = None


@bot.command(name='쫑')
async def jjong_naejeon(ctx):
    global is_naejeon, is_emerald_naejeon, is_twenty_naejeon, is_fourty_naejeon, naejeon_log, emerald_naejeon_log, naejeon_channel

    channel_id = str(ctx.channel.id)

    if channel_id == TWENTY_CHANNEL_ID:
        if is_twenty_naejeon:
            is_twenty_naejeon = await jjong_twenty_naejeon(ctx)

    if channel_id == FOURTY_CHANNEL_ID:
        if is_fourty_naejeon:
            is_fourty_naejeon = await jjong_fourty_naejeon(ctx)

    if channel_id == naejeon_channel:
        if is_naejeon:
            is_naejeon = await jjong_normal_naejeon(ctx)
            if not is_naejeon:
                naejeon_log = None
                naejeon_channel = None

    if channel_id == NAEJEON_EMERALD_CHANNEL_ID:
        if is_emerald_naejeon:
            is_emerald_naejeon = await jjong_normal_naejeon(ctx)
            if not is_emerald_naejeon:
                emerald_naejeon_log = None

@bot.event
async def on_message(message):
    # 메세지 입력 시 마다 수행
    global is_naejeon, is_emerald_naejeon, naejeon_log, emerald_naejeon_log, naejeon_channel

    channel_id = str(message.channel.id)

    # 봇 메세지는 메세지로 인식 X
    if message.author == bot.user:
        return

    # 내전이 열려 있을 경우, 손 든 사람 모집
    if is_naejeon and channel_id == naejeon_channel:
        naejeon_log.append({
            'id': message.id,
            'name': message.author.display_name,
        })

    # 에메랄드 내전도 위와 동일하게 진행
    if is_emerald_naejeon and channel_id == NAEJEON_EMERALD_CHANNEL_ID:
        emerald_naejeon_log.append({
            'id': message.id,
            'name': message.author.display_name,
        })

    msg = checkMessage(message.content)

    # 명령어 체크
    if msg:
        await message.channel.send(msg)
    else:
        await bot.process_commands(message)

@bot.event
async def on_message_delete(message):
    # 메세지 삭제 시 마다 수행
    global is_naejeon, is_emerald_naejeon, naejeon_log, emerald_naejeon_log, naejeon_channel

    channel_id = str(message.channel.id)

    # 내전 모집에서 채팅 지우면 로그에서 삭제
    if is_naejeon and channel_id == naejeon_channel:
        naejeon_log = [log for log in naejeon_log if log['id'] != message.id]

    if is_emerald_naejeon and channel_id == NAEJEON_EMERALD_CHANNEL_ID:
        emerald_naejeon_log = [log for log in emerald_naejeon_log if log['id'] != message.id]

@bot.command(name='비상비상종료종료')
@commands.has_permissions(administrator=True)
async def shutdown(ctx):
    # 디스코드에서 봇 종료를 위한 명령어
    await ctx.send("BYE BYE")
    await bot.close()

def main() -> None:
    bot.run(token=TOKEN)

if __name__ == '__main__':
    main()
