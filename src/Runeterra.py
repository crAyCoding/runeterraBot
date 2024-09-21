# 몇 가지 필요한 Constant
line_names = ['탑', '정글', '미드', '원딜', '서폿']

# 현재 내전이 진행 중인지 확인
is_normal_game = False

# 일반 내전 참가자들을 담은 Log
normal_game_log = None

# 일반 내전이 진행 중인 채널
normal_game_channel = None

# 일반 내전 모집 호스트
normal_game_creator_id = None

# 20인 내전이 진행 중인지 확인
is_twenty_game = False

# 20인 내전 모집 호스트
twenty_host = None

# 20인 내전 경매 호스트
auction_host = None

# 20인 내전 유저 LIST
twenty_user_list = None

# 20인 내전 전용 View
twenty_game_view = None

# 40인 내전이 진행 중인지 확인
is_forty_game = False

# 40인 내전 유저 LIST
forty_user_list = None


class DiscordUser:
    def __init__(self, id, nickname):
        self.id = id
        self.nickname = nickname

    def __eq__(self, other):
        return isinstance(other, DiscordUser) and self.id == other.id

    def __hash__(self):
        return hash(self.id)


# 내전 채널 ID 목록
GAME_A_CHANNEL_ID = '1206635064444854363'
GAME_B_CHANNEL_ID = '1203295033378209852'
GAME_C_CHANNEL_ID = '1241055906695872574'
GAME_D_CHANNEL_ID = '1254453120801439925'
GAME_1_CHANNEL_ID = '1287068501416218665'
GAME_2_CHANNEL_ID = '1287069336896274473'
GAME_PLATINUM_CHANNEL_ID = '1277156618311696384'
GAME_EMERALD_CHANNEL_ID = '1238161553271029895'
GAME_DIAMOND_CHANNEL_ID = '1238164294680576000'
SPECIAL_GAME_CHANNEL_ID_LIST = [GAME_PLATINUM_CHANNEL_ID, GAME_EMERALD_CHANNEL_ID, GAME_DIAMOND_CHANNEL_ID]
TWENTY_RECRUIT_CHANNEL_ID = '1258779240766373939'
FORTY_RECRUIT_CHANNEL_ID = '1261028632680468481'
TWENTY_AUCTION_CHANNEL_ID = '1274316574135681024'

# 테스트 채널 ID
TEST_BY_OWN_CHANNEL_ID = '1258680400981528578'
TEST_WITH_OTHERS_CHANNEL_ID = '1258275050126184523'

# 관리자, 개발자 ID (추가 예정)
SORCERER = '333804390332760064'


def get_nickname(display_name: str):
    return display_name.split('/')[0].split('#')[0].strip()
