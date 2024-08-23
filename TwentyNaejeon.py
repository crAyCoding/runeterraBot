from discord.ui import Button, View, Modal
from SortFunctions import sort_naejeon_members
from TierScore import get_user_tier_score
import discord


# 각 라인별 인원 담는 배열
user_info = None
# 투표 받을 View
naejeon_view = None
# 내전 생성자
naejeon_creator = None
# 투표를 보낸 메세지를 저장할 변수
view_message = None
# 팀장 목록 텍스트
team_head_lineup = None
# 팀원 목록 텍스트
team_user_lineup = None


async def make_twenty_naejeon(ctx, message='모이면 바로 시작'):
    # 20인 내전 모집
    global user_info, naejeon_view, naejeon_creator, view_message

    class TwentyView(View):
        def __init__(self):
            # 투표 제한 시간 설정, 20인 내전은 6시간으로 설정
            super().__init__(timeout=21600)

            self.line_names = ['탑', '정글', '미드', '원딜', '서폿']

            self.buttons = [
                Button(label=f'{line_name} : 0', style=discord.ButtonStyle.gray)
                for line_name in self.line_names
            ]

            for i, button in enumerate(self.buttons):
                button.callback = self.create_callback(i, button)

                self.add_item(button)

        def create_callback(self, line_number, button):
            # 버튼 상호작용 함수
            line_name = self.line_names[line_number]

            async def callback(interaction: discord.Interaction):
                username = interaction.user.display_name
                flag = True

                # 같은 라인에 이미 등록했는지 체크, 등록했다면 유저 삭제
                for i in range(len(user_info[line_number])):
                    if user_info[line_number][i][0] == username:
                        original_message = await interaction.channel.fetch_message(user_info[line_number][i][1])
                        await original_message.delete()
                        del user_info[line_number][i]
                        flag = False
                        break

                # 다른 라인에 등록했는지 체크, 등록되어 있으면 상호작용 무시
                for i in range(len(user_info)):
                    if i == line_number:
                        continue
                    for j in range(len(user_info[i])):
                        if user_info[i][j][0] == username:
                            flag = False

                # 위 두 사항에 해당되지 않는 경우, 해당 라인에 참여시키고 메세지 출력
                if flag:
                    message = await interaction.channel.send(f'{username} 님이 {line_name}로 참여합니다!')
                    user_info[line_number].append((username, message.id))

                button.label = f"{line_name} : {len(user_info[line_number])}"
                # 4표 이상이면 버튼 색 빨간색으로 설정
                button.style = discord.ButtonStyle.red if len(user_info[line_number]) >= 4 else discord.ButtonStyle.gray

                await interaction.response.edit_message(view=self)

            return callback

    # 변수 초기화, 새 내전 생성
    user_info = [[], [], [], [], []]
    naejeon_view = TwentyView()
    naejeon_creator = ctx.author.display_name
    view_message = await ctx.send(embed=discord.Embed(title=f'20인 내전 {message}'), view=naejeon_view)
    await ctx.send(f'@everyone 20인 내전 {message}')
    await ctx.send(f'이미 모집된 라인(버튼이 빨간색인 경우)에 참여를 원하는 경우, 버튼을 누르시면 자동으로 대기 목록에 추가됩니다.')

    # 내전이 생성되었다는 True 값 반환
    return True


async def magam_twenty_naejeon(ctx):
    # 20인 내전 마감
    global user_info, naejeon_view, naejeon_creator, view_message

    if naejeon_creator != ctx.author.display_name:
        return True

    naejeon_members = 20

    # 팀장 라인 번호 찾기
    team_head_line_number = get_team_head_number(user_info, naejeon_members)
    # 대기자 리스트 추출
    waiting_people_list = get_waiting_list(user_info, naejeon_members)
    # 팀장 텍스트
    team_head_lineup = get_team_head_lineup(team_head_line_number, user_info, naejeon_members)
    # 팀원 텍스트
    team_user_lineup = get_user_lineup(team_head_line_number, user_info, naejeon_members)

    await ctx.send(team_head_lineup)
    await ctx.send(team_user_lineup)
    if waiting_people_list != '':
        await ctx.send(waiting_people_list)

    await ctx.send(get_naejeon_warning(naejeon_members))

    from TwentyAuction import add_user_info

    await add_user_info(user_info)

    await ctx.send(f'@everyone {naejeon_members}인 내전 모집이 완료되었습니다. 결과를 확인해주세요')
    await ctx.send(f'20인내전경매 채널에서 !경매 를 통해 경매를 시작할 수 있습니다.')

    # 초기화
    await view_message.delete()
    naejeon_creator = None
    naejeon_view = None
    view_message = None
    user_info = None

    return False


