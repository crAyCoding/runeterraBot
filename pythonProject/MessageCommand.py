import random


def checkMessage(message: str):

    return None

    if len(message) < 1:
        return None

    if message[0] != '!':
        return None

    msg = message[1:]

    if msg == '권기현':
        return '자존감낮음 맨날자책함 녹턴궁맨날켜져있음'

    if msg == '절구' or msg == '김절구':
        return '스흑이랑 밀당하는 중'

    if msg == '제우스' or msg == '장우혁':
        return '### 벌레'

    if msg == '제드에코' or msg == '재진' or msg == "삶지사":
        return '눈치안보는 다딱이'

    if msg == '원더맛':
        return '유튜브 더럽게 맛있다 진짜로'

    if msg == '뭘봐':
        return '마술사의 샌드백'

    if msg == '규진' or msg == '이규진':
        return '니달리 장인'

    if msg == '제이' or msg == '윤제이':
        return '스크림 파토 장인'

    if msg == '준혁' or msg == '야요':
        return '탑징징'

    if msg == '미코피' or msg == '35p' or msg == '35P':
        return '느낌있는 멋진 잘생긴 롤잘하는 어쩌구.. 인 씹덕'

    if msg == '재슥' or msg == '슥재슥':
        return '3회 우승자(다소못함)'

    if msg == '애디':
        return '광탈의 제왕 애디'

    if msg == '페레로' or msg == '김지훈':
        return '혜린(자오밍아님)님과 썸타는중'

    if msg == '혜린':
        return '페레로와 썸타는중'

    if msg == '스흑':
        return '김절구 다시 노리는 중'

    if msg == '김윤혁' or msg == '윤혁':
        return '2주 안에 경고 먹고 나갈 사람인데... 굳이 언급을?'

    if msg == '아캅스' or msg == 'pnpm':

        f_message = f'```ansi\n'
        f_message += f'[0;33m티어값 못하는 여미새 탑 라이너[0m\n'
        f_message += f'```'
        return f_message

    if msg == '순두부' or msg == '순찌정':
        return '나 페레론데...'

    if msg == '쥬예':
        # return '# 👸🏻 쥬 예 곤 듀 등 장 👸🏻'
        return f'_롤체에 45만원 박고 저녁에 컵라면 시키는 남자_'

    if msg == '호빵맨':
        return '틀딱챔만하는 챔프폭'

    if msg == '김하준':
        return '리신3캠 2렙 기적의동선'

    if msg == '이토빙':
        return '챌린저 1200점 인줄 아는 그냥 예티'

    if msg == '광대' or msg == '배리나':
        random_value = random.randint(120, 300)
        return f'{random_value}KG'

    if msg == '워노야':
        return '정글만 마스터 다른라인 다딱이'

    if msg == '하프':
        return '이토빙♡'

    if msg == '킹유미':
        return '# 🤴🏻 유 미 왕 댜 등 장 🤴🏻'

    if msg == '세트' or msg == '제트':
        return '이 사람 없으면 절구팀 우승인데... - 원더맛'

    if msg == '원짜이':
        return '히또'

    if msg == '백구':
        return '노쇼의 장인'

    if msg == '카리나':
        return '# 👊 로 켓 펀 처 👊'

    if msg == 'TEST':
        return '테스트메세지입니다 이걸 왜 입력을하시는지?'

    return None