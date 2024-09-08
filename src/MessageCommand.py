import random


def checkMessage(message: str):

    if len(message) < 1:
        return None

    if message[0] != '!':
        return None

    msg = message[1:]

    if msg == '미코피' or msg == '35P' or msg == '35p':
        return ':regional_indicator_s: :regional_indicator_s: :regional_indicator_i: :regional_indicator_p: :regional_indicator_d: :regional_indicator_u: :regional_indicator_c: :regional_indicator_k: '

    return None