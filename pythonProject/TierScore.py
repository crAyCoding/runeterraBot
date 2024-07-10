def get_user_tier_score(user: str):
    splitted_user_profile = user.split('/')
    user_name = splitted_user_profile[0].strip()
    user_tier = splitted_user_profile[1].strip()
    if user_tier[0] == '🔻' or user_tier[0] == '🔺':
        user_tier = user_tier[1:]


    user_level = user_tier[0].upper()

    result = 300

    if user_level == 'C':
        user_score = int(user_tier[1:])
        user_editted_score = (user_score // 100) * 10
        result -= user_editted_score

    if user_level == 'G' and user_tier[1].upper() == 'M':
        user_score = int(user_tier[2:])
        user_editted_score = (user_score // 100) * 10
        result -= user_editted_score

    if user_level == 'M':
        user_score = int(user_tier[1:])
        user_editted_score = (user_score // 100) * 10
        result -= user_editted_score

    if user_level == 'D':
        user_score = int(user_tier[1:])
        result += (user_score * 10)

    if user_level == 'E':
        user_score = int(user_tier[1:])
        result += 40
        result += (user_score * 10)

    if user_level == 'P':
        user_score = int(user_tier[1:])
        result += 80
        result += (user_score * 10)

    if user_level == 'G' and user_tier[1].upper() != 'M':
        user_score = int(user_tier[1:])
        result += 120
        result += (user_score * 10)

    if user_level == 'S':
        user_score = int(user_tier[1:])
        result += 160
        result += (user_score * 10)

    if user_level == 'B':
        user_score = int(user_tier[1:])
        result += 200
        result += (user_score * 10)

    if user_level == 'I':
        user_score = int(user_tier[1:])
        result += 240
        result += (user_score * 10)

    if user_level == 'U':
        result = 1000000

    return result