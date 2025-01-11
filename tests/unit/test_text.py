from nlp_gems.text import build_text_processor, TextProcessorConfig


def test_text_processor():
    text = "This is a test sentence."
    tp = build_text_processor()
    assert tp(text) == text


def test_text_processor_lower():
    text = "This is a test sentence."
    tp = build_text_processor(TextProcessorConfig(lower=True))
    assert tp(text) == text.lower()

def test_text_processor_remove_punctuation():
    text = "This is a test sentence."
    tp = build_text_processor(TextProcessorConfig(remove_punct=True))
    assert tp(text) == "This is a test sentence"

def test_text_processor_remove_numbers():
    text = "This is a test sentence with some numbers 1234 5678."
    tp = build_text_processor(TextProcessorConfig(remove_numbers=True))
    assert tp(text) == "This is a test sentence with some numbers  ."

def test_text_processor_remove_stopwords():
    text = "This is a test sentence with some stopwords."
    tp = build_text_processor(TextProcessorConfig(language="english", remove_stopwords=True))
    assert tp(text) == "is test sentence some stopwords."

def test_text_processor_remove_accents():
    text = "This is a test sentence with some accents éà."
    tp = build_text_processor(TextProcessorConfig(remove_accents=True))
    assert tp(text) == "This is a test sentence with some accents ea."

def test_text_processor_fix_encoding():
    text = "This is a test sentence with some weird encoding: (à¸‡'âŒ£')à¸‡."
    tp = build_text_processor(TextProcessorConfig(fix_encoding=True))
    assert tp(text) == "This is a test sentence with some weird encoding: (ง'⌣')ง."

def test_text_processor_limit_spaces():
    text = "This is a test sentence with some weird     spaces."
    tp = build_text_processor(TextProcessorConfig(limit_spaces=True))
    assert tp(text) == "This is a test sentence with some weird spaces."

def test_text_processor_limit_horizontal_spaces():
    text = "This is a test sentence with some weird     spaces."
    tp = build_text_processor(TextProcessorConfig(limit_horizontal_spaces=True))
    assert tp(text) == "This is a test sentence with some weird spaces."

def test_text_processor_limit_vertical_spaces():
    text = "This is a test sentence with some weird\n\nvertical spaces."
    tp = build_text_processor(TextProcessorConfig(limit_vertical_spaces=True))
    assert tp(text) == "This is a test sentence with some weird\nvertical spaces."

def test_text_processor_line_strip():
    text = "  This a line  \n"
    tp = build_text_processor(TextProcessorConfig(line_strip=True))
    assert tp(text) == "This a line"

def test_text_processor_html():
    text = "<html><body>This is a test sentence.</body></html>"
    tp = build_text_processor(TextProcessorConfig(html=True))
    assert tp(text) == "This is a test sentence."


def test_lower_and_limit_spaces():
    text = "This is a    test sentence."
    tp = build_text_processor(TextProcessorConfig(lower=True, limit_spaces=True))
    assert tp(text) == "this is a test sentence."

def test_remove_punctuation_and_remove_numbers():
    text = "This is a test sentence with some numbers 1234 5678."
    tp = build_text_processor(TextProcessorConfig(remove_punct=True, remove_numbers=True))
    assert tp(text) == "This is a test sentence with some numbers"

def test_remove_stopwords_and_remove_accents():
    text = "This is a test sentence with some accents éà."
    tp = build_text_processor(TextProcessorConfig(language="english", remove_stopwords=True, remove_accents=True))
    assert tp(text) == "is test sentence some accents ea."