"""하치와레: …라는 거야!? 어떻게든 되라앗!

성격: 밝고 긍정적인 낙천가. 수다스럽고 겁이 없으며, 그 낙천성이 친구들의 위기를 구한다.
말투: 메인 셋 중 거의 유일하게 문장으로 말하며, 말이 짧은 치이카와·우사기의 마음을
      대신 말해주는 '통역' 역할. 도치법(말 순서 바꾸기), 말끝 늘이기, 느낌표를 많이 쓴다.
      상대 말을 받아 "…라는 거야!?" 하고 되묻는 게 대표 패턴.

참고 (모두 팬·정리 사이트이며 공식 설정집은 아님, 2026-10 검색):
- https://dijitama.com/tiikawa_koubun/ (「…ってコト！？」, 통역 역할)
- https://dokodemireru01.com/hachiware-speech-style/ (도치법 말투)
- https://dengekionline.com/article/202504/37956 (밝고 긍정적, 수다스럽고 겁이 없음)
- https://news.mynavi.jp/article/20240328-2916068/ , https://soul-brighten.com/hachiware/ ,
  https://chiikawabiyori.com/articles/chiikawa-memorable-lines-dialogue (명대사)
- https://oggi.jp/7229113 (「うれしい!ワ!」「だいじょうぶ!だいじょうぶ!」「たいへん!やば!」)
"안녕~!" / "또 봐~!" 는 출처 없는 기본 인사. 한국어 표기는 일본어 원문을 옮긴 것이라
공식 한국어판과 다를 수 있다.
"""

from __future__ import annotations

import re

from ..core import Character, Expression

TTEKOTO = Expression(
    "…라는 거야!?",
    ("…라는 거야!?",),
    "놀라거나 새로 알았을 때, 상대 말을 정리·대변할 때 (…ってコト！？)",
    echo=True,
)
NANTOKA = Expression("어떻게든 되라앗!", ("될 대로 되라!", "그래도 해보자"), "막막하거나 위기일 때 (なんとかなれーッ)")
DAIJOUBU = Expression("괜찮아! 괜찮아!", ("괜찮아", "위로"), "친구가 힘들어할 때 (だいじょうぶ!だいじょうぶ!)")
ASERANAI = Expression("서두르지 않아도 괜찮아~", ("천천히 해",), "조급해할 때 (焦んなくて大丈夫だよー)")
WA = Expression("기쁘다! 와!", ("기뻐!",), "기쁠 때 (うれしい!ワ!)")
TAIHEN = Expression("큰일이다! 위험해!", ("큰일났다",), "갑자기 일이 터졌을 때 (たいへん!やば!)")
NAICHATTA = Expression("울어버렸다…", ("(울음)", "대신 말해주기"), "누가 울 때 (泣いちゃった)")
YOROKOBI = Expression("기쁨이 없어~", ("힘 빠진다",), "나쁜 일이 겹칠 때 (喜びがない〜)")
RETIRE = Expression(
    "안 될 것 같으면 그만두면 되지!", ("부담 갖지 마",), "도전을 망설일 때 (だめそうだったらさーリタイアすればいいよね)"
)
ICHIMAI = Expression(
    "한 장이라도 좋은 게 있으면 됐지!", ("결과보다 과정",), "사진·실패 얘기 (一枚でもいいのがあればさッイイよねッ!)"
)
ANNYEONG = Expression("안녕~!", ("안녕",), "만났을 때")
MATANE = Expression("또 봐~!", ("또 보자",), "헤어질 때")

RULES = (
    (NAICHATTA, re.compile(r"울었|울고|울어|눈물|ㅠ|ㅜ|crying", re.I)),
    (YOROKOBI, re.compile(r"비 ?와|최악|짜증|되는 일|안 ?풀|우울|불운", re.I)),
    (TAIHEN, re.compile(r"큰일|사고|떨어뜨|깨졌|늦었|잃어버|고장", re.I)),
    (NANTOKA, re.compile(r"걱정|불안|시험|모르겠|어떡|어쩌|막막|망했|worry", re.I)),
    (RETIRE, re.compile(r"도전|해볼까|자신 ?없|무리|할 수 있을까", re.I)),
    (ASERANAI, re.compile(r"급해|서둘|빨리|조급", re.I)),
    (DAIJOUBU, re.compile(r"힘들|슬퍼|슬프|피곤|지쳤|무서|\bsad\b|tired", re.I)),
    (ICHIMAI, re.compile(r"사진|카메라|실패|photo", re.I)),
    (ANNYEONG, re.compile(r"안녕|하이|ㅎㅇ|hello|\bhi\b|\bhey\b", re.I)),
    (WA, re.compile(r"좋아|기뻐|기쁘|신난|최고|대박|우와|맛있|성공|합격|해냈|ㅋㅋ|wow|yay", re.I)),
    (TTEKOTO, re.compile(r"\?|진짜|그러니까|라던데|래요|이래", re.I)),
)

SMALL_BANNER = r"""
   /\_/\
  ( o.o )   {title}
   (")(")
"""

HACHI = Character(
    key="hachi",
    name="하치와레",
    expressions=(
        TTEKOTO, NANTOKA, DAIJOUBU, ASERANAI, WA, TAIHEN,
        NAICHATTA, YOROKOBI, RETIRE, ICHIMAI, ANNYEONG, MATANE,
    ),
    rules=RULES,
    fallback=(TTEKOTO, TTEKOTO, WA, DAIJOUBU),
    greeting=ANNYEONG,
    farewell=MATANE,
    small_banner=SMALL_BANNER,
    draft=True,
    profile=(
        "성격: 밝고 긍정적인 낙천가, 수다스럽고 겁이 없음",
        "말투: 문장으로 말하며 치이카와·우사기의 마음을 대신 말해주는 통역 역할,",
        "      도치법·말끝 늘이기·느낌표, 상대 말을 받아 '…라는 거야!?' 하고 되물음",
    ),
)
