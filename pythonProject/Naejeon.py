from SortFunctions import sort_naejeon_members

naejeon_creator = None

async def make_normal_naejeon(ctx, message = '3판 2선 모이면 바로 시작'):
    # 일반 내전 모집
    global naejeon_creator

    naejeon_creator = ctx.author.display_name
    await ctx.send(f'@everyone 내전 {message}')
    return True


async def magam_normal_naejeon(ctx, naejeon_log):
    # 일반 내전 마감
    global naejeon_creator

    if naejeon_creator != ctx.author.display_name:
        return True

    participants = set()

    for log in naejeon_log:
        participants.add(log['name'])

    # 참여자가 한 명 이상인 경우
    if participants:
        user_result = sort_naejeon_members(participants)

        result = ''
        result += f'=========================================\n\n'
        for users in user_result:
            result += f'{users}\n'
        result += f'\n=========================================\n'

        await ctx.send(f'@everyone 내전 모집이 마감되었습니다. 모두 모여주세요.')
        await ctx.send(result)


    naejeon_creator = None

    return False

async def jjong_normal_naejeon(ctx):
    # 일반 내전 쫑
    global naejeon_creator

    if naejeon_creator != ctx.author.display_name:
        return True

    await ctx.send(f'@everyone 쫑')

    # 초기화
    naejeon_creator = None

    return False
