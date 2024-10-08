import Runeterra
import itertools
import random
import discord
from discord.ui import Button
from SortFunctions import sort_game_members, get_result_sorted_by_tier, get_tier_score


async def make_normal_game(ctx, message='3판 2선 모이면 바로 시작'):
    # 일반 내전 모집

    # 내전 채팅 로그 기록 시작, 내전을 연 사람을 로그에 추가
    user = Runeterra.DiscordUser(ctx.author.id, ctx.author.display_name)
    Runeterra.normal_game_log = {user: [ctx.message.id]}
    Runeterra.normal_game_channel = str(ctx.channel.id)

    Runeterra.normal_game_creator_id = ctx.author.id
    await ctx.send(f'@everyone 내전 {message}')
    return True


async def close_normal_game(ctx, normal_game_log):
    # 일반 내전 마감
    participants = [user for user in normal_game_log.keys()]

    class GameMember:
        def __init__(self, index):
            self.index = index + 1
            self.user = participants[index]

    class GameView(discord.ui.View):
        def __init__(self):
            super().__init__(timeout=3600)
            self.members = [GameMember(i) for i in range(0, 10)]
            for member in self.members:
                self.add_item(EditButton(member))
            self.add_item(GameStartButton())

        async def update_message(self, interaction: discord.Interaction):
            updated_message = "\n".join([f"### {member.index}: <@{member.user.id}>" for member in self.members])
            await interaction.response.edit_message(content=updated_message, view=self)

    class EditButton(discord.ui.Button):
        def __init__(self, member):
            super().__init__(label=f"{member.index}번 닉네임 수정")
            self.member = member

        async def callback(self, interaction: discord.Interaction):
            await interaction.response.send_modal(EditModal(member=self.member))

    class EditModal(discord.ui.Modal):
        def __init__(self, member):
            super().__init__(timeout=3600, title=f"{member.index}번 닉네임 수정")
            self.member = member

            self.text_input = discord.ui.TextInput(
                label=f"서버 닉네임을 전부 넣어주세요.",
                default=self.member.user.nickname
            )
            self.add_item(self.text_input)

        async def on_submit(self, interaction: discord.Interaction):
            self.member.user.nickname = self.text_input.value
            await view.update_message(interaction)

    class GameStartButton(discord.ui.Button):
        def __init__(self):
            super().__init__(label=f"명단 확정", style=discord.ButtonStyle.success)

        async def callback(self, interaction: discord.Interaction):
            game_host = interaction.user.display_name
            await ctx.send(f'{Runeterra.get_nickname(game_host)}님이 명단을 확정지었습니다.')
            await interaction.message.delete()
            final_participants = []
            for member in view.members:
                final_participants.append(member.user)

            participants_result = sort_game_members(final_participants)
            sorted_participants_message = get_result_sorted_by_tier(participants_result)

            await ctx.send(sorted_participants_message)
            await handle_game_team(ctx, participants_result, game_host, normal_game_log)

    view = GameView()
    game_members_result = "\n".join([f"### {member.index}: <@{member.user.id}>" for member in view.members])
    await ctx.send(content=f'내전 모집이 완료되었습니다. 참여 명단을 확인하세요.\n\n{game_members_result}', view=view)


async def end_normal_game(ctx):
    # 일반 내전 쫑

    if Runeterra.normal_game_creator_id != ctx.author.id:
        return True

    await ctx.send(f'@everyone 쫑')

    # 초기화
    Runeterra.normal_game_creator_id = None

    return False


