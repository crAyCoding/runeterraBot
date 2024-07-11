def checkMessage(message: str):

    if len(message) < 1:
        return None

    if message[0] != '!':
        return None

    msg = message[1:]

    if msg == '권기현':
        return '날쌔지 않음'

    if msg == '절구' or msg == '김절구':
        f_message = f'```ansi\n'
        f_message += f'[0;35m@@22男 남친 구합니다 원하시는 분 DM@@[0m\n'
        f_message += f'```'
        return f_message

    if msg == '배리나':
        return '300KG'

    if msg == '제우스':
        return '점수먹는 하마'

    if msg == '제드에코' or msg == '재진':
        return '다딱'

    if msg == '원더맛':
        return '에메딱'

    if msg == '뭘봐':
        return '마술사의 샌드백'

    if msg == '규진' or msg == '이규진':
        return '니달리 장인'

    if msg == '제이' or msg == '윤제이':
        return '이렐리아 장인'

    if msg == '준혁' or msg == '야요':
        return '탑징징'

    if msg == '미코피' or msg == '35p' or msg == '35P':
        return '씹덕'

    if msg == '모기':
        return '애디 밑'

    if msg == '재슥' or msg == '슥재슥':
        return '3회 우승자(다소못함)'

    if msg == '애디':
        return '광탈의 제왕 애디'

    if msg == '페레로':

        f_message = f'```ansi\n'
        f_message += f'[0;35m@@남친 구합니다 20男 여성분 사절@@[0m\n'
        f_message += f'```'
        return f_message

    if msg == '스흑':

        f_message = f'```ansi\n'
        f_message += f'[0;34m사 랑 해 요 김 절 구 내 사 랑[0m\n'
        f_message += f'```'
        return f_message

    if msg == '김윤혁':
        return '잼민이'

    if msg == '아캅스' or msg == 'pnpm':

        f_message = f'```ansi\n'
        f_message += f'[0;33m26男, 늦었지만 원딜 프로 준비합니다.[0m\n'
        f_message += f'```'
        return f_message

    return None