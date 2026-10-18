import re

from textstat import textstat

_CONTAINS_CHINESE_PATTERN = re.compile(r'[\u4e00-\u9fff0-9]')
_CHINESE_OR_NUMBER_PATTERN = re.compile(r'[\u4e00-\u9fff0-9]')
_TOKENS_PATTERN = re.compile(r'[\u4e00-\u9fff]+|[a-zA-Z]+|[0-9]+')


def contains_chinese(text):
    # 正则表达式，用于匹配中文字符 + 数字 -> 都认为是 zh
    return bool(_CONTAINS_CHINESE_PATTERN.search(text))


def get_text_syllable_num(text):
    syllable_num = 0
    tokens = _TOKENS_PATTERN.findall(text)
    # print(tokens)
    if contains_chinese(text):
        for token in tokens:
            if _CHINESE_OR_NUMBER_PATTERN.search(token):
                syllable_num += len(token)
            else:
                syllable_num += textstat.syllable_count(token)
    else:
        syllable_num = textstat.syllable_count(text)

    return syllable_num


def get_text_tts_dur(text):
    min_speed = 3  # 2.18 #
    max_speed = 5.50

    ratio = 0.8517 if contains_chinese(text) else 1.0

    syllable_num = get_text_syllable_num(text)
    max_dur = syllable_num * ratio / max_speed
    min_dur = syllable_num * ratio / min_speed

    return max_dur, min_dur