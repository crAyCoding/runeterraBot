import asyncio
from typing import Final
import os

import discord
from discord import Intents, Client, Message
from discord.ui import Button, View
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

line_person = [0, 0, 0, 0, 0]
user_info = [[], [], [], [], []]
current_view = None
view_message = None

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

def sort_twenty_members(participants: list):
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
            challenger_users.append((user_score, user))

        if user_level == 'G' and user_tier[1].upper() == 'M':
            user_score = int(user_tier[2:])
            grandmaster_users.append((user_score, user))

        if user_level == 'M':
            user_score = int(user_tier[1:])
            master_users.append((user_score, user))

        if user_level == 'D':
            user_score = int(user_tier[1:])
            diamond_users.append((user_score, user))

        if user_level == 'E':
            user_score = int(user_tier[1:])
            emerald_users.append((user_score, user))

        if user_level == 'P':
            user_score = int(user_tier[1:])
            platinum_users.append((user_score, user))

        if user_level == 'G' and user_tier[1].upper() != 'M':
            user_score = int(user_tier[1:])
            gold_users.append((user_score, user))

        if user_level == 'S':
            user_score = int(user_tier[1:])
            silver_users.append((user_score, user))

        if user_level == 'B':
            user_score = int(user_tier[1:])
            bronze_users.append((user_score, user))

        if user_level == 'I':
            user_score = int(user_tier[1:])
            iron_users.append((user_score, user))

        if user_level == 'U':
            user_score = 0
            unranked_users.append((user_score, user))

    user_result = list()

    if challenger_users:
        challenger_users.sort(key=lambda pair: pair[0], reverse=True)
        for user in challenger_users:
            user_result.append(user[1])

    if grandmaster_users:
        grandmaster_users.sort(key=lambda pair: pair[0], reverse=True)
        for user in grandmaster_users:
            user_result.append(user[1])

    if master_users:
        master_users.sort(key=lambda pair: pair[0], reverse=True)
        for user in master_users:
            user_result.append(user[1])

    if diamond_users:
        diamond_users.sort(key=lambda pair: pair[0])
        for user in diamond_users:
            user_result.append(user[1])

    if emerald_users:
        emerald_users.sort(key=lambda pair: pair[0])
        for user in emerald_users:
            user_result.append(user[1])

    if platinum_users:
        platinum_users.sort(key=lambda pair: pair[0])
        for user in platinum_users:
            user_result.append(user[1])

    if gold_users:
        gold_users.sort(key=lambda pair: pair[0])
        for user in gold_users:
            user_result.append(user[1])

    if silver_users:
        silver_users.sort(key=lambda pair: pair[0])
        for user in silver_users:
            user_result.append(user[1])

    if bronze_users:
        bronze_users.sort(key=lambda pair: pair[0])
        for user in bronze_users:
            user_result.append(user[1])

    if unranked_users:
        for user in unranked_users:
            user_result.append(user[1])


    return user_result

