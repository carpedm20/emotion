from typing import Any, Optional

from emotion_wheel_general import draw_emotion_wheel

EmotionSpace = dict[str, Any]


english_emotion_space_1: EmotionSpace = {
    "NEGATIVE_VALENCE": {
        "HIGH_AROUSAL": {
            "ANGER": [
                "anger",
                "rage",
                "outrage",
                "indignation",
                "irritation",
                "frustration",
                "resentment",
                "contempt",
            ],
            "FEAR": [
                "fear",
                "panic",
                "terror",
                "dread",
                "anxiety",
                "apprehension",
                "alarm",
                "shock",
            ],
            "STRESS": [
                "stress",
                "tension",
                "pressure",
                "overwhelm",
                "agitation",
                "restlessness",
            ],
            "ENVY": [
                "envy",
                "jealousy",
                "inferiority",
                "comparison anxiety",
                "covetousness",
            ],
        },
        "LOW_AROUSAL": {
            "SADNESS": [
                "sadness",
                "sorrow",
                "grief",
                "heartbreak",
                "melancholy",
                "despair",
            ],
            "DISAPPOINTMENT": [
                "disappointment",
                "discouragement",
                "disillusionment",
                "regret",
                "resignation",
            ],
            "SHAME": [
                "shame",
                "embarrassment",
                "humiliation",
                "self-consciousness",
                "guilt",
            ],
            "LONELINESS": [
                "loneliness",
                "isolation",
                "alienation",
                "homesickness",
                "abandonment",
            ],
            "BOREDOM": [
                "boredom",
                "apathy",
                "ennui",
                "listlessness",
                "indifference",
            ],
        },
    },
    "POSITIVE_VALENCE": {
        "HIGH_AROUSAL": {
            "JOY": [
                "joy",
                "delight",
                "elation",
                "exhilaration",
                "jubilation",
                "bliss",
            ],
            "MOTIVATION": [
                "excitement",
                "enthusiasm",
                "anticipation",
                "eagerness",
                "drive",
            ],
            "INTEREST": [
                "interest",
                "curiosity",
                "fascination",
                "engagement",
                "wonder",
            ],
            "CONFIDENCE": [
                "pride",
                "confidence",
                "accomplishment",
                "self-assurance",
                "dignity",
            ],
            "DESIRE": [
                "attraction",
                "desire",
                "longing",
                "yearning",
                "passion",
            ],
            "PLAYFULNESS": [
                "amusement",
                "playfulness",
                "fun",
                "cheerfulness",
                "merriment",
            ],
        },
        "LOW_AROUSAL": {
            "CALM": [
                "calm",
                "serenity",
                "tranquility",
                "relaxation",
                "stillness",
            ],
            "CONTENTMENT": [
                "contentment",
                "satisfaction",
                "fulfillment",
                "ease",
                "comfort",
            ],
            "LOVE": [
                "love",
                "affection",
                "warmth",
                "tenderness",
                "intimacy",
                "trust",
            ],
            "RELIEF": [
                "relief",
                "reassurance",
                "release",
                "gratitude",
                "thankfulness",
            ],
            "NOSTALGIA": [
                "nostalgia",
                "wistfulness",
                "reminiscence",
                "sentimentality",
            ],
        },
    },
}

