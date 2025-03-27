import re

# 예외 규칙 사전 정의
EXCEPTION_MAP = {
    "기저귀 갈았어": "기저귀 교체",
    "기저귀 샀어": "기저귀 구매",
    "낮잠 시작": "애기 수면 시작",
    "애기 잔다": "애기 수면 시작",
    "애기 자": "애기 수면 시작",
    "낮잠 끝": "애기 수면 종료",
    "낮잠 종료": "애기 수면 종료",
    "애기 깼어": "애기 수면 종료",
    "수유 했어": "수유",
    "수유 끝": "수유",
    "수유 종료": "수유",
}

def parse_action(text: str) -> str:
    text = text.strip()

    # ✅ 예외 처리 먼저
    if text in EXCEPTION_MAP:
        return EXCEPTION_MAP[text]

    # 일반적인 어미 제거 처리
    ending_patterns = [
        r"(했었|했|할|갔었|갔|갈|왔었|왔|다녀왔|먹였었|먹였)(다|어|었어|었는데|지|네|잖아|니|게|까|래|려고)?$"
    ]

    for pattern in ending_patterns:
        text = re.sub(pattern, "", text).strip()

    return text
