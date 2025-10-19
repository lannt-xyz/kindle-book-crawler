import unicodedata

def saintize_vietnamese_text(text):
    """
    Chuyển từ tiếng Việt có dấu sang không dấu (ASCII) và thay khoảng trắng thành underscore.
    """
    if not isinstance(text, str):
        return ""
    text = unicodedata.normalize('NFD', text)
    text = ''.join(c for c in text if unicodedata.category(c) != 'Mn')
    text = text.replace('đ', 'd').replace('Đ', 'D')
    text = text.replace(' ', '_')
    return text
