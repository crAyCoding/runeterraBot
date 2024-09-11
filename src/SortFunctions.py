def sort_game_members(participants: list):
    # 티어별로 정리

    challenger_users = list()
    grandmaster_users = list()
    master_users = list()
    diamond_users = list()
    emerald_users = list()
    platinum_users = list()
    gold_users = list()
    silver_users = list()
    bronze_users = list()
    iron_users = list()
    unranked_users = list()

    for user in participants:
        splitted_user_profile = user.split('/')
        user_tier = splitted_user_profile[1].strip()
        if user_tier[0] == '🔻' or user_tier[0] == '🔺':
            user_tier = user_tier[1:]

        user_level = user_tier[0].upper()

        if user_level == 'C':
            user_score = int(user_tier[1:])
            challenger_users.append((user_score, user))

        if user_level == 'G' and user_tier[1].upper() == 'M':
            user_score = int(user_tier[2:])
            grandmaster_users.append((user_score, user))

        if user_level == 'M':
            user_score = int(user_tier[1:])
            master_users.append((user_score, user))

        if user_level == 'D':
            user_score = int(user_tier[1:])
            diamond_users.append((user_score, user))

        if user_level == 'E':
            user_score = int(user_tier[1:])
            emerald_users.append((user_score, user))

        if user_level == 'P':
            user_score = int(user_tier[1:])
            platinum_users.append((user_score, user))

        if user_level == 'G' and user_tier[1].upper() != 'M':
            user_score = int(user_tier[1:])
            gold_users.append((user_score, user))

        if user_level == 'S':
            user_score = int(user_tier[1:])
            silver_users.append((user_score, user))

        if user_level == 'B':
            user_score = int(user_tier[1:])
            bronze_users.append((user_score, user))

        if user_level == 'I':
            user_score = int(user_tier[1:])
            iron_users.append((user_score, user))

        if user_level == 'U':
            user_score = 0
            unranked_users.append((user_score, user))

    user_result = list()

    if challenger_users:
        challenger_users.sort(key=lambda pair: pair[0], reverse=True)
        for user in challenger_users:
            user_result.append(user[1])

    if grandmaster_users:
        grandmaster_users.sort(key=lambda pair: pair[0], reverse=True)
        for user in grandmaster_users:
            user_result.append(user[1])

    if master_users:
        master_users.sort(key=lambda pair: pair[0], reverse=True)
        for user in master_users:
            user_result.append(user[1])

    if diamond_users:
        diamond_users.sort(key=lambda pair: pair[0])
        for user in diamond_users:
            user_result.append(user[1])

    if emerald_users:
        emerald_users.sort(key=lambda pair: pair[0])
        for user in emerald_users:
            user_result.append(user[1])

    if platinum_users:
        platinum_users.sort(key=lambda pair: pair[0])
        for user in platinum_users:
            user_result.append(user[1])

    if gold_users:
        gold_users.sort(key=lambda pair: pair[0])
        for user in gold_users:
            user_result.append(user[1])

    if silver_users:
        silver_users.sort(key=lambda pair: pair[0])
        for user in silver_users:
            user_result.append(user[1])

    if bronze_users:
        bronze_users.sort(key=lambda pair: pair[0])
        for user in bronze_users:
            user_result.append(user[1])

    if unranked_users:
        for user in unranked_users:
            user_result.append(user[1])


    return user_result

def get_result_sorted_by_tier(user_result: list):
    now_tier = ''
    result = ''
    result += f'=========================================\n\n'
    for user in user_result:
        splitted_user_profile = user.split('/')
        user_tier = splitted_user_profile[1].strip()
        if user_tier[0] == '🔻' or user_tier[0] == '🔺':
            user_tier = user_tier[1:]
        user_level = user_tier[0].upper()
        if now_tier == '':
            now_tier = user_level
        elif now_tier != user_level:
            now_tier = user_level
            result += f'\n'
        result += f'{user}\n'
    result += f'\n=========================================\n'

    return result

def get_tier_score(user):
    splitted_user_profile = user.split('/')
    user_tier = splitted_user_profile[1].strip()
    if user_tier[0] == '🔻' or user_tier[0] == '🔺':
        user_tier = user_tier[1:]

    user_level = user_tier[0].upper()

    # I B S G P E D M GM C

    if user_level == 'C':
        return int(user_tier[1:]) + 2800

    if user_level == 'G' and user_tier[1].upper() == 'M':
        return int(user_tier[2:]) + 2800

    if user_level == 'M':
        return int(user_tier[1:]) + 2800

    if user_level == 'D':
        return (4 - int(user_tier[1:])) * 100 + 2400

    if user_level == 'E':
        return (4 - int(user_tier[1:])) * 100 + 2000

    if user_level == 'P':
        return (4 - int(user_tier[1:])) * 100 + 1600

    if user_level == 'G' and user_tier[1].upper() != 'M':
        return (4 - int(user_tier[1:])) * 100 + 1200

    if user_level == 'S':
        return (4 - int(user_tier[1:])) * 100 + 800

    if user_level == 'B':
        return (4 - int(user_tier[1:])) * 100 + 400

    if user_level == 'I':
        return (4 - int(user_tier[1:])) * 100

    if user_level == 'U':
        return 0