korean_emotion_space_1: EmotionSpace = {
    "부정 정서": {
        "고각성": {
            "분노": [
                "분노",
                "몹시 화남",
                "크게 화남",
                "답답한 분노",
                "억울해서 화남",
                "미워하는 마음",
                "짜증",
                "좌절감",
                "감정이 격해짐",
                "신경질",
                "성가심",
                "원망",
                "속이 끓음",
                "깔보는 마음",
                "무시함",
            ],
            "공포": [
                "두려움",
                "공황",
                "공포",
                "경계심",
                "섬뜩함",
                "오싹함",
                "걱정됨",
                "불안",
                "불편함",
                "초조함",
                "걱정",
                "불길한 예감",
                "지나친 의심",
                "깜짝 놀람",
                "충격",
            ],
            "스트레스": [
                "스트레스",
                "긴장",
                "압박감",
                "감당 못함",
                "고통",
                "마음 흔들림",
                "안절부절못함",
                "부담감",
                "기운 빠짐",
                "절박함",
                "미리 걱정함",
                "잘해야 해서 불안",
            ],
            "시기": [
                "부러움",
                "질투",
                "남의 것을 탐냄",
                "시샘",
                "열등감",
                "남과 비교 불안",
            ],
        },
        "저각성": {
            "슬픔": [
                "슬픔",
                "깊은 슬픔",
                "가슴이 미어짐",
                "우울함",
                "마음이 가라앉음",
                "희망이 없음",
                "마음의 상처",
                "풀이 죽음",
                "너무 괴로움",
                "한숨만 나옴",
                "사별의 슬픔",
            ],
            "실망": [
                "실망",
                "기가 죽음",
                "정떨어짐",
                "기운 빠짐",
                "후회",
                "나를 탓함",
                "포기하고 싶음",
            ],
            "수치심": [
                "수치심",
                "민망함",
                "모욕당한 느낌",
                "창피함",
                "남 눈치 봄",
                "죄책감",
                "잘못했다고 느낌",
            ],
            "외로움": [
                "외로움",
                "집이 그리움",
                "혼자 남은 느낌",
                "소외된 느낌",
                "버려진 느낌",
            ],
            "지루함": [
                "지루함",
                "무기력",
                "지겨움",
                "힘이 없음",
                "무관심",
                "피로감",
            ],
        },
    },
    "긍정 정서": {
        "고각성": {
            "행복감": [
                "기쁨",
                "즐거움",
                "기분이 올라감",
                "푹 빠져 좋음",
                "너무 행복함",
                "짜릿함",
                "들뜸",
                "신남",
                "환호",
                "더없는 행복",
            ],
            "의욕": [
                "흥분",
                "열정",
                "기대감",
                "의욕",
                "활력",
                "기운이 솟음",
            ],
            "관심": [
                "흥미",
                "호기심",
                "푹 빠짐",
                "궁금증",
                "몰입감",
                "열중",
                "신기함",
                "크게 감탄함",
            ],
            "자신감": [
                "자부심",
                "이겨낸 기분",
                "자신감",
                "내가 해냄",
                "성취감",
                "스스로 믿음",
                "당당함",
            ],
            "원하는 마음": [
                "끌림",
                "반함",
                "갖고 싶음",
                "열정",
                "그리움",
                "간절히 원함",
            ],
            "신남": [
                "즐거움",
                "장난기",
                "흥겨움",
                "활기",
                "재미",
                "명랑함",
            ],
        },
        "저각성": {
            "차분함": [
                "차분함",
                "평온함",
                "고요함",
                "몸이 풀림",
                "조용함",
                "안정감",
            ],
            "만족": [
                "만족감",
                "흐뭇함",
                "가득 참",
                "평화로움",
                "편안함",
                "안락함",
            ],
            "사랑": [
                "사랑",
                "애정",
                "따뜻함",
                "다정함",
                "친밀감",
                "신뢰",
                "호감",
                "끝까지 아낌",
                "안쓰러워함",
            ],
            "안도": [
                "안도감",
                "긴장이 풀림",
                "안심",
                "감사",
                "고마움",
            ],
            "향수": [
                "향수",
                "추억에 잠김",
                "그때가 그리움",
                "지난 일 떠올림",
            ],
        },
    },
}

