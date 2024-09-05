from datetime import datetime
import random

import discord
from discord.ui import Button, View, Modal

from TwentyNaejeon import get_team_head_number, get_team_head_lineup, get_user_lineup

user_list = None


async def add_user_info(user_info):
    global user_list

    user_list = user_info


async def confirm_twenty_recruit(ctx):
    global user_list

    line_names = ['탑', '정글', '미드', '원딜', '서폿']

    class TwentyMember:
        def __init__(self, index):
            self.line = line_names[index]
            self.members = user_list[index]

    class AuctionView(discord.ui.View):
        def __init__(self):
            super().__init__(timeout=3600)
            self.members = [TwentyMember(i) for i in range(0, 5)]
            for members in self.members:
                self.add_item(EditButton(members))
            self.add_item(ConfirmButton())

        async def update_message(self, interaction: discord.Interaction):
            members_text = f'참여 명단\n=========================================\n'
            for i in range(0, 5):
                members_text += get_members_text(user_list[i], line_names[i])
            await interaction.response.edit_message(content=members_text, view=self)

    class ConfirmButton(discord.ui.Button):
        def __init__(self):
            super().__init__(label=f"명단 확정",style=discord.ButtonStyle.success)

        async def callback(self, interaction: discord.Interaction):
            username = interaction.user.display_name
            await ctx.send(f'{username}님이 명단을 확정지었습니다.')
            await interaction.message.delete()
            await run_twenty_auction(ctx)

    class EditButton(discord.ui.Button):
        def __init__(self, members):
            super().__init__(label=f"{members.line} 명단 수정")
            self.members = members

        async def callback(self, interaction: discord.Interaction):
            await interaction.response.send_modal(EditModal(members=self.members))

    class EditModal(discord.ui.Modal):
        def __init__(self, members):
            super().__init__(title=f"{members.line} 명단 수정")
            self.members = members

            default_text = get_members_text(self.members.members, self.members.line)

            self.text_input = discord.ui.TextInput(
                label=f"제공된 양식에서 벗어나지 않게 주의해주세요.",
                style=discord.TextStyle.paragraph,
                default=default_text
            )
            self.add_item(self.text_input)

        async def on_submit(self, interaction: discord.Interaction):
            await edit_user_list(self.text_input.value)
            await view.update_message(interaction)

    view = AuctionView()
    members_text = f'참여 명단\n=========================================\n'
    for i in range(0, 5):
        members_text += get_members_text(user_list[i], line_names[i])
    await ctx.send(content=members_text, view=view)


def get_members_text(member_list, line):
    members = member_list

    members_text = f'{line}\n'

    for member in members:
        members_text += f'{member}\n'

    members_text += f'=========================================\n'

    return members_text


async def edit_user_list(input_text):
    global user_list

    line_names = ['탑', '정글', '미드', '원딜', '서폿']

    splitted_input = input_text.split('\n')
    line_name = splitted_input[0]
    line_index = 0
    for i, name in enumerate(line_names):
        if name == line_name:
            line_index = i
    for index in range(1, 5):
        user_list[line_index][index - 1] = splitted_input[index]

    return None


