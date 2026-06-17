import re
from collections import Counter
from dataclasses import dataclass, field

try:
    import jieba
    _JIEBA_AVAILABLE = True
except ImportError:
    _JIEBA_AVAILABLE = False


@dataclass
class TextStats:
    char_count: int = 0
    word_count: int = 0
    line_count: int = 0
    sentence_count: int = 0
    top_words: list[tuple[str, int]] = field(default_factory=list)


_SENTENCE_ENDINGS = re.compile(r'[.!?。！？]+')
_EN_WORD_PATTERN = re.compile(r"[A-Za-z']+")
_CJK_CHAR_PATTERN = re.compile(r'[\u4e00-\u9fff]+')


def _tokenize(text: str) -> list[str]:
    tokens: list[str] = []

    en_words = _EN_WORD_PATTERN.findall(text)
    tokens.extend(w.lower() for w in en_words)

    cjk_blocks = _CJK_CHAR_PATTERN.findall(text)
    for block in cjk_blocks:
        if _JIEBA_AVAILABLE:
            tokens.extend(t for t in jieba.lcut(block) if t.strip())
        else:
            tokens.extend(list(block))

    return tokens


def analyze(text: str) -> TextStats:
    char_count = len(text)
    line_count = text.count('\n') + (1 if text and not text.endswith('\n') else 0) if text else 0
    words = _tokenize(text)
    word_count = len(words)
    sentence_count = len(_SENTENCE_ENDINGS.findall(text))

    top_words = Counter(words).most_common(10)

    return TextStats(
        char_count=char_count,
        word_count=word_count,
        line_count=line_count,
        sentence_count=sentence_count,
        top_words=top_words,
    )


if __name__ == "__main__":
    sample = """The quick brown fox jumps over the lazy dog.
The dog barked. 那只敏捷的棕色狐狸跳过了懒惰的狗。
那只狗汪汪叫。狐狸跑掉了！狐狸回来了吗？不，狐狸没有回来。
Another sentence here. And another one! 狐狸很聪明。"""

    stats = analyze(sample)
    print(f"字符数: {stats.char_count}")
    print(f"单词数: {stats.word_count}")
    print(f"行数:   {stats.line_count}")
    print(f"句子数: {stats.sentence_count}")
    print("高频词 Top 10:")
    for word, count in stats.top_words:
        print(f"  {word}: {count}")
