import itertools
import random

import discord

from SortFunctions import sort_naejeon_members, get_result_sorted_by_tier, get_tier_score

naejeon_creator = None


async def make_normal_naejeon(ctx, message='3판 2선 모이면 바로 시작'):
    # 일반 내전 모집
    global naejeon_creator

    naejeon_creator = ctx.author.display_name
    await ctx.send(f'@everyone 내전 {message}')
    return True


async def magam_normal_naejeon(ctx, participants):
    # 일반 내전 마감

    class NaejeonMember:
        def __init__(self, index):
            self.index = index + 1
            self.name = participants[index]

    class NaejeonView(discord.ui.View):
        def __init__(self):
            super().__init__(timeout=3600)
            self.members = [NaejeonMember(i) for i in range(0, 10)]
            for member in self.members:
                self.add_item(EditButton(member))
            self.add_item(NaejeonStartButton())

        async def update_message(self, interaction: discord.Interaction):
            naejeon_members_result = "\n".join([f"### {member.index}: {member.name}" for member in self.members])
            await interaction.response.edit_message(content=naejeon_members_result, view=self)

    class EditButton(discord.ui.Button):
        def __init__(self, member):
            super().__init__(label=f"{member.index}번 닉네임 수정")
            self.member = member

        async def callback(self, interaction: discord.Interaction):
            await interaction.response.send_modal(EditModal(member=self.member))

    class EditModal(discord.ui.Modal):
        def __init__(self, member):
            super().__init__(title=f"{member.index}번 닉네임 수정")
            self.member = member

            self.text_input = discord.ui.TextInput(
                label=f"서버 닉네임을 전부 넣어주세요.",
                default=self.member.name
            )
            self.add_item(self.text_input)

        async def on_submit(self, interaction: discord.Interaction):
            self.member.name = self.text_input.value
            await view.update_message(interaction)

    class NaejeonStartButton(discord.ui.Button):
        def __init__(self):
            super().__init__(label=f"명단 확정", style=discord.ButtonStyle.success)

        async def callback(self, interaction: discord.Interaction):
            username = interaction.user.display_name
            await ctx.send(f'{username}님이 명단을 확정지었습니다.')
            await interaction.message.delete()
            final_participants = []
            for member in view.members:
                final_participants.append(member.name)

            participants_result = sort_naejeon_members(final_participants)
            sorted_participants_message = get_result_sorted_by_tier(participants_result)

            await ctx.send(sorted_participants_message)
            await handle_naejeon_team(ctx, participants_result)

    view = NaejeonView()
    naejeon_members_result = "\n".join([f"### {member.index}: {member.name}" for member in view.members])
    await ctx.send(content=f'@everyone 내전 모집이 완료되었습니다. 참여 명단을 확인하세요.\n\n{naejeon_members_result}', view=view)


async def jjong_normal_naejeon(ctx):
    # 일반 내전 쫑
    global naejeon_creator

    if naejeon_creator != ctx.author.display_name:
        return True

    await ctx.send(f'@everyone 쫑')

    # 초기화
    naejeon_creator = None

    return False


async def handle_naejeon_team(ctx, participants):

    team_head_list = []

    class NaejeonMember:
        def __init__(self, index):
            self.index = index + 1
            self.name = participants[index]

    class HandleTeamView(discord.ui.View):
        def __init__(self):
            super().__init__(timeout=3600)
            self.members = [NaejeonMember(i) for i in range(0, 10)]
            for member in self.members:
                self.add_item(TeamHeadButton(member))
            self.add_item(StopButton())
            self.add_item(AutoPlayButton())

    class TeamHeadButton(discord.ui.Button):
        def __init__(self, member):
            super().__init__(label=f"{member.index}.{member.name}")
            self.member = member

        async def callback(self, interaction: discord.Interaction):
            username = interaction.user.display_name
            team_head_list.append(self.member.name)
            await ctx.send(f'{username}님이 버튼을 눌렀습니다. {self.member.name}님이 팀장입니다.')
            self.view.remove_item(self)
            self.view.members.remove(self.member)
            if len(team_head_list) == 2:
                await interaction.message.delete()
                await choose_blue_red_naejeon(ctx, team_head_list, self.view.members)
                return

            await interaction.response.edit_message(content=f'## 두번째 팀장 닉네임 버튼을 눌러주세요.', view=self.view)

    class StopButton(discord.ui.Button):
        def __init__(self):
            super().__init__(label=f"메모장으로 진행", style=discord.ButtonStyle.red)

        async def callback(self, interaction: discord.Interaction):
            username = interaction.user.display_name
            await ctx.send(f'{username}님이 메모장으로 진행을 선택하셨습니다.')
            await interaction.message.delete()

    class AutoPlayButton(discord.ui.Button):
        def __init__(self):
            super().__init__(label=f"수습 마술사에게 팀뽑 맡기기", style=discord.ButtonStyle.primary)

        async def callback(self, interaction: discord.Interaction):
            await make_auto_team(ctx, participants)
            await interaction.message.delete()

    handle_team_view = HandleTeamView()
    await ctx.send(content=f'## 팀장 두 분의 닉네임 버튼을 눌러주세요.', view=handle_team_view)

