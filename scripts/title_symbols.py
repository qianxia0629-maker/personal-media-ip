"""Check a title against explicitly allowed punctuation and symbol tokens."""
import unicodedata

VIDEO_CHANNEL_SYMBOLS = '《》〈〉“”‘’"\'「」『』：:+＋?？%％℃'
VIDEO_CHANNEL_SEQUENCES = ['°C']


def invalid_title_characters(title, allowed_symbols, allowed_sequences=()):
    """Allow letters/numbers, ordinary spaces, and configured symbols only."""
    invalid = []
    i = 0
    while i < len(title):
        token = next((s for s in allowed_sequences if s and title.startswith(s, i)), None)
        if token:
            i += len(token)
            continue
        char = title[i]
        category = unicodedata.category(char)
        if (char != ' ' and char not in allowed_symbols
                and category[0] != 'L' and category != 'Nd'):
            if char not in invalid:
                invalid.append(char)
        i += 1
    return invalid