other_emotion_space_1: EmotionSpace = {
    "부정 정서": {
        "고각성": {
            "분노": [
                "격분한",
                "격앙된",
                "노한",
                "답답한",
                "분개한",
                "억울한",
                "언짢은",
                "성난",
                "미운",
                "심술 난",
                "화나는",
                "짜증 나는",
                "성가신",
                "시샘하는",
            ],
            "공포": [
                "겁나는",
                "겁에 질린",
                "깜짝 놀란",
                "무서워하는",
                "두려운",
                "충격을 받은",
            ],
            "불안": [
                "걱정되는",
                "긴장되는",
                "마음이 안 놓이는",
                "당황한",
                "뒤숭숭한",
                "안절부절못하는",
                "어쩔 줄 모르는",
                "불안정한",
                "불안한",
                "초조한",
                "전전긍긍하는",
                "조바심 나는",
                "신경이 곤두선",
                "신경 쓰이는",
                "조마조마한",
                "혼란스러운",
                "조심스러운",
                "민감한",
            ],
            "스트레스": [
                "갑갑한",
                "고민스러운",
                "고통스러운",
                "곤란한",
                "골치 아픈",
                "괴로운",
                "근심스러운",
                "불편한",
                "속상한",
                "힘겨운",
            ],
        },
        "저각성": {
            "슬픔": [
                "마음 상한",
                "낙담한",
                "낙심한",
                "애도하는",
                "불쌍한",
                "상심한",
                "우울한",
                "울적한",
                "슬픈",
                "슬픔에 잠긴",
                "시무룩한",
                "침울한",
                "절망스러운",
                "불행한",
                "비참한",
                "섭섭한",
            ],
            "실망": [
                "기가 꺾인",
                "기가 죽은",
                "용기를 잃은",
                "좌절스러운",
                "풀이 죽은",
                "실망한",
                "의기소침한",
                "정떨어지는",
                "불만족스러운",
                "비관적인",
            ],
            "수치심": [
                "민망한",
                "부끄러운",
            ],
            "외로움": [
                "고독한",
                "외로운",
            ],
            "무기력": [
                "기운 없는",
                "기운을 잃은",
                "맥 풀리는",
                "무감각한",
                "냉담한",
                "냉정한",
                "무관심한",
                "무기력한",
                "힘이 빠지는",
                "무딘",
                "관심이 없는",
                "지겨운",
                "지루한",
                "지치는",
                "질리는",
                "피곤한",
                "피로한",
                "졸리는",
                "심드렁한",
                "마음 내키지 않는",
            ],
            "염려": [
                "미심쩍은",
                "우려하는",
                "의심스러운",
                "주저하는",
                "회의적인",
                "심란한",
            ],
        },
    },
    "긍정 정서": {
        "고각성": {
            "환희": [
                "감격한",
                "감동한",
                "기분이 들뜨는",
                "기쁨에 겨운",
                "기쁨에 넘치는",
                "머리가 핑 도는",
                "숨이 멎을 듯한",
                "놀라운",
                "날아갈 듯한",
                "더없이 행복한",
                "환희에 찬",
                "황홀한",
                "짜릿한",
                "희열에 넘치는",
            ],
            "활력": [
                "유쾌한",
                "명랑한",
                "기운 나는",
                "즐거운",
                "상쾌한",
                "생기가 나는",
                "쾌활한",
                "활발한",
                "활기에 찬",
                "흥분되는",
            ],
            "열정": [
                "고무된",
                "기대되는",
                "열광적인",
                "열렬한",
                "열정이 넘치는",
                "열의가 생기는",
                "열중한",
                "영감을 받은",
            ],
            "자신감": [
                "용기를 얻은",
                "의기양양한",
                "자신만만한",
                "자신에 찬",
                "자유로운",
                "득의양양한",
                "영광스러운",
                "희망에 찬",
                "찬란한",
            ],
            "호기심": [
                "감탄한",
                "관심이 가는",
                "멋진",
                "호기심이 생기는",
                "흥미가 생기는",
            ],
        },
        "저각성": {
            "안정감": [
                "차분한",
                "침착한",
                "안정되는",
                "편안한",
                "평온한",
                "평화로운",
            ],
            "만족": [
                "만족스러운",
                "기꺼운",
                "홀가분한",
                "충만감이 드는",
                "흡족한",
                "행복한",
                "낙관적인",
            ],
            "애정": [
                "마음이 넓어지는",
                "마음이 열리는",
                "사랑스러운",
                "상냥한",
                "애정이 생기는",
                "믿음이 생기는",
                "친근한",
                "따뜻한",
                "반가운",
            ],
            "안도": [
                "마음이 놓이는",
                "긴장이 풀리는",
                "안도하는",
                "안심되는",
            ],
            "감사": [
                "감사하는",
                "고마운",
                "축복받은",
            ],
        },
    },
}

def _prune_leaf_lists(node: Any, retention_ratio: float) -> Any:
    """
    Keep the wheel hierarchy fixed and simplify only the outermost emotion lists.
    """
    if isinstance(node, list):
        keep_count = max(1, min(len(node), int(len(node) * retention_ratio)))
        return node[:keep_count]

    return {
        key: _prune_leaf_lists(value, retention_ratio)
        for key, value in node.items()
    }


