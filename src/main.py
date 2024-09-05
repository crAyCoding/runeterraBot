from typing import Final
import os
import sys

from discord import Intents
from discord.ext import commands
from discord.ui import Modal
from dotenv import load_dotenv

from TwentyAuction import run_twenty_auction, add_user_list_by_own, confirm_twenty_recruit
from TwentyNaejeon import *
from FourtyNaejeon import make_fourty_naejeon, magam_fourty_naejeon, jjong_fourty_naejeon
from Naejeon import make_normal_naejeon, magam_normal_naejeon, jjong_normal_naejeon
from SortFunctions import sort_naejeon_members, get_result_sorted_by_tier
from MessageCommand import checkMessage

# env 파일 변수 불러오기
load_dotenv()
TOKEN: Final[str] = os.getenv('DISCORD_TOKEN')
TEST_CHANNEL_ID: Final[str] = os.getenv('TEST_CHANNEL_ID')
TEST2_CHANNEL_ID: Final[str] = os.getenv('TEST2_CHANNEL_ID')
TWENTY_CHANNEL_ID: Final[str] = os.getenv('TWENTY_CHANNEL_ID')
FOURTY_CHANNEL_ID: Final[str] = os.getenv('FOURTY_CHANNEL_ID')
NAEJEON_A_CHANNEL_ID: Final[str] = os.getenv('NAEJEON_A_CHANNEL_ID')
NAEJEON_B_CHANNEL_ID: Final[str] = os.getenv('NAEJEON_B_CHANNEL_ID')
NAEJEON_C_CHANNEL_ID: Final[str] = os.getenv('NAEJEON_C_CHANNEL_ID')
NAEJEON_D_CHANNEL_ID: Final[str] = os.getenv('NAEJEON_D_CHANNEL_ID')
NAEJEON_EMERALD_CHANNEL_ID: Final[str] = os.getenv('NAEJEON_EMERALD_CHANNEL_ID')
NAEJEON_DIAMOND_CHANNEL_ID: Final[str] = os.getenv('NAEJEON_DIAMOND_CHANNEL_ID')
TWENTY_NAEJEON_AUCTION_CHANNEL_ID: Final[str] = os.getenv('TWENTY_NAEJEON_AUCTION_CHANNEL_ID')

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

#20인 내전 관련
is_twenty_naejeon = False
auction_host = None

#40인 내전 진행 여부
is_fourty_naejeon = False

#긴급
fourty_jikjak_flag = True
test_var = None


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

@bot.command(name='내전')
async def make_naejeon(ctx, *, message = '모이면 바로 시작'):
    global is_naejeon, is_emerald_naejeon, is_twenty_naejeon, is_fourty_naejeon, naejeon_log, emerald_naejeon_log, naejeon_channel

    await ctx.send("현재 수습 마술사 작업 중입니다. 수동으로 내전 진행해주시면 감사하겠습니다.")
    return None

    channel_id = str(ctx.channel.id)

    if channel_id == TWENTY_CHANNEL_ID:
        if not is_twenty_naejeon:
            is_twenty_naejeon = await make_twenty_naejeon(ctx, message)

    if channel_id == FOURTY_CHANNEL_ID:
        if not is_fourty_naejeon:
            is_fourty_naejeon = await make_fourty_naejeon(ctx, message)

    if channel_id == NAEJEON_A_CHANNEL_ID or channel_id == NAEJEON_B_CHANNEL_ID or channel_id == NAEJEON_C_CHANNEL_ID or channel_id == NAEJEON_D_CHANNEL_ID:
        if not is_naejeon:
            naejeon_log = []
            naejeon_log.append({'id':ctx.author.id,'name':ctx.author.display_name})
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

    if channel_id == TWENTY_CHANNEL_ID:
        if is_twenty_naejeon:
            is_twenty_naejeon = await magam_twenty_naejeon(ctx)

    if channel_id == FOURTY_CHANNEL_ID:
        if is_fourty_naejeon:
            is_fourty_naejeon = await magam_fourty_naejeon(ctx)

    if channel_id == naejeon_channel or channel_id == TEST2_CHANNEL_ID:
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

        participants = set()

        for log in naejeon_log:
            participants.add(log['name'])

        if len(participants) == 10:

            await magam_normal_naejeon(message.channel, list(participants))

            naejeon_log = None
            naejeon_channel = None
            is_naejeon = False


    # 에메랄드 내전도 위와 동일하게 진행
    if is_emerald_naejeon and channel_id == NAEJEON_EMERALD_CHANNEL_ID:
        emerald_naejeon_log.append({
            'id': message.id,
            'name': message.author.display_name,
        })

        participants = set()

        for log in emerald_naejeon_log:
            participants.add(log['name'])

        if len(participants) == 10:
            user_result = sort_naejeon_members(participants)

            result = ''
            result += f'=========================================\n\n'
            for users in user_result:
                result += f'{users}\n'
            result += f'\n=========================================\n'

            await message.channel.send(f'@everyone 내전 모집이 마감되었습니다. 모두 모여주세요.')
            await message.channel.send(result)

            emerald_naejeon_log = None
            is_emerald_naejeon = False


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

