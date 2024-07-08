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
from TwentyNaejeon import get_twenty_user_lineup, get_team_head_lineup, get_team_head_number, get_twenty_waiting_list

load_dotenv()
TOKEN: Final[str] = os.getenv('DISCORD_TOKEN')

intents: Intents = Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

recording = False
recording_channel = None
message_log = []

user_info = [[], [], [], [], []]
current_view = None
view_message = None
naejeon_creator = None
twenty_naejeon_creator = None
twenty_naejeon_channel = None


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

@bot.command(name='20인내전모집')
async def start_twenty_game(ctx, *, message='모바시'):
    global user_info, current_view, view_message, twenty_naejeon_creator, twenty_naejeon_channel
    line = ['탑','정글','미드','원딜','서폿']

    class MyView(View):
        def __init__(self):
            super().__init__()

            top_button = Button(label=f'탑 : 0', style = discord.ButtonStyle.gray)
            top_button.callback = self.top_callback(top_button)

            jg_button = Button(label=f'정글 : 0', style=discord.ButtonStyle.gray)
            jg_button.callback = self.jg_callback(jg_button)

            mid_button = Button(label=f'미드 : 0', style=discord.ButtonStyle.gray)
            mid_button.callback = self.mid_callback(mid_button)

            ad_button = Button(label=f'원딜 : 0', style=discord.ButtonStyle.gray)
            ad_button.callback = self.ad_callback(ad_button)

            sup_button = Button(label=f'서폿 : 0', style=discord.ButtonStyle.gray)
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
                    message = await ctx.send(f'{username} 님이 {line_name}으로 참여합니다!')
                    user_info[line_number].append((username, message.id))


                button.label = f"{line_name} : {len(user_info[line_number])}"
                if(len(user_info[line_number]) >= 4):
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
                    message = await ctx.send(f'{username} 님이 {line_name}로 참여합니다!')
                    user_info[line_number].append((username, message.id))


                button.label = f"{line_name} : {len(user_info[line_number])}"
                if (len(user_info[line_number]) >= 4):
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
                    message = await ctx.send(f'{username} 님이 {line_name}로 참여합니다!')
                    user_info[line_number].append((username, message.id))


                button.label = f"{line_name} : {len(user_info[line_number])}"
                if (len(user_info[line_number]) >= 4):
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
                    message = await ctx.send(f'{username} 님이 {line_name}로 참여합니다!')
                    user_info[line_number].append((username, message.id))


                button.label = f"{line_name} : {len(user_info[line_number])}"
                if (len(user_info[line_number]) >= 4):
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
                    message = await ctx.send(f'{username} 님이 {line_name}으로 참여합니다!')
                    user_info[line_number].append((username, message.id))

                button.label = f"{line_name} : {len(user_info[line_number])}"
                if (len(user_info[line_number]) >= 4):
                    button.style = discord.ButtonStyle.red
                else:
                    button.style = discord.ButtonStyle.gray

                await interaction.response.edit_message(view=self)

            return callback

    if twenty_naejeon_creator == None:
        current_view = MyView()
        twenty_naejeon_creator = ctx.author.display_name
        twenty_naejeon_channel = ctx.channel
        view_message = await ctx.send(embed = discord.Embed(title=f'20인 내전 {message}'),view=current_view)
        await ctx.send(f'@everyone 20인 내전 {message}')

@bot.command(name='20인내전마감')
async def twenty_end_game(ctx):
    global user_info, current_view, view_message, twenty_naejeon_creator, twenty_naejeon_channel

    if twenty_naejeon_creator == ctx.author.display_name and twenty_naejeon_channel == ctx.channel:

        if current_view:
            current_view.clear_items()
            await view_message.edit(view=current_view)

        team_head_line_number = get_team_head_number(user_info)
        waiting_people_list = get_twenty_waiting_list(user_info)

        await ctx.send(get_team_head_lineup(team_head_line_number,user_info))
        await ctx.send(get_twenty_user_lineup(team_head_line_number,user_info))

        if waiting_people_list != '':
            await ctx.send(waiting_people_list)

        await ctx.send(f'@everyone 20인 내전 모집이 완료되었습니다. 결과를 확인해주세요')

        twenty_naejeon_creator = None
        current_view = None
        view_message = None
        user_info = [[], [], [], [], []]

@bot.command(name='20인내전쫑')
async def twenty_jjong_game(ctx):
    global user_info, current_view, view_message, twenty_naejeon_creator

    if twenty_naejeon_creator == ctx.author.display_name and twenty_naejeon_channel == ctx.channel:

        if current_view:
            current_view.clear_items()
            await view_message.edit(view=current_view)

        twenty_naejeon_creator = None
        current_view = None
        view_message = None
        user_info = [[], [], [], [], []]

        await ctx.send(f'@everyone 20인 내전 쫑')

@bot.command(name='내전모집')
async def start_game(ctx, *, message='모바시'):
    global recording, message_log, recording_channel, naejeon_creator
    if recording == False:
        recording = True
        recording_channel = ctx.channel
        message_log = []
        naejeon_creator = ctx.author.display_name
        await ctx.send(f'@everyone 내전 {message}')
    else:
        await ctx.send('이미 내전이 열려 있습니다. 기존의 내전을 마감하고 진행해주세요.')


@bot.command(name='내전마감')
async def end_game(ctx):
    global recording, message_log, recording_channel, naejeon_creator
    if recording == True:
        if recording_channel == ctx.channel and naejeon_creator == ctx.author.display_name:
            recording = False
            participants = set()
            naejeon_creator = None

            for log in message_log:
                participants.add(log['author'])

            if participants:
                participants_result = sort_participants(participants)

                await ctx.send(f'@everyone 내전 모집이 마감되었습니다. 모두 모여주세요.')
                await ctx.send(participants_result)
            else:
                await ctx.send('의도치 않은 오류가 발생했습니다.')
        elif recording_channel == ctx.channel:
            await ctx.send('내전 마감은 내전 모집을 시작한 분이 직접 입력해주세요.')
        else:
            await ctx.send('다른 채널에서 내전이 진행 중입니다.')
    else:
        await ctx.send('아직 내전이 실행되지 않았습니다. !내전으로 내전을 열어주세요.')

@bot.command(name='내전쫑')
async def jjong_game(ctx):
    global recording, message_log, recording_channel, naejeon_creator
    if recording == True and recording_channel == ctx.channel and naejeon_creator == ctx.author.display_name:
        recording = False
        message_log = []
        recording_channel = None
        naejeon_creator = None
        await ctx.send(f'@everyone 쫑')
    elif recording == True and recording_channel == ctx.channel:
        await ctx.send('내전 쫑은 내전 모집을 시작한 분이 직접 입력해주세요.')


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

    if message.content == '!권기현':
        await message.channel.send(f'날쌔지 않음')

    if message.content == '!절구':
        await message.channel.send(f'절구통')

    if message.content == '!배리나':
        await message.channel.send(f'180KG')

    if message.content == '!제우스':
        await message.channel.send(f'점수먹는 하마')

    if message.content == '!제드에코' or message.content == '!재진':
        await message.channel.send(f'에메딱')

    if message.content == '!뭘봐':
        await message.channel.send(f'마술사의 샌드백')

    if message.content == '!규진' or message.content == '!이규진':
        await message.channel.send(f'룬테라 정해인')

    if message.content == '!준혁' or message.content == '!야요':
        await message.channel.send(f'탑징징')

    await bot.process_commands(message)

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