async def make_auto_team(ctx, participants):
    auto_teams = get_auto_team(participants)
    result_board = get_naejeon_board(auto_teams)

    class AutoTeamView(discord.ui.View):
        def __init__(self):
            super().__init__(timeout=3600)
            self.add_item(ResumeButton())
            self.add_item(UndoButton())

    class UndoButton(discord.ui.Button):
        def __init__(self):
            super().__init__(label=f"되돌아가기", style=discord.ButtonStyle.red)

        async def callback(self, interaction: discord.Interaction):
            await interaction.message.delete()
            await handle_naejeon_team(ctx, participants)

    class ResumeButton(discord.ui.Button):
        def __init__(self):
            super().__init__(label=f"이대로 진행", style=discord.ButtonStyle.primary)

        async def callback(self, interaction: discord.Interaction):
            await interaction.response.edit_message(content=f'{result_board}', view=None)

    auto_team_view = AutoTeamView()
    await ctx.send(content=f'{result_board}', view=auto_team_view)

def get_auto_team(participants):

    user_result = []

    for participant in participants:
        user_result.append({'tier_score':get_tier_score(participant),'username':participant})

    best_difference = float('inf')  # 차이를 저장할 변수
    best_group = None

    for group1_indices in itertools.combinations(range(len(user_result)), 5):
        group1 = [user_result[i] for i in group1_indices]
        group2 = [user_result[i] for i in range(len(user_result)) if i not in group1_indices]

        sum_group1 = sum([item['tier_score'] for item in group1])
        sum_group2 = sum([item['tier_score'] for item in group2])

        difference = abs(sum_group1 - sum_group2)

        if difference < best_difference:
            best_difference = difference
            best_group = [[item['username'] for item in group1],
                          [item['username'] for item in group2]]

    if random.choice([True, False]):
        best_group[0], best_group[1] = best_group[1], best_group[0]

    return best_group

async def choose_blue_red_naejeon(ctx, team_head_list, members):

    await ctx.send(f'=========================================')
    # 블루팀 레드팀 고르기
    blue_team = []
    red_team = []

    selected = random.choice(team_head_list)
    team_head_list.remove(selected)
    not_selected = team_head_list[0]

    first_random_number = random.randint(2, 1000)
    second_random_number = random.randint(1, first_random_number - 1)

    await ctx.send(f'{selected}님이 {not_selected}님을 {first_random_number} : {second_random_number}으로 이겼습니다.')


    class BlueRedView(discord.ui.View):
        def __init__(self):
            super().__init__(timeout=3600)
            self.add_item(BlueButton())
            self.add_item(RedButton())

    class BlueButton(discord.ui.Button):
        def __init__(self):
            super().__init__(label=f"블루팀", style=discord.ButtonStyle.primary)

        async def callback(self, interaction: discord.Interaction):
            username = interaction.user.display_name
            if username != selected:
                await interaction.response.edit_message(content=f'## {selected}님이 누른 것만 인식합니다. {username}님 누르지 말아주세요.',view=blue_red_view)
                return
            blue_team.append(selected)
            red_team.append(team_head_list[0])
            await ctx.send(f'{selected}님이 블루팀을 선택하셨습니다.')
            await interaction.message.delete()
            await choose_order_naejeon(ctx, blue_team, red_team, members)

    class RedButton(discord.ui.Button):
        def __init__(self):
            super().__init__(label=f"레드팀", style=discord.ButtonStyle.red)

        async def callback(self, interaction: discord.Interaction):
            username = interaction.user.display_name
            if username != selected:
                await interaction.response.edit_message(content=f'## {selected}님이 누른 것만 인식합니다. {username}님 누르지 말아주세요.',view=blue_red_view)
                return
            red_team.append(selected)
            blue_team.append(team_head_list[0])
            await ctx.send(f'{selected}님이 레드팀을 선택하셨습니다.')
            await interaction.message.delete()
            await choose_order_naejeon(ctx, blue_team, red_team, members)

    blue_red_view = BlueRedView()
    await ctx.send(content=f'## {selected}님, 진영을 선택해주세요.', view=blue_red_view)


