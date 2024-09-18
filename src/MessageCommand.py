def check_message(message: str):
    if len(message) < 1:
        return None

    if message[0] != '!':
        return None

    msg = message[1:]

    if msg == '미코피' or msg == '35P' or msg == '35p':
        mkp_text = '■■■■   ■■■■   ■   ■■■■   ■■■　   ■　　■   ■■■■   ■　　■\n'
        mkp_text += '■　　　   ■　　　   ■   ■　　■   ■　　■   ■　　■   ■　　　   ■　■\n'
        mkp_text += '■■■■   ■■■■   ■   ■■■■   ■　　■   ■　　■   ■　　　   ■■\n'
        mkp_text += '　　　■   　　　■   ■   ■　　　   ■　　■   ■　　■   ■　　　   ■　■\n'
        mkp_text += '■■■■   ■■■■   ■   ■　　　   ■■■　   ■■■■   ■■■■   ■　　■'
        return mkp_text

    if msg == '사냥꾼':
        return '20인내전 9연승 중'

    return None
