def get_user_tier_score(user: str):
    splitted_user_profile = user.split('/')
    user_name = splitted_user_profile[0].strip()
    user_tier = splitted_user_profile[1].strip()
    if user_tier[0] == '🔻' or user_tier[0] == '🔺':
        user_tier = user_tier[1:]


    user_level = user_tier[0].upper()

    if user_level == 'G' and user_tier[1].upper() == 'M':
        user_score = int(user_tier[2:])
    else:
        user_score = int(user_tier[1:])

    def get_editted_score(user_score):
        return (user_score // 100) * 10

    score_by_tier = {
        'C': -get_editted_score(user_score),
        'G': -get_editted_score(user_score) if user_tier[1].upper() == 'M' else (user_score * 10) + 120,
        'M': -get_editted_score(user_score),
        'D': user_score * 10,
        'E': (user_score * 10) + 40,
        'P': (user_score * 10) + 80,
        'S': (user_score * 10) + 160,
        'B': (user_score * 10) + 200,
        'I': (user_score * 10) + 240
    }

    default_score = 300

    if user_level in score_by_tier:
        return default_score + score_by_tier[user_level]
    else:
        return 99999999