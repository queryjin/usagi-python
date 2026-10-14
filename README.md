# usagi-python 🐰

치이카와(ちいかわ)의 **우사기**처럼 대답하는 터미널 대화 라이브러리.
의존성 없이 파이썬 표준 라이브러리만 사용합니다.

```
   (\(\
   ( -.-)   우사기와 대화하기  (/help 도움말, /quit 종료)
   o_(")(")

우사기> 야하!
나> 다녀왔어
우사기> 미야아아!!
나> 배고파
우사기> 쥬르리 쥬르리!
나> 이 푸딩 진짜 맛있다
우사기> 우아!
나> 그게 뭔데?
우사기> 하아?
```

## 설치

```bash
pip install git+https://github.com/queryjin/usagi-python.git
# 개발용
git clone https://github.com/queryjin/usagi-python.git && cd usagi-python
pip install -e ".[dev]"
```

## 터미널에서 사용

```bash
usagi                 # 대화 모드
usagi -e              # 대답 옆에 번역 표시 (대화 중 /explain 으로 토글)
usagi --no-art        # 시작 화면의 우사기 아트 숨기기
usagi art             # 우사기 아트만 출력
usagi say 배고파       # 한 문장만 대답
usagi translate 우라   # 우사기 말 번역 -> 최근 / 거대하다
usagi dict            # 사전 보기
echo "맛있다" | usagi  # 파이프 입력
python -m usagi       # 설치 없이 실행 (src 를 PYTHONPATH 에 둘 때)
```

대화 모드 명령어: `/help`, `/dict`, `/explain`, `/quit`

대화 모드를 시작하면 우사기 점자 아트(`src/usagi/art.py`)가 먼저 나옵니다.
아트 폭은 74칸이라, 터미널이 그보다 좁으면 작은 토끼 배너로 대신합니다.

## 파이썬에서 사용

```python
from usagi import Usagi, say, translate

say("배고파")                       # '쥬르리!'
say("배고파", explain=True)         # '쥬르리!  (먹고 싶다…)'
translate("후응")                   # '맞아'

u = Usagi(seed=42)                  # 시드 고정 → 재현 가능
reply = u.reply("요즘 어때?")
reply.expression.word               # '우라'
reply.text                          # '우라!!'
```

## 우사기 사전

| 표현 | 의미 | 반응하는 입력 예시 |
|---|---|---|
| 야하 | 뭔가를 찾았을 때, 혹은 등장할 때 | 안녕, 찾았다, hello |
| 우라 | 최근 / 거대하다 (상황에 따라 다름) | 요즘, 최근, 거대, big |
| 푸루야 | 공감 요구, 따라오라는 초대, 응원 | 힘들어, 화이팅, 같이 가자 |
| 푸루 | 잡초 이름, 알겠어 | 해줘, 부탁해, ok |
| 하아? | 뭐야?, 놀랐을 때, 어이없을 때 | 뭐?, 왜, 진짜?, 헐 |
| 후응 | 맞아 (긍정의 의미) | 맞지?, 그치, 인정 |
| 쥬르리 | 식욕이 돌 때 | 배고파, 먹고 싶다, 밥 |
| 미야아아 | 어서 오세요 | 다녀왔어, 퇴근, 도착 |
| 우아 | 맛있다 | 맛있다, 존맛, yummy |
| 푸루야우라우라 | 해독 불가능한 기괴한 괴성 | ㅋㅋㅋㅋ, 미쳤다, 대박, !!! |

매칭되는 키워드가 없으면 무작위로 대답합니다. 규칙은 `src/usagi/core.py` 의 `RULES` 에서
위쪽일수록 우선순위가 높습니다. 표현을 추가하려면 `vocab.py` 에 `Expression` 을 만들고 `RULES` 에 패턴을 넣으면 됩니다.

## 테스트

```bash
pytest
```