async def run_twenty_auction(ctx):
    global user_list

    # user_list는 20인 내전으로부터 받아와야 함. 일단 지금은 생략
    # user_list = read_file_and_split_to_arrays('twentyex.txt')

    if user_list is None:
        await ctx.send(f'문제가 발생했습니다. 수동으로 경매를 진행해주세요.')
        return None

    naejeon_members = 20

    # 팀장 라인 번호 찾기
    team_head_line_number = get_team_head_number(user_list, naejeon_members)
    # 팀장 텍스트
    team_head_lineup = get_team_head_lineup(team_head_line_number, user_list, naejeon_members)
    # 팀원 텍스트
    team_user_lineup = get_user_lineup(team_head_line_number, user_list, naejeon_members)

    today_title = datetime.now().strftime("%m월 %d일 20인 내전")
    auction_warning = get_auction_warning()
    warning_message = None

    class NoteView(View):
        def __init__(self, title=f'{today_title}', initial_content=team_head_lineup + team_user_lineup):
            super().__init__(timeout=21600)
            self.title = title
            self.content = initial_content

        @discord.ui.button(label="경매 시작", style=discord.ButtonStyle.green)
        async def auction_start_button(self, interaction: discord.Interaction, button: Button):
            host = interaction.user.display_name
            auction_text = self.content
            auction_list = []
            add_auction_team_head(auction_list, auction_text)
            team_user_list = get_auction_team_user(auction_text)
            await interaction.message.delete()
            if warning_message is not None:
                await warning_message.delete()
            await twenty_auction(host, auction_list, team_user_list, ctx)

        @discord.ui.button(label="명단 수정", style=discord.ButtonStyle.primary)
        async def edit_note_button(self, interaction: discord.Interaction, button: Button):
            await interaction.message.delete()
            if warning_message is not None:
                await warning_message.delete()
            await confirm_twenty_recruit(ctx)

    class TwentyAuctionModal(Modal):
        def __init__(self, view: NoteView):
            super().__init__(title=f'{today_title}', timeout=21600)
            self.view = view
            self.note_input = discord.ui.TextInput(
                label='프로필만 변경해주세요. 포맷이 변경되면 오류가 발생합니다.',
                style=discord.TextStyle.paragraph,
                default=self.view.content
            )
            self.add_item(self.note_input)

        async def on_submit(self, interaction: discord.Interaction):
            self.view.content = self.note_input.value
            embed = discord.Embed(title=f'{today_title}', description=self.view.content)
            await interaction.response.edit_message(embed=embed, view=self.view)

    view = NoteView()
    embed = discord.Embed(title=view.title, description=view.content)
    await ctx.send(embed=embed, view=view)
    warning_message = await ctx.send(auction_warning)


async def twenty_auction(host: str, auction_list, team_user_list, ctx):
    global user_list

    await ctx.send(f'경매를 시작합니다. 경매 진행자는 {host}입니다.')

    team_users = []
    yoochal_users = []
    user_lines = []
    add_user_lines(user_lines, team_user_list)
    user_lines_count = [0, 0, 0, 0]
    team_scores = []
    for lines in auction_list:
        team_scores.append(lines[0])

    for lines in team_user_list:
        if not lines:
            continue
        for user in lines:
            team_users.append(user)

    random.shuffle(team_users)

    end_flag = False

    # 경매 로테이션.
    while team_users:
        auction_result_message = await ctx.send(get_auction_result(team_scores, auction_list))
        auction_remain_message = await ctx.send(get_auction_remain_user(team_user_list))
        now_user = team_users.pop(0)
        user_number = now_user[0]
        user_line = (user_number - 1) // 4
        user_line_number = get_line_index(user_lines[user_line])

        await ctx.send(f'### 현재 경매 대상 : [{user_lines[user_line]}] {user_number}. {now_user[1]}')

        def check(message):
            if message.author.display_name != host or message.channel.id != ctx.channel.id:
                return False
            msg_content = message.content
            if msg_content == '유찰':
                return True
            if msg_content == '종료':
                return True
            msg_info = msg_content.split(' ')
            if len(msg_info) != 2:
                return False
            team_number = msg_info[0][0]
            score = msg_info[1]
            if team_number not in {'1', '2', '3', '4'}:
                return False
            if score.isdigit():
                return True
            return False

        user_message = await ctx.bot.wait_for('message', check=check)

        if user_message.content == '유찰':
            yoochal_users.append(now_user)
        elif user_message.content == '종료':
            await auction_result_message.delete()
            await auction_remain_message.delete()
            end_flag = True
            break
        else:
            message_info = user_message.content.split(' ')
            team_number = int(message_info[0][0])
            auction_score = int(message_info[1])

            team_user_list = [
                [user for user in lines if user[0] != user_number]
                for lines in team_user_list
            ]

            auction_list[team_number - 1][1][user_line_number] = f'{now_user[1]} > {auction_score}'
            team_scores[team_number - 1] -= auction_score
            user_lines_count[user_line] += 1

            def process_users(user_list, user_line, auction_list, remain_user_list, user_lines):
                for user in user_list[:]:
                    user_number, user_name = user
                    user_line_index = (user_number - 1) // 4

                    if user_line_index == user_line:
                        user_line_number = get_line_index(user_lines[user_line_index])
                        for team in auction_list:
                            if not team[1][user_line_number]:
                                team[1][user_line_number] = f'{user_name} > FREE'
                        user_list.remove(user)
                        continue

                for user in user_list:
                    remain_user_list.append(user)

            if user_lines_count[user_line] == 3:
                remain_user_list = []
                process_users(team_users, user_line, auction_list, remain_user_list, user_lines)
                process_users(yoochal_users, user_line, auction_list, remain_user_list, user_lines)
                team_user_list[:] = [
                    [u for u in lines if u[0] in [user[0] for user in remain_user_list]]
                    for lines in team_user_list
                ]

        if not team_users:
            team_users = yoochal_users
            yoochal_users = []

        await auction_result_message.delete()
        await auction_remain_message.delete()

    if end_flag:
        await ctx.send(f'경매를 강제 종료하였습니다. !경매를 통해 재시작할 수 있습니다.')
    else:
        await ctx.send(get_auction_result(team_scores, auction_list))
        team_max_score = team_scores.index(max(team_scores)) + 1
        await ctx.send(f'경매가 완료되었습니다. {team_max_score}팀 팀장은 팀과 회의를 진행한 뒤 20인내전채팅 채널에 붙을 팀을 적어주시면 됩니다.')
        await ctx.send(f'4강전은 남은 점수가 높은 팀이 첫번째 판 진영 선택권을 가집니다. 점수가 동일한 경우 주사위를 굴려 진행해주시면 됩니다.')
        await ctx.send(f'완료된 경매에서는 되돌리기가 불가능합니다. 이 점 참고바랍니다.')
        await ctx.send(f'모두 화이팅입니다!')
        # await ctx.send(get_auction_remain_user(team_user_list))
        user_list = None