def _build_simplified_series(
    base_space: EmotionSpace,
    retention_ratios: tuple[float, ...],
) -> list[EmotionSpace]:
    return [
        _prune_leaf_lists(base_space, retention_ratio)
        for retention_ratio in retention_ratios
    ]


ENGLISH_LEAF_RETENTION_RATIOS: tuple[float, ...] = (
    1.0,
    0.9,
    0.8,
    0.7,
    0.6,
    0.5,
    0.4,
    0.3,
)

KOREAN_LEAF_RETENTION_RATIOS: tuple[float, ...] = (
    1.0,
    0.9,
    0.8,
    0.7,
    0.6,
    0.5,
    0.4,
    0.3,
)

OTHER_LEAF_RETENTION_RATIOS: tuple[float, ...] = (
    1.0,
    0.9,
    0.8,
    0.7,
    0.6,
    0.5,
    0.4,
    0.3,
)

(
    english_emotion_space_1,
    english_emotion_space_2,
    english_emotion_space_3,
    english_emotion_space_4,
    english_emotion_space_5,
    english_emotion_space_6,
    english_emotion_space_7,
    english_emotion_space_8,
) = _build_simplified_series(
    english_emotion_space_1,
    ENGLISH_LEAF_RETENTION_RATIOS,
)

(
    korean_emotion_space_1,
    korean_emotion_space_2,
    korean_emotion_space_3,
    korean_emotion_space_4,
    korean_emotion_space_5,
    korean_emotion_space_6,
    korean_emotion_space_7,
    korean_emotion_space_8,
) = _build_simplified_series(
    korean_emotion_space_1,
    KOREAN_LEAF_RETENTION_RATIOS,
)

(
    other_emotion_space_1,
    other_emotion_space_2,
    other_emotion_space_3,
    other_emotion_space_4,
    other_emotion_space_5,
    other_emotion_space_6,
    other_emotion_space_7,
    other_emotion_space_8,
) = _build_simplified_series(
    other_emotion_space_1,
    OTHER_LEAF_RETENTION_RATIOS,
)


ENGLISH_EMOTION_SPACES: list[EmotionSpace] = [
    english_emotion_space_1,
    english_emotion_space_2,
    english_emotion_space_3,
    english_emotion_space_4,
    english_emotion_space_5,
    english_emotion_space_6,
    english_emotion_space_7,
    english_emotion_space_8,
]

KOREAN_EMOTION_SPACES: list[EmotionSpace] = [
    korean_emotion_space_1,
    korean_emotion_space_2,
    korean_emotion_space_3,
    korean_emotion_space_4,
    korean_emotion_space_5,
    korean_emotion_space_6,
    korean_emotion_space_7,
    korean_emotion_space_8,
]

OTHER_EMOTION_SPACES: list[EmotionSpace] = [
    other_emotion_space_1,
    other_emotion_space_2,
    other_emotion_space_3,
    other_emotion_space_4,
    other_emotion_space_5,
    other_emotion_space_6,
    other_emotion_space_7,
    other_emotion_space_8,
]

LANGUAGE_EMOTION_SPACES: dict[str, list[EmotionSpace]] = {
    "english": ENGLISH_EMOTION_SPACES,
    "korean": KOREAN_EMOTION_SPACES,
    "other": OTHER_EMOTION_SPACES,
}


def render_wheel_set(
    emotion_space: EmotionSpace,
    stem: str,
    *,
    background: Optional[str] = None,
    transparent_background: Optional[bool] = None,
) -> None:
    for ext in ("png", "svg"):
        draw_emotion_wheel(
            emotion_space,
            output_path=f"{stem}.{ext}",
            background=background,
            transparent_background=transparent_background,
        )


def render_language_wheels(
    language: str,
    spaces: list[EmotionSpace],
    *,
    background: Optional[str] = None,
    transparent_background: Optional[bool] = None,
) -> None:
    for idx, emotion_space in enumerate(spaces, start=1):
        render_wheel_set(
            emotion_space,
            f"{language}_emotion_wheel_{idx}",
            background=background,
            transparent_background=transparent_background,
        )


for language, spaces in LANGUAGE_EMOTION_SPACES.items():
    render_language_wheels(language, spaces)