async def jjong_twenty_naejeon(ctx):
    # 20인 내전 쫑
    global user_info, naejeon_view, view_message, naejeon_creator

    if naejeon_creator != ctx.author.display_name:
        return True

    await ctx.send(f'@everyone 20인 내전 쫑')

    # 초기화
    await view_message.delete()
    naejeon_creator = None
    naejeon_view = None
    view_message = None
    user_info = None

    return False


def get_team_head_number(user_info: list, naejeon_members: int):
    # 팀장 찾기
    # 각 라인별 최대 점수, 최소 점수를 구해서 차이가 가장 적은 라인 반환

    min_diff = float('inf')
    line_number = 0

    for i, users in enumerate(user_info):
        scores = [get_user_tier_score(user[0]) for user in users[:(naejeon_members // 5)]]

        if scores:
            diff = max(scores) - min(scores)

            if 0 <= diff < min_diff:
                min_diff = diff
                line_number = i

    return line_number


def get_team_head_lineup(line_number: int, user_info: list, naejeon_members: int):
    # 팀장 결과 반환

    line_names = ['탑', '정글', '미드', '원딜', '서폿']
    line_name = line_names[line_number]

    result = ''
    result += f'팀장 : {line_name}\n'
    result += f'=========================================\n\n'

    participants = []

    for i in range(min((naejeon_members // 5), len(user_info[line_number]))):
        participants.append(user_info[line_number][i][0])

    users = sort_naejeon_members(participants)

    for i in range(min((naejeon_members // 5), len(users))):
        result += f'{i + 1}팀\n'
        user_score = get_user_tier_score(users[i])
        result += f'{users[i]} : {user_score}\n\n'

    result += f'=========================================\n\n\n'

    return result


def get_user_lineup(head_line_number: int, user_info: list, naejeon_members: int):
    # 팀원 결과 반환

    line_names = ['탑', '정글', '미드', '원딜', '서폿']

    result = ''
    result += f'팀원\n'
    result += f'=========================================\n\n'

    for line_number in range(len(user_info)):
        if line_number == head_line_number:
            continue

        participants = []

        for i in range(min((naejeon_members // 5), len(user_info[line_number]))):
            participants.append(user_info[line_number][i][0])

        users = sort_naejeon_members(participants)

        line_name = line_names[line_number]

        result += f'### {line_name}\n\n'

        for i in range(len(users)):
            result += f'{users[i]}\n'

        result += f' \n'

    result += f'========================================='

    return result


def get_waiting_list(user_info: list, naejeon_members: int):
    # 대기자 명단 반환

    line_names = ['탑', '정글', '미드', '원딜', '서폿']

    waiting_list = ''

    for line_number in range(len(user_info)):
        for i in range(len(user_info[line_number])):
            if i == (naejeon_members // 5):
                waiting_list += f'{line_names[line_number]}\n'

            if i >= (naejeon_members // 5):
                waiting_list += f'{user_info[line_number][i][0]}\n'

    if waiting_list == '':
        return waiting_list

    result = ''
    result += f'대기 명단\n'
    result += f'=========================================\n'
    result += waiting_list
    result += f'========================================='

    return result


def get_naejeon_warning(naejeon_members: int):
    warning_text = ''

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
    warning_text += f'즐거운 {naejeon_members}인 내전 되시길 바랍니다!!'

    return warning_text

async def test_add_twenty():
    global user_info

    user_info = [[],[],[],[],[]]
    index = -1
    with open('twentyex.txt', 'r', encoding='utf-8') as file:
        lines = [line.strip() for line in file.readlines()]
        for i in range(20):
            if i % 4 == 0:
                index += 1
            user_info[index].append((lines[i], ''))

    from TwentyAuction import add_user_info

    await add_user_info(user_info)