async def handle_game_team(ctx, participants, game_host, normal_game_log):
    team_head_list = []

    class GameMember:
        def __init__(self, index):
            self.index = index + 1
            self.name = participants[index].nickname

    class HandleTeamView(discord.ui.View):
        def __init__(self):
            super().__init__(timeout=3600)
            self.members = [GameMember(i) for i in range(0, 10)]
            for member in self.members:
                self.add_item(TeamHeadButton(member))
            self.add_item(StopButton())
            self.add_item(UndoButton())
            # 수습 마술사 팀뽑 버튼 (일시 비활성화)
            # self.add_item(AutoPlayButton())

    class TeamHeadButton(discord.ui.Button):
        def __init__(self, member):
            super().__init__(label=f"{member.index}.{member.name}")
            self.member = member

        async def callback(self, interaction: discord.Interaction):
            username = interaction.user.display_name
            if username != game_host:
                await (interaction.response.edit_message
                       (content=f'## {Runeterra.get_nickname(game_host)}님이 누른 것만 인식합니다. '
                                f'{Runeterra.get_nickname(username)}님 누르지 말아주세요.', view=self.view))
                return
            team_head_list.append(self.member.name)
            await ctx.send(f'{self.member.name}님이 팀장입니다.')
            self.view.remove_item(self)
            self.view.members.remove(self.member)
            if len(team_head_list) == 2:
                await interaction.message.delete()
                await choose_blue_red_game(ctx, team_head_list, self.view.members)
                return

            await interaction.response.edit_message(content=f'## 두번째 팀장 닉네임 버튼을 눌러주세요.', view=self.view)

    class StopButton(discord.ui.Button):
        def __init__(self):
            super().__init__(label=f"메모장으로 진행", style=discord.ButtonStyle.red)

        async def callback(self, interaction: discord.Interaction):
            username = interaction.user.display_name
            if username != game_host:
                await (interaction.response.edit_message
                       (content=f'## {Runeterra.get_nickname(game_host)}님이 누른 것만 인식합니다. '
                                f'{Runeterra.get_nickname(username)}님 누르지 말아주세요.', view=self.view))
                return
            await ctx.send(f'메모장으로 진행합니다.')
            await interaction.message.delete()

    class AutoPlayButton(discord.ui.Button):
        def __init__(self):
            super().__init__(label=f"수습 마술사에게 팀뽑 맡기기", style=discord.ButtonStyle.primary)

        async def callback(self, interaction: discord.Interaction):
            await make_auto_team(ctx, participants)
            await interaction.message.delete()

    class UndoButton(discord.ui.Button):
        def __init__(self):
            super().__init__(label=f"명단 수정하기", style=discord.ButtonStyle.primary)

        async def callback(self, interaction: discord.Interaction):
            username = interaction.user.display_name
            if username != game_host:
                await (interaction.response.edit_message
                       (content=f'## {Runeterra.get_nickname(game_host)}님이 누른 것만 인식합니다. '
                                f'{Runeterra.get_nickname(username)}님 누르지 말아주세요.', view=self.view))
                return
            await interaction.message.delete()
            await close_normal_game(ctx, normal_game_log)

    handle_team_view = HandleTeamView()
    await ctx.send(content=f'## {Runeterra.get_nickname(game_host)}님, 팀장 두 분의 닉네임 버튼을 눌러주세요.', view=handle_team_view)


async def make_auto_team(ctx, participants):
    auto_teams = get_auto_team(participants)
    result_board = get_game_board(auto_teams)

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
            await handle_game_team(ctx, participants)

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
        user_result.append({'tier_score': get_tier_score(participant), 'username': participant})

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


async def choose_blue_red_game(ctx, team_head_list, members):
    await ctx.send(f'=========================================')
    # 블루팀 레드팀 고르기
    blue_team = []
    red_team = []

    team_head1 = team_head_list[0]
    team_head2 = team_head_list[1]

    while True:
        random_number1, random_number2 = random.randint(1, 6), random.randint(1, 6)

        await ctx.send(f'{Runeterra.get_nickname(team_head1)} > {random_number1} :'
                       f' {random_number2} < {Runeterra.get_nickname(team_head2)}')

        if random_number1 != random_number2:
            selected = team_head1 if random_number1 > random_number2 else team_head2
            not_selected = team_head2 if selected == team_head_list[0] else team_head1
            break

    class BlueRedView(discord.ui.View):
        def __init__(self):
            super().__init__(timeout=3600)

            blue_button = Button(label=f'블루팀', style=discord.ButtonStyle.primary)
            red_button = Button(label=f"레드팀", style=discord.ButtonStyle.red)

            blue_button.callback = lambda interaction: self.button_callback(interaction, team_type=True)
            red_button.callback = lambda interaction: self.button_callback(interaction, team_type=False)

            self.add_item(blue_button)
            self.add_item(red_button)

        async def button_callback(self, interaction: discord.Interaction, team_type: bool):
            username = interaction.user.display_name
            if username != selected:
                warning_message = (f'## {Runeterra.get_nickname(selected)}님이 누른 것만 인식합니다. '
                                   f'{Runeterra.get_nickname(username)}님 누르지 말아주세요.')
                await interaction.response.edit_message(content=warning_message, view=blue_red_view)
                return
            (blue_team if team_type else red_team).append(selected)
            (red_team if team_type else blue_team).append(not_selected)
            selected_team = '블루팀' if team_type else '레드팀'
            await ctx.send(f'{Runeterra.get_nickname(selected)}님이 {selected_team}을 선택하셨습니다.')
            await interaction.message.delete()
            await choose_order_game(ctx, blue_team, red_team, members)

    blue_red_view = BlueRedView()
    await ctx.send(content=f'## {Runeterra.get_nickname(selected)}님, 진영을 선택해주세요.', view=blue_red_view)


