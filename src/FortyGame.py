from discord.ui import Button, View
from TwentyGame import get_naejeon_warning, get_team_head_lineup, get_team_head_number, get_user_lineup, get_waiting_list
import discord

# 각 라인별 인원 담는 배열
user_info = None
# 투표 받을 View
naejeon_view = None
# 내전 생성자
naejeon_creator = None
# 투표를 보낸 메세지를 저장할 변수
view_message = None


async def make_fourty_naejeon(ctx, message='모이면 바로 시작'):
    global user_info, naejeon_view, naejeon_creator, view_message

    class FourtyView(View):
        def __init__(self):
            # 투표 제한 시간 설정, 40인 내전은 12시간으로 설정
            super().__init__(timeout=36000)

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
                # 8표 이상이면 버튼 색 빨간색으로 설정
                button.style = discord.ButtonStyle.red if len(user_info[line_number]) >= 8 else discord.ButtonStyle.gray

                await interaction.response.edit_message(view=self)

            return callback

    user_info = [[], [], [], [], []]
    naejeon_view = FourtyView()
    naejeon_creator = ctx.author.display_name
    view_message = await ctx.send(embed=discord.Embed(title=f'40인 내전 {message}'), view=naejeon_view)
    await ctx.send(f'@everyone 40인 내전 {message}')

    return True

async def magam_fourty_naejeon(ctx):
    global user_info, naejeon_view, naejeon_creator, view_message

    if naejeon_creator != ctx.author.display_name:
        return True

    naejeon_members = 40

    team_head_line_number = get_team_head_number(user_info, naejeon_members)
    waiting_people_list = get_waiting_list(user_info, naejeon_members)

    await ctx.send(get_team_head_lineup(team_head_line_number, user_info, naejeon_members))
    await ctx.send(get_user_lineup(team_head_line_number, user_info, naejeon_members))
    await ctx.send(get_naejeon_warning(naejeon_members))

    if waiting_people_list != '':
        await ctx.send(waiting_people_list)

    await ctx.send(f'@everyone {naejeon_members}인 내전 모집이 완료되었습니다. 결과를 확인해주세요')

    # 초기화
    await view_message.delete()
    naejeon_creator = None
    naejeon_view = None
    view_message = None
    user_info = None

    return False

async def jjong_fourty_naejeon(ctx):
    global user_info, naejeon_view, view_message, naejeon_creator

    if naejeon_creator != ctx.author.display_name:
        return True

    await ctx.send(f'@everyone 40인 내전 쫑')

    # 초기화
    await view_message.delete()
    naejeon_creator = None
    naejeon_view = None
    view_message = None
    user_info = None

    return False
