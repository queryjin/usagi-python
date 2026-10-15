"""우사기: 야하! 우라! 푸루야!"""

from __future__ import annotations

import re

from ..core import Character, Chatter, Expression

YAHA = Expression("야하", ("찾았다!", "등장!"), "뭔가를 찾았을 때, 혹은 등장할 때")
URA = Expression("우라", ("최근", "거대하다"), "최근 / 거대하다 (상황에 따라 다름)")
PURUYA = Expression("푸루야", ("같이 하자!", "따라와!", "힘내!"), "공감 요구, 따라오라는 초대, 응원")
PURU = Expression("푸루", ("알겠어", "잡초 이름"), "잡초 이름, 알겠어")
HAA = Expression("하아?", ("뭐야?", "놀랐어!", "어이없네"), "뭐야?, 놀랐을 때, 어이없을 때")
HUNG = Expression("후응", ("맞아",), "맞아 (긍정의 의미)")
JURURI = Expression("쥬르리", ("먹고 싶다…",), "식욕이 돌 때")
MIYAAA = Expression("미야아아", ("어서 오세요",), "어서 오세요")
UA = Expression("우아", ("맛있다",), "맛있다")
PURUYA_URAURA = Expression(
    "푸루야우라우라", ("해독 불가능한 기괴한 괴성",), "해독 불가능한 기괴한 괴성", loud=True
)

RULES = (
    (PURUYA_URAURA, re.compile(r"ㅋㅋㅋㅋ|ㅎㅎㅎㅎ|!!!|미쳤|미친|대박|난리|으아아|crazy|wtf|lol", re.I)),
    (UA, re.compile(r"맛있|맛나|꿀맛|존맛|yummy|delicious|tasty", re.I)),
    (JURURI, re.compile(r"배고|배가 고|먹고 ?싶|먹을래|밥|간식|라면|고기|푸딩|hungry|food|\beat\b", re.I)),
    (MIYAAA, re.compile(r"다녀왔|왔어|왔다|들어왔|도착|퇴근|i'?m home|i'?m back", re.I)),
    (YAHA, re.compile(r"안녕|하이|ㅎㅇ|찾았|발견|짠|등장|hello|\bhi\b|\bhey\b|found", re.I)),
    (URA, re.compile(r"최근|요즘|요새|크다|거대|엄청|big|huge|recent|lately", re.I)),
    (PURUYA, re.compile(r"힘들|피곤|지쳤|우울|슬퍼|화이팅|파이팅|응원|같이|가자|하자|할까|tired|sad|let'?s", re.I)),
    (HUNG, re.compile(r"맞지|그치|그렇지|맞아|그래\?|인정|좋아\?|right\?|yes|yeah", re.I)),
    (PURU, re.compile(r"해줘|해 줘|부탁|알았|알겠|ㅇㅋ|오케이|please|\bok\b|okay", re.I)),
    (HAA, re.compile(r"\?|뭐|왜|진짜|헐|어떻게|what|why|huh", re.I)),
)

ART = """\
⠀⠀⠀⠀⠀⠀⢀⣀⠀⢀⡤⣤⡀
⠀⠀⠀⠀⠀⠀⡏⠉⢷⣼⠀⠈⢳⡄
⠀⠀⠀⠀⠀⠀⢷⠀⠀⠹⣇⠀⠀⢷
⠀⠀⠀⠀⠀⠀⠈⣇⠀⠀⠹⡆⠀⠸⡇
⠀⠀⠀⠀⠀⠀⠀⠸⡆⠀⠀⢻⠀⠀⣧
⠀⠀⠀⠀⠀⠀⠀⠀⢹⡀⠀⠸⠆⠀⠃⠠⢤⣤⣄⣀
⠀⠀⠀⠀⣀⡤⠖⠋⠉⠁⠀⠀⠀⠀⠀⢀⣀⠀⠀⠉⠛⢶⣄
⠀⠀⢀⡼⠋⠀⢀⡤⠖⠀⠀⠀⠀⠀⠀⠉⠉⠉⠛⢦⡀⠀⠉⢿⣄
⠀⢠⡞⠁⠀⢠⠏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢻⡄⠀⠀⢻⣆
⠀⡿⠀⠀⠀⠿⠀⠀⠀⣀⣀⠀⠀⠀⠀⠀⣠⢤⣄⠀⠀⠃⠀⠀⠈⣿
⢸⡇⠀⠀⠀⠀⠀⠀⢸⣯⣿⡇⠀⠀⠀⠀⠻⠯⠟⢀⡀⡀⢠⠀⠀⢻⡀
⢸⡇⠀⠀⠀⣤⢠⢠⡄⠉⠉⠀⢀⡀⣶⣀⡄⠀⠀⠘⠁⠁⠈⠀⠀⣼
⠀⢿⡀⠀⠀⠉⠀⠀⠀⠀⠀⠀⠈⠉⠩⠏⠀⠀⠀⠀⠀⠀⠀⠀⢀⡟
⠀⠈⢷⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡼⠁
⠀⠀⠀⠙⣶⠄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠠⡀
⠀⠀⠀⢰⡏⠀⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡦⢀⡇
⠀⠀⠀⠀⠳⢤⡬⠇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣸⠓⠉
⠀⠀⠀⠀⠀⠀⠒⠚⢦⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣴⠃
⠀⠀⠀⠀⠀⢠⠖⠀⠀⠙⠷⣤⣀⡀⠀⢀⡀⠠⣤⠖⠋⠁
⠀⠀⠀⠀⠀⠀⠀⠇⠠⠄⠰⠀⠀⠙⣏⣉⡷⣤⠟
"""

SMALL_BANNER = r"""
   (\(\
   ( -.-)   {title}
   o_(")(")
"""

USAGI = Character(
    key="usagi",
    name="우사기",
    expressions=(YAHA, URA, PURUYA, PURU, HAA, HUNG, JURURI, MIYAAA, UA, PURUYA_URAURA),
    rules=RULES,
    fallback=(HAA, PURU, HUNG, URA, PURUYA, YAHA),
    greeting=YAHA,
    farewell=PURU,
    small_banner=SMALL_BANNER,
    art=ART,
)


class Usagi(Chatter):
    """우사기와 대화하는 객체.

    >>> Usagi(seed=0).reply("배고파").expression.word
    '쥬르리'
    """

    def __init__(self, seed: int | None = None) -> None:
        super().__init__(USAGI, seed)