def add_auction_team_head(auction_list, auction_text):
    lines = auction_text.split('\n')

    team_head_line = get_line_index(lines[0][5:])

    team_positions = [(3, 4), (6, 7), (9, 10), (12, 13)]
    teams = ['1팀', '2팀', '3팀', '4팀']

    team_head_list = []
    for team, (pos, info_pos) in zip(teams, team_positions):
        if lines[pos] != team:
            return None
        nickname, score = map(str.strip, lines[info_pos].split(':'))
        team_nickname_list = []
        for i in range(5):
            if i == team_head_line:
                team_nickname_list.append(nickname)
            else:
                team_nickname_list.append('')
        auction_list.append((int(score), team_nickname_list))
    # 리턴값은 (팀장 이름, 팀 점수) 가 4개 들어 있는 리스트
    return team_head_list


def get_auction_team_user(auction_text):
    lines = auction_text.split('\n')
    team_user_list = [[] for _ in range(5)]
    index = 0

    for i, start in enumerate([21, 28, 35, 42]):
        line_index = get_line_index(lines[start].split(' ')[1])
        for j in range(4):
            team_user_list[line_index].append((index + j + 1, lines[start + 2 + j]))
        index += 4

    return team_user_list


def get_auction_result(team_scores, auction_list):
    auction_result = ''
    line = ['\u3000탑', '정글', '미드', '원딜', '서폿']

    def get_team_text(auction_list, index):
        team_text = ''

        score = auction_list[index][0]
        nickname_list = auction_list[index][1]

        team_text += f'\n{index + 1}팀 ( 남은 점수 : {team_scores[index]} )\n\n'
        for i in range(len(nickname_list)):
            line_name = line[i]
            nickname = nickname_list[i]
            team_text += f'{line_name} : {nickname}\n'

        return team_text

    auction_result += f'```\n'
    for index in range(len(auction_list)):
        auction_result += get_team_text(auction_list, index)
    auction_result += f'```'

    return auction_result