def get_user_tier_score(user: str):
    splitted_user_profile = user.split('/')
    user_name = splitted_user_profile[0].strip()
    user_tier = splitted_user_profile[1].strip()

    user_level = user_tier[0].upper()

    result = 300

    if user_level == 'C':
        user_score = int(user_tier[1:])
        user_editted_score = (user_score // 100) * 10
        result -= user_editted_score

    if user_level == 'G' and user_tier[1].upper() == 'M':
        user_score = int(user_tier[2:])
        user_editted_score = (user_score // 100) * 10
        result -= user_editted_score

    if user_level == 'M':
        user_score = int(user_tier[1:])
        user_editted_score = (user_score // 100) * 10
        result -= user_editted_score

    if user_level == 'D':
        user_score = int(user_tier[1:])
        result += (user_score * 20)

    if user_level == 'E':
        user_score = int(user_tier[1:])
        result += 80
        result += (user_score * 20)

    if user_level == 'P':
        user_score = int(user_tier[1:])
        result += 160
        result += (user_score * 20)

    if user_level == 'G' and user_tier[1].upper() != 'M':
        user_score = int(user_tier[1:])
        result += 240
        result += (user_score * 20)

    if user_level == 'S':
        user_score = int(user_tier[1:])
        result += 320
        result += (user_score * 20)

    if user_level == 'B':
        user_score = int(user_tier[1:])
        result += 400
        result += (user_score * 20)

    if user_level == 'I':
        user_score = int(user_tier[1:])
        result += 480
        result += (user_score * 20)

    if user_level == 'U':
        result = 1000000

    return result

def get_team_head_number():
    global user_info

    min_diff = 9999999
    line_number = 0


    for i in range(len(user_info)):
        max_score = 0
        min_score = 9999999
        for user_message_info in user_info[i]:
            user = user_message_info[0]
            user_score = get_user_tier_score(user)

            if user_score > max_score:
                max_score = user_score
            if user_score < min_score:
                min_score = user_score

        diff = max_score - min_score

        if diff >= 0 and diff < min_diff:
            min_diff = diff
            line_number = i

    return line_number


def get_team_head_lineup(line_number: int):
    global user_info

    result = ''
    result += f'=========================================\n\n'

    user_result = user_info[line_number]

    for i in range(len(user_result)):
        result += f'{i+1}팀\n'
        user_score = get_user_tier_score(user_result[i][0])
        result += f'{user_result[i][0]} : {user_score}\n\n'

    result += f'========================================='

    return result

def get_twenty_user_lineup(head_line_number: int):
    global user_info

    line = ['탑','정글','미드','원딜','서폿']

    index = 1

    result = ''
    result += f'=========================================\n\n'

    for line_number in range(len(user_info)):
        if line_number == head_line_number:
            continue

        user_result = user_info[line_number]

        result += f'{line[line_number]}\n'

        for i in range(len(user_result)):
            result += f'{index}. {user_result[i][0]}\n'
            index += 1

    result += f'========================================='

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

@bot.command(name='20인내전')
async def start_twenty_game(ctx, *, message='모바시'):
    global line_person, user_info, current_view, view_message
    line = ['탑','정글','미드','원딜','서폿']

    class MyView(View):
        def __init__(self):
            super().__init__()

            top_button = Button(label=f'탑 : {line_person[0]}', style = discord.ButtonStyle.gray)
            top_button.callback = self.top_callback(top_button)

            jg_button = Button(label=f'정글 : {line_person[1]}', style=discord.ButtonStyle.gray)
            jg_button.callback = self.jg_callback(jg_button)

            mid_button = Button(label=f'미드 : {line_person[2]}', style=discord.ButtonStyle.gray)
            mid_button.callback = self.mid_callback(mid_button)

            ad_button = Button(label=f'원딜 : {line_person[3]}', style=discord.ButtonStyle.gray)
            ad_button.callback = self.ad_callback(ad_button)

            sup_button = Button(label=f'서폿 : {line_person[4]}', style=discord.ButtonStyle.gray)
            sup_button.callback = self.sup_callback(sup_button)

            self.add_item(top_button)
            self.add_item(jg_button)
            self.add_item(mid_button)
            self.add_item(ad_button)
            self.add_item(sup_button)
        def top_callback(self, button):
            line_number = 0
            line_name = line[line_number]
            async def callback(interaction: discord.Interaction):
                username = interaction.user.display_name
                flag = True
                for i in range(len(user_info[line_number])):
                    if user_info[line_number][i][0] == username:
                        line_person[line_number] -= 1
                        original_message = await interaction.channel.fetch_message(user_info[line_number][i][1])
                        await original_message.delete()
                        del user_info[line_number][i]
                        flag = False

                for i in range(len(user_info)):
                    if i == line_number:
                        continue
                    for j in range(len(user_info[i])):
                        if user_info[i][j][0] == username:
                            flag = False

                if flag:
                    line_person[line_number] += 1
                    if line_person[line_number] >= 4:
                        await ctx.send(f'{username} 님이 {line_name}으로 대기합니다. (대기는 아직 개발 중입니다...) ')
                    else:
                        message = await ctx.send(f'{username} 님이 {line_name}으로 참여합니다!')
                        user_info[line_number].append((username,message.id))


                button.label = f"{line_name} : {line_person[line_number]}"
                if(line_person[line_number] >= 4):
                    button.style = discord.ButtonStyle.red
                else:
                    button.style = discord.ButtonStyle.gray

                await interaction.response.edit_message(view=self)

            return callback
        def jg_callback(self, button):
            line_number = 1
            line_name = line[line_number]

            async def callback(interaction: discord.Interaction):
                username = interaction.user.display_name
                flag = True
                for i in range(len(user_info[line_number])):
                    if user_info[line_number][i][0] == username:
                        line_person[line_number] -= 1
                        original_message = await interaction.channel.fetch_message(user_info[line_number][i][1])
                        await original_message.delete()
                        del user_info[line_number][i]
                        flag = False

                for i in range(len(user_info)):
                    if i == line_number:
                        continue
                    for j in range(len(user_info[i])):
                        if user_info[i][j][0] == username:
                            flag = False

                if flag:
                    line_person[line_number] += 1
                    if line_person[line_number] >= 4:
                        await ctx.send(f'{username} 님이 {line_name}으로 대기합니다. (대기는 아직 개발 중입니다...) ')
                    else:
                        message = await ctx.send(f'{username} 님이 {line_name}으로 참여합니다!')
                        user_info[line_number].append((username, message.id))

                button.label = f"{line_name} : {line_person[line_number]}"
                if (line_person[line_number] >= 4):
                    button.style = discord.ButtonStyle.red
                else:
                    button.style = discord.ButtonStyle.gray

                await interaction.response.edit_message(view=self)

            return callback
        def mid_callback(self, button):
            line_number = 2
            line_name = line[line_number]

            async def callback(interaction: discord.Interaction):
                username = interaction.user.display_name
                flag = True
                for i in range(len(user_info[line_number])):
                    if user_info[line_number][i][0] == username:
                        line_person[line_number] -= 1
                        original_message = await interaction.channel.fetch_message(user_info[line_number][i][1])
                        await original_message.delete()
                        del user_info[line_number][i]
                        flag = False

                for i in range(len(user_info)):
                    if i == line_number:
                        continue
                    for j in range(len(user_info[i])):
                        if user_info[i][j][0] == username:
                            flag = False

                if flag:
                    line_person[line_number] += 1
                    if line_person[line_number] >= 4:
                        await ctx.send(f'{username} 님이 {line_name}으로 대기합니다. (대기는 아직 개발 중입니다...) ')
                    else:
                        message = await ctx.send(f'{username} 님이 {line_name}으로 참여합니다!')
                        user_info[line_number].append((username, message.id))

                button.label = f"{line_name} : {line_person[line_number]}"
                if (line_person[line_number] >= 4):
                    button.style = discord.ButtonStyle.red
                else:
                    button.style = discord.ButtonStyle.gray

                await interaction.response.edit_message(view=self)

            return callback
        def ad_callback(self, button):
            line_number = 3
            line_name = line[line_number]

            async def callback(interaction: discord.Interaction):
                username = interaction.user.display_name
                flag = True
                for i in range(len(user_info[line_number])):
                    if user_info[line_number][i][0] == username:
                        line_person[line_number] -= 1
                        original_message = await interaction.channel.fetch_message(user_info[line_number][i][1])
                        await original_message.delete()
                        del user_info[line_number][i]
                        flag = False

                for i in range(len(user_info)):
                    if i == line_number:
                        continue
                    for j in range(len(user_info[i])):
                        if user_info[i][j][0] == username:
                            flag = False

                if flag:
                    line_person[line_number] += 1
                    if line_person[line_number] >= 4:
                        await ctx.send(f'{username} 님이 {line_name}으로 대기합니다. (대기는 아직 개발 중입니다...) ')
                    else:
                        message = await ctx.send(f'{username} 님이 {line_name}으로 참여합니다!')
                        user_info[line_number].append((username, message.id))

                button.label = f"{line_name} : {line_person[line_number]}"
                if (line_person[line_number] >= 4):
                    button.style = discord.ButtonStyle.red
                else:
                    button.style = discord.ButtonStyle.gray

                await interaction.response.edit_message(view=self)

            return callback
        def sup_callback(self, button):
            line_number = 4
            line_name = line[line_number]

            async def callback(interaction: discord.Interaction):
                username = interaction.user.display_name
                flag = True
                for i in range(len(user_info[line_number])):
                    if user_info[line_number][i][0] == username:
                        line_person[line_number] -= 1
                        original_message = await interaction.channel.fetch_message(user_info[line_number][i][1])
                        await original_message.delete()
                        del user_info[line_number][i]
                        flag = False

                for i in range(len(user_info)):
                    if i == line_number:
                        continue
                    for j in range(len(user_info[i])):
                        if user_info[i][j][0] == username:
                            flag = False

                if flag:
                    line_person[line_number] += 1
                    if line_person[line_number] >= 4:
                        await ctx.send(f'{username} 님이 {line_name}으로 대기합니다. (대기는 아직 개발 중입니다...) ')
                    else:
                        message = await ctx.send(f'{username} 님이 {line_name}으로 참여합니다!')
                        user_info[line_number].append((username, message.id))

                button.label = f"{line_name} : {line_person[line_number]}"
                if (line_person[line_number] >= 4):
                    button.style = discord.ButtonStyle.red
                else:
                    button.style = discord.ButtonStyle.gray

                await interaction.response.edit_message(view=self)

            return callback

    current_view = MyView()

    view_message = await ctx.send(embed = discord.Embed(title='20인 내전'),view=current_view)
    await ctx.send(f'@everyone 20인 내전 {message}')

@bot.command(name='20인내전마감')
async def twenty_end_game(ctx):
    global user_info, line_person, current_view, view_message

    if current_view:
        current_view.clear_items()
        await view_message.edit(view=current_view)

    people = line_person[0] + line_person[1] + line_person[2] + line_person[3] + line_person[4]

    team_head_line_number = get_team_head_number()

    await ctx.send(get_team_head_lineup(team_head_line_number))
    await ctx.send(get_twenty_user_lineup(team_head_line_number))

    await ctx.send(f'감사합니다 여러분. 총 참여 인원은 {people}명 입니다.')
    current_view = None
    view_message = None
    user_info = [[], [], [], [], []]
    line_person = [0,0,0,0,0]


@bot.command(name='마감')
async def end_game(ctx):
    global recording, message_log, recording_channel
    if recording == True:
        if recording_channel == ctx.channel:
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
            await ctx.send('다른 채널에서 내전이 진행 중입니다.')
    else:
        await ctx.send('아직 내전이 실행되지 않았습니다. !내전으로 내전을 열어주세요.')

@bot.command(name='쫑')
async def jjong_game(ctx):
    global recording, message_log, recording_channel
    if recording == True and recording_channel == ctx.channel:
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
async def jeolgu(ctx):
    await ctx.send(f'절구통')

@bot.command(name='배리나')
async def baerina(ctx):
    await ctx.send(f'150KG')

@bot.command(name='제우스')
async def zeus(ctx):
    await ctx.send(f'점수먹는 하마')

@bot.command(name='뭘봐')
async def meolbwa(ctx):
    await ctx.send(f'마술사의 샌드백')

@bot.command(name='제드에코')
async def zeddekko(ctx):
    await ctx.send(f'에메딱')

@bot.command(name='준혁')
async def yayo(ctx):
    await ctx.send(f'탑징징')

@bot.command(name='규진')
async def yayo(ctx):
    await ctx.send(f'0.1 정해인')

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