async def choose_order_game(ctx, blue_team, red_team, members):
    await ctx.send(f'=========================================')
    # 선뽑 후뽑 고르기
    teams = [blue_team, red_team]
    order_flag = True

    while True:
        random_number1, random_number2 = random.randint(1, 6), random.randint(1, 6)

        await ctx.send(f'{Runeterra.get_nickname(blue_team[0])} > {random_number1} :'
                       f' {random_number2} < {Runeterra.get_nickname(red_team[0])}')

        if random_number1 != random_number2:
            selected = blue_team[0] if random_number1 > random_number2 else red_team[0]
            order_flag = True if selected == blue_team[0] else False
            not_selected = red_team[0] if selected == blue_team[0] else blue_team[0]
            break

    class OrderView(discord.ui.View):
        def __init__(self):
            super().__init__(timeout=3600)

            first_pick_button = Button(label=f"선뽑(먼저 한명 뽑기)", style=discord.ButtonStyle.primary)
            second_pick_button = Button(label=f"후뽑(나중에 두명 뽑기)", style=discord.ButtonStyle.red)

            first_pick_button.callback = lambda interaction: self.button_callback(interaction, pick_type=True)
            second_pick_button.callback = lambda interaction: self.button_callback(interaction, pick_type=False)

            self.add_item(first_pick_button)
            self.add_item(second_pick_button)

        async def button_callback(self, interaction: discord.Interaction, pick_type):
            username = interaction.user.display_name
            if username != selected:
                warning_message = (f'## {Runeterra.get_nickname(selected)}님이 누른 것만 인식합니다. '
                                   f'{Runeterra.get_nickname(username)}님 누르지 말아주세요.')
                await interaction.response.edit_message(content=warning_message, view=order_view)
                return
            order_type = '선뽑' if pick_type else '후뽑'
            await ctx.send(f'{Runeterra.get_nickname(selected)}님이 {order_type}입니다.')
            await interaction.message.delete()
            await choose_game_team(ctx, teams, order_flag if pick_type else not order_flag, members)
            return

    order_view = OrderView()
    await ctx.send(content=f'## {Runeterra.get_nickname(selected)}님, 뽑는 순서를 정해주세요.', view=order_view)


async def choose_game_team(ctx, teams, flag, members):
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

    class ChooseGameView(discord.ui.View):
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
                await interaction.response.edit_message(
                    content=f'{get_game_board(teams)}\n## '
                            f'{Runeterra.get_nickname(team_head)}님이 누른 것만 인식합니다. '
                            f'{Runeterra.get_nickname(username)}님 누르지 말아주세요.',
                    view=self.view)
                return

            self.view.remove_item(self)
            self.view.members.remove(self.member)
            add_member_to_team(pick_order, teams, self.member.name)
            pick_order.pop(0)

            await ctx.send(f'{Runeterra.get_nickname(username)}님이 '
                           f'{Runeterra.get_nickname(self.member.name)}님을 '
                           f'{8 - len(pick_order)}번째로 뽑았습니다.')

            if len(pick_order) == 1:
                add_member_to_team(pick_order, teams, self.view.members[0].name)
                await interaction.message.delete()
                await ctx.send(get_game_board(teams))
                await ctx.send(f'밴픽은 아래 사이트에서 진행해주시면 됩니다.')
                await ctx.send(f'https://banpick.kr/')
                await ctx.send(f'사용자 설정 방 제목 : 룬테라 / 비밀번호 : 1234')
                return

            team_head = get_team_head(pick_order, teams)
            await interaction.response.edit_message(content=f'{get_game_board(teams)}\n## '
                                                            f'{Runeterra.get_nickname(team_head)}님, 팀원을 뽑아주세요.',
                                                    view=self.view)

    choose_game_view = ChooseGameView()
    await ctx.send(content=f'{get_game_board(teams)}\n## '
                           f'{Runeterra.get_nickname(get_team_head(pick_order, teams))}님, 팀원을 뽑아주세요.',
                   view=choose_game_view)

    # await ctx.send(get_game_board(teams))


def get_game_board(teams):
    board = f'```\n'
    board += f'🟦  블루진영\n\n'
    for blue_member in teams[0]:
        board += f'{blue_member}\n'
    board += f'\n🟥  레드진영\n\n'
    for red_member in teams[1]:
        board += f'{red_member}\n'
    board += f'```'
    return board