async def choose_order_naejeon(ctx, blue_team, red_team, members):

    await ctx.send(f'=========================================')
    # 선뽑 후뽑 고르기
    teams = [blue_team, red_team]
    order_flag = True

    selected_team = random.choice(teams)
    selected = selected_team[0]
    if selected == blue_team[0]:
        order_flag = True
        not_selected = red_team[0]
    else:
        order_flag = False
        not_selected = blue_team[0]

    first_random_number = random.randint(2, 1000)
    second_random_number = random.randint(1, first_random_number - 1)

    await ctx.send(f'{selected}님이 {not_selected}님을 {first_random_number} : {second_random_number}으로 이겼습니다.')

    class OrderView(discord.ui.View):
        def __init__(self):
            super().__init__(timeout=3600)
            self.add_item(FirstPickButton())
            self.add_item(SecondPickButton())

    class FirstPickButton(discord.ui.Button):
        def __init__(self):
            super().__init__(label=f"선뽑(먼저 한명 뽑기)", style=discord.ButtonStyle.primary)

        async def callback(self, interaction: discord.Interaction):
            username = interaction.user.display_name
            if username != selected:
                await interaction.response.edit_message(content=f'## {selected}님이 누른 것만 인식합니다. {username}님 누르지 말아주세요.',view=order_view)
                return
            await ctx.send(f'{selected}님이 선뽑입니다.')
            await interaction.message.delete()
            await choose_naejeon_team(ctx, teams, order_flag, members)
            return

    class SecondPickButton(discord.ui.Button):
        def __init__(self):
            super().__init__(label=f"후뽑(나중에 두명 뽑기)", style=discord.ButtonStyle.red)

        async def callback(self, interaction: discord.Interaction):
            username = interaction.user.display_name
            if username != selected:
                await interaction.response.edit_message(content=f'## {selected}님이 누른 것만 인식합니다. {username}님 누르지 말아주세요.',view=order_view)
                return
            await ctx.send(f'{selected}님이 후뽑입니다.')
            await interaction.message.delete()
            await choose_naejeon_team(ctx, teams, not order_flag, members)
            return

    order_view = OrderView()
    await ctx.send(content=f'## {selected}님, 뽑는 순서를 정해주세요.', view=order_view)

async def choose_naejeon_team(ctx, teams, flag, members):
    await ctx.send(f'=========================================')

    pick_order = [flag, not flag, not flag, flag, flag, not flag, not flag, flag]

    def get_team_head(pick_order, teams):
        return teams[0][0] if pick_order[0] else teams[1][0]

    def add_member_to_team(pick_order, teams, member_name):
        if pick_order[0]:
            teams[0].append(member_name)
        else:
            teams[1].append(member_name)

    class RemainMember:
        def __init__(self, index):
            self.name = members[index].name

    class ChooseNaejeonView(discord.ui.View):
        def __init__(self):
            super().__init__()
            self.members = [RemainMember(i) for i in range(0, 8)]
            for member in self.members:
                self.add_item(MemberButton(member))

    class MemberButton(discord.ui.Button):
        def __init__(self, member):
            super().__init__(label=f"{member.name}")
            self.member = member

        async def callback(self, interaction: discord.Interaction):
            username = interaction.user.display_name
            team_head = get_team_head(pick_order, teams)

            if username != team_head:
                await interaction.response.edit_message(content=f'{get_naejeon_board(teams)}\n## {team_head}님이 누른 것만 인식합니다. {username}님 누르지 말아주세요.', view=self.view)
                return

            self.view.remove_item(self)
            self.view.members.remove(self.member)
            add_member_to_team(pick_order, teams, self.member.name)
            pick_order.pop(0)

            await ctx.send(f'{username}님이 {self.member.name}님을 뽑았습니다.')

            if len(pick_order) == 1:
                add_member_to_team(pick_order, teams, self.view.members[0].name)
                await interaction.message.delete()
                await ctx.send(get_naejeon_board(teams))
                await ctx.send(f'밴픽은 아래 사이트에서 진행해주시면 됩니다.')
                await ctx.send(f'https://banpick.kr/')
                await ctx.send(f'사용자설정 방 제목 : 룬테라 / 비밀번호 : 1234')
                return

            team_head = get_team_head(pick_order, teams)
            await interaction.response.edit_message(content=f'{get_naejeon_board(teams)}\n## {team_head}님, 팀원을 뽑아주세요.', view=self.view)

    choose_naejeon_view = ChooseNaejeonView()
    await ctx.send(content=f'{get_naejeon_board(teams)}\n## {get_team_head(pick_order, teams)}님, 팀원을 뽑아주세요.', view=choose_naejeon_view)

    # await ctx.send(get_naejeon_board(teams))


def get_naejeon_board(teams):
    board = f'```\n'
    board += f'🟦  블루진영\n\n'
    for blue_member in teams[0]:
        board += f'{blue_member}\n'
    board += f'\n🟥  레드진영\n\n'
    for red_member in teams[1]:
        board += f'{red_member}\n'
    board += f'```'
    return board