from discord.ui import Button, View
from SortFunctions import sort_twenty_members
from TierScore import get_user_tier_score
import random
import discord

# 각 라인별 인원 담는 배열
user_info = None
# 투표 받을 View
naejeon_view = None
# 내전 생성자
naejeon_creator = None
# 투표를 보낸 메세지를 저장할 변수
view_message = None
# 라인 이름
line = ['탑','정글','미드','원딜','서폿']


async def make_twenty_naejeon(ctx, message = '모이면 바로 시작'):
    global user_info, naejeon_view, naejeon_creator, line, view_message

    class MyView(View):
        def __init__(self):
            super().__init__(timeout=10800)

            top_button = Button(label=f'탑 : 0', style=discord.ButtonStyle.gray)
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
                        original_message = await interaction.channel.fetch_message(
                            user_info[line_number][i][1])
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

    user_info = [[], [], [], [], []]
    naejeon_view = MyView()
    naejeon_creator = ctx.author.display_name
    view_message = await ctx.send(embed=discord.Embed(title=f'20인 내전 {message}'), view=naejeon_view)
    await ctx.send(f'@everyone 20인 내전 {message}')

    return True

async def magam_twenty_naejeon(ctx):
    global user_info, naejeon_view, naejeon_creator, line, view_message

    if naejeon_creator != ctx.author.display_name:
        return True


    team_head_line_number = get_team_head_number(user_info)
    waiting_people_list = get_twenty_waiting_list(user_info)

    await ctx.send(get_team_head_lineup(team_head_line_number, user_info))
    await ctx.send(get_twenty_user_lineup(team_head_line_number, user_info))
    await ctx.send(get_twenty_naejeon_warning())

    if waiting_people_list != '':
        await ctx.send(waiting_people_list)

    await ctx.send(f'@everyone 20인 내전 모집이 완료되었습니다. 결과를 확인해주세요')

    # 초기화
    await view_message.delete()
    naejeon_creator = None
    naejeon_view = None
    view_message = None
    user_info = None

    return False

async def jjong_twenty_naejeon(ctx):
    global user_info, naejeon_view, view_message, naejeon_creator

    if naejeon_creator != ctx.author.display_name:
        return None

    await ctx.send(f'@everyone 20인 내전 쫑')

    # 초기화
    await view_message.delete()
    naejeon_creator = None
    naejeon_view = None
    view_message = None
    user_info = None
    

def get_team_head_number(user_info: list):

    min_diff = 9999999
    line_number = 0


    for i in range(len(user_info)):
        max_score = 0
        min_score = 9999999
        for index in range(min(4,len(user_info[i]))):
            users = user_info[i]

            user = users[index][0]
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


def get_team_head_lineup(line_number: int, user_info: list):

    result = ''
    result += f'팀장\n'
    result += f'=========================================\n\n'

    user_for_sort = []

    for i in range(min(4,len(user_info[line_number]))):
        user_for_sort.append(user_info[line_number][i])

    users = sort_twenty_members(user_for_sort)

    for i in range(min(4,len(users))):
        result += f'{i+1}팀\n'
        user_score = get_user_tier_score(users[i])
        result += f'{users[i]} : {user_score}\n\n'

    result += f'========================================='

    return result

def get_twenty_user_lineup(head_line_number: int, user_info: list):

    line = ['탑','정글','미드','원딜','서폿']

    index = 1

    result = ''
    result += f'팀원\n'
    result += f'=========================================\n\n'

    for line_number in range(len(user_info)):
        if line_number == head_line_number:
            continue

        user_for_sort = user_info[line_number][0:4]

        users = sort_twenty_members(user_for_sort)

        result += f'{line[line_number]}\n'

        for i in range(len(users)):
            result += f'{index}. {users[i]}\n'
            index += 1

        result += f' \n'

    result += f'========================================='

    return result

def get_twenty_waiting_list(user_info: list):

    line = ['탑', '정글', '미드', '원딜', '서폿']


    waiting_list = ''

    for line_number in range(len(user_info)):
        for i in range(len(user_info[line_number])):
            if i == 4:
                waiting_list += f'{line[line_number]}\n'

            if i >= 4:
                waiting_list += f'{user_info[line_number][i][0]}\n'

    if waiting_list == '':
        return waiting_list

    result = ''
    result += f'대기 명단\n'
    result += f'=========================================\n'
    result += waiting_list
    result += f'========================================='

    return result

def get_twenty_naejeon_warning():

    warning_text = ''

    warning_text += f'경매 방식\n\n'
    warning_text += f'1. 입찰은 10 단위로 하되 갱신에는 제한이 없습니다.\n'
    warning_text += f'2. 각 라인별 남은 마지막 매물(유찰포함)은 그 라인이 없는 팀이 무료로 데려갑니다.\n'
    warning_text += f'   ex) 서폿에 제트님만 남을시 서폿없는팀이 제트님을 무료로 데려갑니다.\n'
    warning_text += f'3. 입찰에 참여를 할때 팀명과 가격을 말해주세요.\n'
    warning_text += f'   ex) 1팀 20 이런 방식으로 해주세요.\n'
    warning_text += f'4. 경매가 끝나고 돈이 제일 많이 남은 팀은 상대팀 지목 및 진영선택권을 가져갑니다.\n\n'
    warning_text += f'경매 유의사항\n\n'
    warning_text += f'1. 처음부터 올인을 하거나 반대로 너무 아낄시에는 대참사가 일어날 수 있습니다. 현명한 결정 응원합니다.\n'
    warning_text += f'2. 경매중에는 팀장 외 마이크는 다 꺼주시기 바랍니다.\n'
    warning_text += f'3. 경매가 익숙하지 않을 수 있습니다.\n'
    warning_text += f'   그러나 경매결과가 맘에 들지 않는다고 불평하는 자세는 지양해주시기 바랍니다.\n'
    warning_text += f'4. 3번 사항이 관리자 혹은 진행자에게 적발이 될 경우 경고를 부여하겠습니다.\n\n'
    warning_text += f'즐거운 20인 내전 되시길 바랍니다!!'

    return warning_text

def get_twenty_team_choose_number():

    sixteen_numbers = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16]
    result = []

    for i in range(16):
        number = random.choice(sixteen_numbers)
        sixteen_numbers.remove(number)
        result.append(number)

    return result