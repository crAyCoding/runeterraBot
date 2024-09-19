from datetime import datetime
from discord.ui import Button, View
from SortFunctions import sort_game_members
from TierScore import get_user_tier_score
import discord
import Runeterra

# 각 라인별 인원 담는 배열
user_info = None
# 투표 받을 View
game_view = None
# 내전 생성자
game_creator = None
# 투표를 보낸 메세지를 저장할 변수
view_message = None
# 팀장 목록 텍스트
team_head_lineup = None
# 팀원 목록 텍스트
team_user_lineup = None


async def make_twenty_game(ctx, message='모이면 바로 시작'):
    # 20인 내전 모집

    def create_callback(line_name, button):
        # 버튼 상호작용 함수

        async def callback(interaction: discord.Interaction):
            user = Runeterra.DiscordUser(interaction.user.id, interaction.user.display_name)
            is_valid_push = True

            # 같은 라인에 이미 등록했는지 체크, 등록했다면 유저 삭제
            for line_user in Runeterra.twenty_user_list[line_name]:
                if user.id == line_user.id:
                    Runeterra.twenty_user_list[line_name].remove(line_user)
                    is_valid_push = False
                    break

            # 다른 라인에 등록했는지 체크, 등록되어 있으면 상호작용 무시
            for line_users in Runeterra.twenty_user_list.values():
                for line_user in line_users:
                    if user.id == line_user.id:
                        is_valid_push = False
                        break

            # 위 두 사항에 해당되지 않는 경우, 해당 라인에 참여시키고 메세지 출력
            if is_valid_push:
                Runeterra.twenty_user_list[line_name].append(user)

            button.label = f"{line_name} : {len(Runeterra.twenty_user_list[line_name])}"
            # 4표 이상이면 버튼 색 빨간색으로 설정
            button.style = discord.ButtonStyle.red \
                if len(Runeterra.twenty_user_list[line_name]) >= 4 else discord.ButtonStyle.gray

            await interaction.response.edit_message(content=get_twenty_recruit_board(message), view=game_view)

        return callback

    class TwentyView(View):
        def __init__(self):
            # 투표 제한 시간 설정, 20인 내전은 12시간으로 설정
            super().__init__(timeout=43200)

            self.buttons = [
                Button(label=f'{line_name} : 0', style=discord.ButtonStyle.gray)
                for line_name in Runeterra.line_names
            ]

            for line_number, button in enumerate(self.buttons):
                button.callback = create_callback(Runeterra.line_names[line_number], button)

                self.add_item(button)

    # 변수 초기화, 새 내전 생성
    Runeterra.twenty_user_list = {line_name: [] for line_name in Runeterra.line_names}
    Runeterra.twenty_game_view = TwentyView()
    Runeterra.twenty_host = ctx.author.id
    await ctx.send(content=get_twenty_recruit_board(message), view=game_view)
    await ctx.send(f'@everyone 20인 내전 {message}')
    await ctx.send(f'이미 모집된 라인(버튼이 빨간색인 경우)에 참여를 원하는 경우, 버튼을 누르시면 자동으로 대기 목록에 추가됩니다.')

    # 내전이 생성되었다는 True 값 반환
    return True


async def close_twenty_game(ctx):
    # 20인 내전 마감

    if Runeterra.twenty_host != ctx.author.id:
        return True

    game_members = 20

    # 팀장 라인 번호 찾기
    team_head_line_number = get_team_head_number(game_members)
    # 대기자 리스트 추출
    waiting_people_list = get_waiting_list(game_members)
    # 팀장 텍스트
    team_head_lineup = get_team_head_lineup(team_head_line_number, game_members)
    # 팀원 텍스트
    team_user_lineup = get_user_lineup(team_head_line_number, game_members)

    await ctx.send(team_head_lineup)
    await ctx.send(team_user_lineup)
    if waiting_people_list != '':
        await ctx.send(waiting_people_list)

    await ctx.send(get_game_warning(game_members))

    await ctx.send(f'@everyone {game_members}인 내전 모집이 완료되었습니다. 결과를 확인해주세요')
    await ctx.send(f'20인내전경매 채널에서 !경매 를 통해 경매를 시작할 수 있습니다.')

    # 초기화
    Runeterra.twenty_user_list = None
    Runeterra.twenty_host = None
    Runeterra.twenty_game_view = None

    return False


async def end_twenty_game(ctx):
    # 20인 내전 쫑

    if Runeterra.twenty_host != ctx.author.id:
        return True

    await ctx.send(f'@everyone 20인 내전 쫑')

    # 초기화
    Runeterra.twenty_user_list = None
    Runeterra.twenty_host = None
    Runeterra.twenty_game_view = None

    return False


