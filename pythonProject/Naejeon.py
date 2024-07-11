from SortFunctions import sort_participants

naejeon_creator = None

async def make_normal_naejeon(ctx, message = '3판 2선 모이면 바로 시작'):
    global naejeon_creator

    naejeon_creator = ctx.author.display_name
    await ctx.send(f'@everyone 내전 {message}')
    return True


async def magam_normal_naejeon(ctx, naejeon_log):
    global naejeon_creator

    if naejeon_creator != ctx.author.display_name:
        return True

    participants = set()

    for log in naejeon_log:
        participants.add(log['name'])

    if participants:
        participants_result = sort_participants(participants)

        await ctx.send(f'@everyone 내전 모집이 마감되었습니다. 모두 모여주세요.')
        await ctx.send(participants_result)


    naejeon_creator = None

    return False

async def jjong_normal_naejeon(ctx):
    global naejeon_creator

    if naejeon_creator == ctx.author.display_name:
        naejeon_creator = None
        await ctx.send(f'@everyone 쫑')