@bot.command(name='비상탈출')
@commands.has_permissions(administrator=True)
async def shutdown(ctx):
    # 디스코드에서 봇 종료를 위한 명령어
    await ctx.send("BYE")
    await bot.close()

@bot.command(name='재부팅')
@commands.is_owner()
async def reboot(ctx):
    await ctx.send("Rebooting bot...")
    await bot.close()
    os.execv(sys.executable, ['python'] + sys.argv)

@bot.command(name='경매')
async def twenty_auction_naejeon(ctx):
    channel_id = str(ctx.channel.id)

    if channel_id == TWENTY_NAEJEON_AUCTION_CHANNEL_ID:
        await confirm_twenty_recruit(ctx)

@bot.command(name='수동경매')
async def test_test(ctx):
    await add_user_list_by_own(ctx)


@bot.command(name='테스트')
async def test_only_def(ctx):
    # participants = ['순간번쩍#KR1 / M20 / TOP','FERRERO0#KR1 / E3 / TOP','마술사의 수습생 #KR1 / D1 / AD','메벤남#쌀숭이 / D3 /JG,TOP,SUP','엄마가만든카레 #KR1 / E1 / MID','This is Attacker #KR1 / E1 / AD','뭘by녀석아 #KR1 / E3 / AD, 제육','피자시켜놓고피클만쳐먹는성수#Pizza/M195 / ALL','쥬 예 #0410 / D2 / ALL','Lo fi #RELAX/ D2 /SUP,AD']
    # with open('./naejeonex.txt', 'r', encoding='utf-8') as file:
    #     lines = [line.strip() for line in file.readlines()]
    #     for i in range(10):
    #         participants.append(lines[i])


    await make_twenty_naejeon(ctx, '아잉')

    await test_add_twenty()

@bot.command(name='테스트경매')
async def test_auction(ctx):
    await confirm_twenty_recruit(ctx)


@bot.command(name='내전초기화')
async def reset_naejeon(ctx):
    global is_naejeon, naejeon_log, naejeon_channel

    user_id = ctx.author.id

    if user_id != 333804390332760064:
        await ctx.send('개발자만 가능해요~ 안돼요~ 돌아가요~')
        return None

    is_naejeon = False
    naejeon_log = None
    naejeon_channel = None

    await ctx.send("일반 내전을 초기화시켰습니다.")

@bot.command(name='20인내전초기화')
async def reset_twenty(ctx):
    global is_twenty_naejeon, auction_host

    channel_id = str(ctx.channel.id)
    user_id = ctx.author.id

    if channel_id != TWENTY_CHANNEL_ID:
        return None

    if user_id != 333804390332760064:
        await ctx.send('개발자만 가능해요~ 안돼요~ 돌아가요~')
        return None

    is_twenty_naejeon = False
    auction_host = None

    reset_twenty_naejeon(ctx)
    await ctx.send('20인 내전을 초기화하였습니다.')


def main() -> None:
    bot.run(token=TOKEN)

if __name__ == '__main__':
    main()
