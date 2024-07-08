
from SortFunctions import sort_twenty_members
from TierScore import get_user_tier_score

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
                waiting_list += f'{user_info[line_number][0]}\n'

    if waiting_list == '':
        return waiting_list

    result = ''
    result += f'대기 명단\n'
    result += f'=========================================\n'
    result += waiting_list
    result += f'========================================='

    return result

