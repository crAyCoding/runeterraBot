import os

import Runeterra

from discord import Intents
from discord.ext import commands

from TwentyAuction import add_user_list_by_own, confirm_twenty_recruit
from TwentyGame import *
from FortyGame import make_fourty_game, magam_fourty_game, jjong_fourty_game
from NormalGame import make_normal_game, close_normal_game, end_normal_game
from MessageCommand import check_message

# GitHub Secrets에서 가져오는 값
TOKEN = os.getenv('DISCORD_TOKEN')

# 디스코드 봇 설정
intents: Intents = Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')


@bot.command(name='내전')
async def make_game(ctx, *, message='모이면 바로 시작'):
    # await ctx.send("현재 수습 마술사 작업중 입니다. 수동으로 내전 진행해주시면 감사하겠습니다.")
    # return None

    channel_id = str(ctx.channel.id)
    normal_channel_id_list = [Runeterra.GAME_A_CHANNEL_ID, Runeterra.GAME_B_CHANNEL_ID,
                              Runeterra.GAME_C_CHANNEL_ID, Runeterra.GAME_D_CHANNEL_ID]

    if channel_id == Runeterra.TWENTY_RECRUIT_CHANNEL_ID and not Runeterra.is_twenty_game:
        Runeterra.is_twenty_game = await make_twenty_game(ctx, message)

    if channel_id == Runeterra.FORTY_RECRUIT_CHANNEL_ID and not Runeterra.is_forty_game:
        Runeterra.is_forty_game = await make_fourty_game(ctx, message)

    if channel_id in normal_channel_id_list and not Runeterra.is_normal_game:
        Runeterra.is_normal_game = await make_normal_game(ctx, message)

    if channel_id in Runeterra.SPECIAL_GAME_CHANNEL_ID_LIST:
        await make_normal_game(ctx, message)

    if channel_id == Runeterra.TEST_BY_OWN_CHANNEL_ID:
        Runeterra.is_normal_game = await make_normal_game(ctx)

@bot.command(name='마감')
async def close_game(ctx):
    channel_id = str(ctx.channel.id)

    if channel_id == Runeterra.TWENTY_RECRUIT_CHANNEL_ID and Runeterra.is_twenty_game:
        Runeterra.is_twenty_game = await close_twenty_game(ctx)

    if channel_id == Runeterra.FORTY_RECRUIT_CHANNEL_ID and Runeterra.is_forty_game:
        Runeterra.is_forty_game = await magam_fourty_game(ctx)


@bot.command(name='쫑')
async def end_game(ctx):
    channel_id = str(ctx.channel.id)

    normal_channel_id_list = [Runeterra.GAME_A_CHANNEL_ID, Runeterra.GAME_B_CHANNEL_ID,
                              Runeterra.GAME_C_CHANNEL_ID, Runeterra.GAME_D_CHANNEL_ID]

    if channel_id == Runeterra.TWENTY_RECRUIT_CHANNEL_ID and Runeterra.is_twenty_game:
        Runeterra.is_twenty_game = await end_twenty_game(ctx)

    if channel_id == Runeterra.FORTY_RECRUIT_CHANNEL_ID and Runeterra.is_forty_game:
        Runeterra.is_forty_game = await jjong_fourty_game(ctx)

    if channel_id in normal_channel_id_list and Runeterra.is_normal_game:
        Runeterra.normal_game_log = None
        Runeterra.normal_game_channel = None
        Runeterra.is_normal_game = await end_normal_game(ctx)


# 메세지 입력 시 마다 수행
@bot.event
async def on_message(message):
    channel_id = str(message.channel.id)

    # 봇 메세지는 메세지로 인식 X
    if message.author == bot.user:
        return

    # 내전이 열려 있을 경우, 손 든 사람 모집
    if Runeterra.is_normal_game and channel_id == Runeterra.normal_game_channel:
        user = Runeterra.DiscordUser(message.author.id, message.author.display_name)
        if user in Runeterra.normal_game_log:
            Runeterra.normal_game_log[user].append(message.id)
        else:
            Runeterra.normal_game_log[user] = [message.id]
        # 참여자 수가 10명이면 내전 자동 마감
        if len(Runeterra.normal_game_log) == 10:
            await close_normal_game(message.channel, Runeterra.normal_game_log.keys())
            # 내전 변수 초기화
            Runeterra.normal_game_log = None
            Runeterra.normal_game_channel = None
            Runeterra.is_normal_game = False
        print(Runeterra.normal_game_log)

    msg = check_message(message.content)

    # 명령어 체크
    if msg:
        await message.channel.send(msg)
    else:
        await bot.process_commands(message)


# 메세지 삭제 시 마다 수행
@bot.event
async def on_message_delete(message):
    channel_id = str(message.channel.id)
    user = Runeterra.DiscordUser(message.author.id, message.author.display_name)

    # 내전 모집에서 채팅 지우면 로그에서 삭제
    if Runeterra.is_normal_game and channel_id == Runeterra.normal_game_channel:
        Runeterra.normal_game_log[user] = [mid for mid in Runeterra.normal_game_log[user] if mid != message.id]


@bot.command(name='비상탈출')
@commands.is_owner()
async def shutdown(ctx):
    # 디스코드에서 봇 종료를 위한 명령어
    await ctx.send("BYE")
    await bot.close()


@bot.command(name='경매')
async def twenty_auction(ctx):
    channel_id = str(ctx.channel.id)

    if channel_id == Runeterra.TWENTY_AUCTION_CHANNEL_ID:
        await confirm_twenty_recruit(ctx)


@bot.command(name='수동경매')
async def twenty_auction_by_own(ctx):
    await add_user_list_by_own(ctx)


@bot.command(name='테스트')
async def test_only_def(ctx):
    # await confirm_forty_recruit(ctx)
    return None


@bot.command(name='초기화')
async def reset_game(ctx):
    channel_id = str(ctx.channel.id)
    user_id = str(ctx.author.id)

    normal_channel_id_list = [Runeterra.GAME_A_CHANNEL_ID, Runeterra.GAME_B_CHANNEL_ID,
                              Runeterra.GAME_C_CHANNEL_ID, Runeterra.GAME_D_CHANNEL_ID]

    if user_id != Runeterra.SORCERER:
        await ctx.send('개발자만 가능해요~ 안돼요~ 돌아가요~')
        return None

    if channel_id in normal_channel_id_list:
        Runeterra.is_normal_game = False
        Runeterra.normal_game_log = None
        Runeterra.normal_game_channel = None
        await ctx.send("일반 내전을 초기화했습니다.")

    if channel_id == Runeterra.TWENTY_RECRUIT_CHANNEL_ID:
        Runeterra.is_twenty_game = False
        Runeterra.auction_host = None
        reset_twenty_game(ctx)
        await ctx.send('20인 내전을 초기화했습니다.')

    if channel_id == Runeterra.FORTY_RECRUIT_CHANNEL_ID:
        Runeterra.is_forty_game = False
        Runeterra.auction_host = None
        # reset_forty_game(ctx)
        await ctx.send('40인 내전을 초기화했습니다.')

def main() -> None:
    bot.run(token=TOKEN)


if __name__ == '__main__':
    main()
