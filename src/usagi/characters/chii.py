"""치이카와: 왓! 와아… 후!

성격: 겁 많고 잘 우는 울보지만, 다정하고 친구를 아끼는 노력파.
      긴장하면 실수하지만 분해하며 극복해 나간다.
말투: 말수가 거의 없고, 짧은 감탄사로 기분을 나타낸다.
      대답은 기본적으로 "응" 아니면 "이얏!".

참고 (모두 팬·정리 사이트이며 공식 설정집은 아님, 2026-10 검색):
- https://dijitama.com/tiikawa_koubun/ (ワッ / ワァ / フッ 의 쓰임)
- https://dijitama.com/tiikawa_syabereru/ (말수가 적고 짧은 말로 대화)
- https://kaji-amehare.com/chikawa-kobun/ (「フ！」는 대개 기쁠 때, 「うん」「イヤッ」으로 의사 표시)
- https://dic.pixiv.net/a/ちいかわ(キャラクター) (긴장을 잘 하는 노력파)
- https://chiikawabiyori.com/articles/chiikawa-character-personality-guide-2026 (겁 많은 울보, 친구 생각)
한국어 표기는 일본어 원문을 옮긴 것이라 공식 한국어판과 다를 수 있다.
"""

from __future__ import annotations

import re

from ..core import Character, Expression

WAT = Expression("왓", ("앗, 놀랐다",), "살짝 놀랐을 때 (ワッ)")
WAA = Expression("와아…", ("우와…", "(울먹)"), "저도 모르게 소리가 나올 때, 울음이 터질 때 (ワァ…)")
FU = Expression("후!", ("기뻐!", "안녕!"), "기쁠 때, 인사할 때 (フ！)")
UN = Expression("응", ("응", "알겠어"), "동의할 때 (うん)")
IYA = Expression("이얏!", ("싫어!", "무서워!"), "거절할 때, 위험하거나 공격받을 때 (イヤッ)")
YADA = Expression("야다앗!", ("절대 싫어!",), "강하게 거부할 때 (ヤダーッ)")
YAA = Expression("야앗!!", ("간다!",), "맞서거나 스스로를 북돋울 때 (ヤーッ!!)")

RULES = (
    (YAA, re.compile(r"토벌|싸우|싸움|덤벼|이기자|힘내|화이팅|파이팅|fight", re.I)),
    (IYA, re.compile(r"무서|벌레|괴물|귀신|위험|공격|scary", re.I)),
    (YADA, re.compile(r"싫|안 ?할래|하기 ?싫|안 ?돼|\bno\b", re.I)),
    (WAA, re.compile(r"슬퍼|슬프|울|눈물|ㅠ|ㅜ|우와|대박|예쁘|귀여|신기|멋있|멋지|wow|\bsad\b", re.I)),
    (FU, re.compile(r"좋아|기뻐|기쁘|최고|고마|칭찬|맛있|배고|먹|안녕|하이|hello|\bhi\b", re.I)),
    (WAT, re.compile(r"헉|헐|깜짝|놀랐|갑자기|진짜\?|what", re.I)),
    (UN, re.compile(r"해줘|부탁|같이|가자|할래|맞지|그치|ㅇㅋ|\bok\b|okay|yes|\?", re.I)),
)

SMALL_BANNER = r"""
   .-"-.
  ( o.o )   {title}
   (")(")
"""

CHII = Character(
    key="chii",
    name="치이카와",
    expressions=(WAT, WAA, FU, UN, IYA, YADA, YAA),
    rules=RULES,
    fallback=(UN, UN, WAT, WAA),
    greeting=FU,
    farewell=UN,
    small_banner=SMALL_BANNER,
    draft=True,
    profile=(
        "성격: 겁 많고 잘 우는 울보지만 다정하고 친구를 아끼는 노력파",
        "말투: 말수가 거의 없고 짧은 감탄사로 기분을 표현, 대답은 대개 '응' 아니면 '이얏!'",
    ),
)