def get_auction_remain_user(team_user_list):
    remain_result = ''
    line = ['탑', '정글', '미드', '원딜', '서폿']

    remain_result += f'```\n'
    for i in range(len(team_user_list)):
        line_name = line[i]
        line_users = team_user_list[i]
        if not line_users:
            continue
        remain_result += f'{line_name}\n'
        for user in line_users:
            remain_result += f'{user[0]}) {user[1]}\n'
    remain_result += f'```'

    return remain_result


def add_user_lines(user_lines, team_user_list):
    line = ['탑', '정글', '미드', '원딜', '서폿']

    for i in range(len(team_user_list)):
        line_name = line[i]
        line_users = team_user_list[i]
        if not line_users:
            continue
        user_lines.append(line_name)


def get_line_index(line):
    line_text = line.strip()
    line_map = {
        '탑': 0,
        '정글': 1,
        '미드': 2,
        '원딜': 3,
        '서폿': 4
    }
    return line_map.get(line_text)


def get_auction_warning():
    warning_text = ''

    warning_text += f'## 경매 진행 참고사항\n'
    warning_text += f'명단에 변경 사항이 있는 경우 수정하기 버튼을 눌러 수정해주시길 바랍니다.\n'
    warning_text += f'한 번 경매 시작 버튼을 누르면 명단 수정이 불가능합니다.\n'
    warning_text += f'## 경매 시작을 누른 사람이 진행자가 됩니다. 진행자가 아닌 경우 장난으로 경매 시작 버튼 누르지 마시길 바랍니다.\n'
    warning_text += f'진행자 및 팀장을 제외한 모든 인원은 마이크를 꺼주시길 바랍니다.\n'
    warning_text += f'경매가 시작되면 랜덤으로 한명씩 출력되며, 그 사람에 대하여 경매를 진행해주시면 됩니다.\n'
    warning_text += f'경매 결과에 해당하는 팀 번호 버튼을 누르고, 입력창에 가격을 입력해주시면 됩니다. ex) 1팀 80\n'
    warning_text += f'유찰의 경우 자동으로 유찰 대기열에 추가되며, 경매가 종료된 이후 유찰 대기열로 경매를 추가 진행합니다.\n'
    warning_text += f'혹여 오류가 발생한 경우, 번거롭더라도 수동으로 추가 진행 부탁드립니다.\n'
    warning_text += f'경매를 방해하는 행위 및 장난으로 버튼을 누르는 행위에는 경고가 부여될 수 있습니다.'

    return warning_text


async def add_user_list_by_own(ctx):
    class SelfAuctionView(View):
        def __init__(self):
            super().__init__(timeout=21600)
            self.content = f'수 동 입 력 해 주 세 요'

        @discord.ui.button(label="명단 제출", style=discord.ButtonStyle.green)
        async def auction_start_button(self, interaction: discord.Interaction, button: Button):
            await interaction.message.delete()
            users = self.content.split('\n')
            await add_users_in_user_list(users)
            await run_twenty_auction(ctx)

        @discord.ui.button(label="수정하기", style=discord.ButtonStyle.primary)
        async def edit_note_button(self, interaction: discord.Interaction, button: Button):
            await interaction.response.send_modal(TwentyAuctionModal(self))

    class TwentyAuctionModal(Modal):
        def __init__(self, view: SelfAuctionView):
            super().__init__(title='수동경매', timeout=21600)
            self.view = view
            self.note_input = discord.ui.TextInput(
                label='탑,정글,미드,원딜,서폿 순으로 4명씩 입력해주세요.',
                style=discord.TextStyle.paragraph,
                default=self.view.content
            )
            self.add_item(self.note_input)

        async def on_submit(self, interaction: discord.Interaction):
            self.view.content = self.note_input.value
            await interaction.response.edit_message(content=self.view.content, view=self.view)

    view = SelfAuctionView()
    await ctx.send(content=view.content, view=view)


async def add_users_in_user_list(users):
    global user_list

    user_list = [[], [], [], [], []]
    for index, user in enumerate(users):
        line_number = index // 4
        user_list[line_number].append(user)