def get_team_head_number(game_members: int):
    # 팀장 찾기
    # 각 라인별 최대 점수, 최소 점수를 구해서 차이가 가장 적은 라인 반환

    min_diff = float('inf')
    line_number = -1

    for index, (line_name, user_list) in enumerate(Runeterra.twenty_user_list.items()
                                                   if game_members == 20 else Runeterra.forty_user_list.items()):
        if len(user_list) < (game_members // 5):
            continue
        scores = [get_user_tier_score(user) for user in user_list[:(game_members // 5)]]

        if scores:
            diff = max(scores) - min(scores)

            if 0 <= diff < min_diff:
                min_diff = diff
                line_number = index

    return line_number


def get_team_head_lineup(head_line_number: int, game_members: int):
    # 팀장 결과 반환

    line_name = Runeterra.line_names[head_line_number]

    result = ''
    result += f'팀장 : {line_name}\n'
    result += f'=========================================\n\n'

    user_list = Runeterra.twenty_user_list if game_members == 20 else Runeterra.forty_user_list

    participants = [user.nickname for user in user_list[line_name][:(game_members // 5)]]

    users = sort_game_members(participants)

    for i, user_nickname in enumerate(users):
        result += f'{i + 1}팀\n'
        user_score = get_user_tier_score(user_nickname)
        result += f'{user_nickname} : {user_score}\n\n'

    result += f'=========================================\n\n\n'

    return result


# 여기부터 작업하면 됨!! 아마 잘 될듯?> 몰루? 시발 어제의 나 왜 여기서 관뒀냐..?

def get_user_lineup(head_line_number: int, game_members: int):
    # 팀원 결과 반환

    result = ''
    result += f'팀원\n'
    result += f'=========================================\n\n'

    user_list = Runeterra.twenty_user_list if game_members == 20 else Runeterra.forty_user_list

    for line_number, (line_name, users) in enumerate(user_list.items()):
        if line_number == head_line_number:
            continue

        print(users)

        participants = []

        for i in range(min((game_members // 5), len(user_info[line_number]))):
            participants.append(user_info[line_number][i])

        users = sort_game_members(participants)

        result += f'### {line_name}\n\n'

        for i in range(len(users)):
            result += f'{users[i]}\n'

        result += f' \n'

    result += f'========================================='

    return result


def get_waiting_list(user_info: list, game_members: int):
    # 대기자 명단 반환

    line_names = ['탑', '정글', '미드', '원딜', '서폿']

    waiting_list = ''

    for line_number in range(len(user_info)):
        for i in range(len(user_info[line_number])):
            if i == (game_members // 5):
                waiting_list += f'{line_names[line_number]}\n'

            if i >= (game_members // 5):
                waiting_list += f'{user_info[line_number][i]}\n'

    if waiting_list == '':
        return waiting_list

    result = ''
    result += f'대기 명단\n'
    result += f'=========================================\n'
    result += waiting_list
    result += f'========================================='

    return result


def get_game_warning(game_members: int):
    warning_text = ''

    warning_text += f'20인 내전은 경매로 진행됩니다.\n'
    warning_text += f'자세한 규칙은 20인-40인 내전 규칙 채널에서 확인하실 수 있습니다.\n'
    warning_text += f'즐거운 {game_members}인 내전 되시길 바랍 니다!!'

    """
    warning_text += f'경매 방식\n\n'
    warning_text += f'1. 입찰은 10 단위로 하되 갱신에는 제한이 없습니다.\n'
    warning_text += f'2. 각 라인별 남은 마지막 매물(유찰포함)은 그 라인이 없는 팀이 무료로 데려갑니다.\n'
    warning_text += f'   ex) 서폿에 제트님만 남을시 서폿 없는 팀이 제트님을 무료로 데려갑니다.\n'
    warning_text += f'3. 입찰에 참여를 할때 팀명과 가격을 말해주세요.\n'
    warning_text += f'   ex) 1팀 20 이런 방식으로 해주세요.\n'
    warning_text += f'4. 경매가 끝나고 돈이 제일 많이 남은 팀은 상대팀 지목 및 진영선택권을 가져갑니다.\n\n'
    warning_text += f'경매 유의사항\n\n'
    warning_text += f'1. 처음부터 올인을 하거나 반대로 너무 아낄 경우에는 대참사가 일어날 수 있습니다. 현명한 결정 응원합니다.\n'
    warning_text += f'2. 경매중에는 팀장 외 마이크는 다 꺼주시기 바랍니다.\n'
    warning_text += f'3. 경매가 익숙하지 않을 수 있습니다.\n'
    warning_text += f'   그러나 경매결과가 맘에 들지 않는다고 불평하는 자세는 지양해주시기 바랍니다.\n'
    warning_text += f'4. 3번 사항이 관리자 혹은 진행자에게 적발이 될 경우 경고를 부여하겠습니다.\n\n'
    """

    return warning_text


def get_twenty_recruit_board(message):
    team_head_number = get_team_head_number(20)

    twenty_recruit_board = ''

    twenty_recruit_board += f'```\n'

    today_text = datetime.now().strftime("%m월 %d일 20인 내전")

    twenty_recruit_board += f'{today_text} {message}\n\n'

    for i in range(0, 5):
        twenty_recruit_board += f'{Runeterra.line_names[i]}'
        if i == team_head_number:
            twenty_recruit_board += f' (팀장)'
        twenty_recruit_board += f'\n'
        for number, (line_name, user_list) in enumerate(Runeterra.twenty_user_list.items):
            if number >= 4:
                twenty_recruit_board += f'(대기) '
            else:
                twenty_recruit_board += f'{number + 1}. '
            twenty_recruit_board += f'{user}\n'
        twenty_recruit_board += f'\n'

    twenty_recruit_board += f'```'

    return twenty_recruit_board


def reset_twenty_game(ctx):
    global user_info

    user_info = None
