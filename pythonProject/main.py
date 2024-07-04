import asyncio
from typing import Final
import os

from discord import Intents, Client, Message
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN: Final[str] = os.getenv('DISCORD_TOKEN')

intents: Intents = Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

recording = False
recording_channel = None
message_log = []

def sort_participants(participants: set):
    challenger_users = list()
    grandmaster_users = list()
    master_users = list()
    diamond_users = list()
    emerald_users = list()
    platinum_users = list()
    gold_users = list()
    silver_users = list()
    bronze_users = list()
    iron_users = list()
    unranked_users = list()

    for user in participants:
        splitted_user_profile = user.split('/')
        user_tier_non_strip = splitted_user_profile[1]
        user_tier = user_tier_non_strip.strip()

        user_level = user_tier[0].upper()

        if user_level == 'C':
            user_score = int(user_tier[1:])
            challenger_users.append((user_score,user))

        if user_level == 'G' and user_tier[1].upper() == 'M':
            user_score = int(user_tier[2:])
            grandmaster_users.append((user_score,user))

        if user_level == 'M':
            user_score = int(user_tier[1:])
            master_users.append((user_score,user))

        if user_level == 'D':
            user_score = int(user_tier[1:])
            diamond_users.append((user_score,user))

        if user_level == 'E':
            user_score = int(user_tier[1:])
            emerald_users.append((user_score,user))

        if user_level == 'P':
            user_score = int(user_tier[1:])
            platinum_users.append((user_score,user))

        if user_level == 'G' and user_tier[1].upper() != 'M':
            user_score = int(user_tier[1:])
            gold_users.append((user_score,user))

        if user_level == 'S':
            user_score = int(user_tier[1:])
            silver_users.append((user_score,user))

        if user_level == 'B':
            user_score = int(user_tier[1:])
            bronze_users.append((user_score,user))

        if user_level == 'I':
            user_score = int(user_tier[1:])
            iron_users.append((user_score,user))

        if user_level == 'U':
            user_score = 0
            unranked_users.append((user_score,user))

    user_result = list()

    if challenger_users:
        challenger_users.sort(key=lambda pair: pair[0], reverse=True)
        for user in challenger_users:
            user_result.append(user[1])
        user_result.append('')

    if grandmaster_users:
        grandmaster_users.sort(key=lambda pair: pair[0], reverse=True)
        for user in grandmaster_users:
            user_result.append(user[1])
        user_result.append('')

    if master_users:
        master_users.sort(key=lambda pair: pair[0], reverse=True)
        for user in master_users:
            user_result.append(user[1])
        user_result.append('')

    if diamond_users:
        diamond_users.sort(key=lambda pair: pair[0])
        for user in diamond_users:
            user_result.append(user[1])
        user_result.append('')

    if emerald_users:
        emerald_users.sort(key=lambda pair: pair[0])
        for user in emerald_users:
            user_result.append(user[1])
        user_result.append('')

    if platinum_users:
        platinum_users.sort(key=lambda pair: pair[0])
        for user in platinum_users:
            user_result.append(user[1])
        user_result.append('')

    if gold_users:
        gold_users.sort(key=lambda pair: pair[0])
        for user in gold_users:
            user_result.append(user[1])
        user_result.append('')

    if silver_users:
        silver_users.sort(key=lambda pair: pair[0])
        for user in silver_users:
            user_result.append(user[1])
        user_result.append('')

    if bronze_users:
        bronze_users.sort(key=lambda pair: pair[0])
        for user in bronze_users:
            user_result.append(user[1])
        user_result.append('')

    if unranked_users:
        for user in unranked_users:
            user_result.append(user[1])
        user_result.append('')

    result = ''
    result += f'=========================================\n\n'
    for users in user_result:
        result += f'{users}\n'
    result += f'=========================================\n'

    return result

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

@bot.command(name='내전')
async def start_game(ctx, *, message='모바시'):
    global recording, message_log, recording_channel
    if recording == False:
        recording = True
        recording_channel = ctx.channel
        message_log = []
        await ctx.send(f'@everyone 내전 {message}')
    else:
        await ctx.send('이미 내전이 열려 있습니다. 기존의 내전을 마감하고 진행해주세요.')

@bot.command(name='마감')
async def end_game(ctx):
    global recording, message_log, recording_channel
    if recording == True:
        recording = False
        participants = set()

        for log in message_log:
            participants.add(log['author'])

        if participants:
            participants_result = sort_participants(participants)

            await ctx.send(f'@everyone 내전 모집이 마감되었습니다. 모두 모여주세요.')
            await ctx.send(participants_result)
        else:
            await ctx.send('의도치 않은 오류가 발생했습니다.')
    else:
        await ctx.send('아직 내전이 실행되지 않았습니다. !내전으로 내전을 열어주세요.')

@bot.command(name='쫑')
async def jjong_game(ctx):
    global recording, message_log, recording_channel
    if recording == True:
        recording = False
        message_log = []
        recording_channel = None
        await ctx.send(f'@everyone 쫑')


@bot.event
async def on_message(message):
    global recording, participants

    if message.author == bot.user:
        return

    if recording and message.channel == recording_channel:
        message_log.append({
            'id': message.id,
            'author': message.author.display_name,
            'content': message.content,
            'timestamp': message.created_at
        })

    await bot.process_commands(message)

@bot.command(name='권기현')
async def ddolddol(ctx):
    await ctx.send(f'날쌔지 않음')

@bot.command(name='절구')
async def ddolddol(ctx):
    await ctx.send(f'절구통')

@bot.event
async def on_message_delete(message):
    global recording, recording_channel, message_log

    if recording and message.channel == recording_channel:
        message_log = [log for log in message_log if log['id'] != message.id]

@bot.command(name='마술사봇긴급종료')
@commands.has_permissions(administrator=True)
async def shutdown(ctx):
    await ctx.send("긴급탈출")
    await bot.close()

def main() -> None:
    bot.run(token=TOKEN)

if __name__ == '__main__':
    main()
