import hashlib
import re
from typing import Callable

import ftfy
from loguru import logger
from nltk.corpus import stopwords
from pydantic import BaseModel, Field
from toolz import compose_left, identity
from trafilatura import extract
from unidecode import unidecode

_punctuation_pattern = re.compile(
    r"[!\"'\\#\$%&\'\(\)\*\+,-\./:;<=>\?@\[\]\^_`\{|\}~§ª¹º¿–—“”�]"
)
_spaces_pattern = re.compile(r"\s+")
_horizontal_spaces_pattern = re.compile(r"[^\S\n\v\f\r\u2028\u2029]+")
_vertical_spaces_pattern = re.compile(r"[\n\v\f\r\u2028\u2029]+", flags=re.MULTILINE)
_begin_line_strip_pattern = re.compile(r"^\s+", flags=re.MULTILINE)
_end_line_strip_pattern = re.compile(r"\s+$", flags=re.MULTILINE)
_number_pattern = re.compile(r"\d+")


class TextProcessorConfig(BaseModel):
    html: bool = Field(default=False, description="Extract text from HTML")
    strip: bool = Field(default=True, description="Strip text")
    remove_accents: bool = Field(default=False, description="Remove accents")
    remove_punct: bool = Field(default=False, description="Remove punctuation")
    remove_stopwords: bool = Field(default=False, description="Remove stopwords")
    remove_numbers: bool = Field(default=False, description="Remove numbers")
    lower: bool = Field(default=False, description="Lowercase text")
    fix_encoding: bool = Field(default=False, description="Fix encoding")
    limit_spaces: bool = Field(default=False, description="Limit spaces")
    limit_horizontal_spaces: bool = Field(
        default=False, description="Limit horizontal spaces"
    )
    limit_vertical_spaces: bool = Field(
        default=False, description="Limit vertical spaces"
    )
    line_strip: bool = Field(default=False, description="Strip line")
    language: str = Field(default="portuguese", description="Language for stopwords")


def build_text_processor(
    config: TextProcessorConfig | None = None,
) -> Callable[[str], str]:
    config = config or TextProcessorConfig()
    if config.remove_accents:
        config.fix_encoding = True
        logger.warning("Setting remove_accents to True also sets fix_encoding to True")

    if config.remove_stopwords:
        config.limit_spaces = True
        logger.warning(
            "Setting remove_stopwords to True also sets limit_spaces to True"
        )

    if config.limit_spaces:
        config.limit_horizontal_spaces = False
        config.limit_vertical_spaces = False
        config.line_strip = False
        logger.warning(
            "Setting limit_spaces to True also sets limit_horizontal_spaces, "
            "limit_vertical_spaces and line_strip to False"
        )

    return compose_left(
        _eye(lambda text: extract(text) or "", config.html),
        _eye(ftfy.fix_text, config.fix_encoding),
        _eye(lambda text: re.sub(_number_pattern, "", text), config.remove_numbers),
        _eye(lambda text: re.sub(_punctuation_pattern, " ", text), config.remove_punct),
        _eye(lambda text: re.sub(_spaces_pattern, " ", text), config.limit_spaces),
        _eye(
            lambda text: re.sub(_vertical_spaces_pattern, "\n", text),
            config.limit_vertical_spaces,
        ),
        _eye(
            lambda text: re.sub(_horizontal_spaces_pattern, " ", text),
            config.limit_horizontal_spaces,
        ),
        _eye(
            lambda text: re.sub(_begin_line_strip_pattern, "", text),
            config.line_strip,
        ),
        _eye(lambda text: re.sub(_end_line_strip_pattern, "", text), config.line_strip),
        _eye(
            lambda text: re.sub(_get_stopwords_pattern(config.language), " ", text),
            config.remove_stopwords,
        ),
        _eye(unidecode, config.remove_accents),
        _eye(str.lower, config.lower),
        _eye(str.strip, config.strip),
    )


def _get_stopwords_pattern(language: str):
    return re.compile(
        (
            r"(^|\s|" + _punctuation_pattern.pattern + r")"
            r"(" + "|".join(stopwords.words(language)) + r")"
            r"(\s+|$|" + _punctuation_pattern.pattern + r")"
        ),
        flags=re.IGNORECASE | re.MULTILINE,
    )


def _eye(function: Callable[[str], str], condition: bool):
    return function if condition else identity


def hash_text(text: str) -> str:
    return str(hashlib.sha512(text.encode("utf-8")).hexdigest())
